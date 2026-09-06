[← Flux](../README.md)

# flux-pr — ephemeral preview environments

A proof of concept for the flux-operator feature that creates a set of Kubernetes resources while
something exists upstream — a branch, or an open pull request — and deletes them when it goes away.

Two examples are checked in, deliberately side by side, because they answer different questions:

| | Example 1 — branch | Example 2 — pull request |
|---|---|---|
| Provider type | `GitHubBranch` | `GitHubPullRequest` |
| Environment lives while… | the branch `dev` **exists** | a PR **from** `dev` is **open** |
| Destroyed by | deleting the branch | merging or closing the PR — the branch survives |
| Namespace | `preview-dev` | `preview-pr-<number>` |
| Cost to test | one `git push` | opening a PR |

<https://fluxoperator.dev/docs/crd/resourcesetinputprovider/>
<https://fluxoperator.dev/docs/crd/resourceset/>

---

## How it works

Two CRDs, and the split between them is the whole idea:

| Object | Role |
|---|---|
| `ResourceSetInputProvider` | polls a Git **provider API** (not the repository) and publishes a list of `status.exportedInputs` — one entry per branch/PR that matches the filter |
| `ResourceSet` | a template rendered **once per exported input**, and garbage-collected when an input disappears |

```
GitHub API ──poll every 1m──→ ResourceSetInputProvider
                                (match → 1 input, no match → 0)
                                        │
                                        ▼
                                   ResourceSet
                                        │
                       ┌────────────────┴────────────────┐
                       ▼                                 ▼
              1 input → Namespace + Deployment    0 inputs → pruned
                        + Service
```

The important part is that **deletion is not an event handler**. The provider simply stops exporting
the input, the `ResourceSet` re-renders to an empty set, and the operator prunes what it owns. There
is no webhook, no CI job, no cleanup cron. That is why it survives a controller restart, a missed
webhook, or a branch deleted while the cluster was down.

## What is checked in

Both examples reconcile from the same folder, via
[`clusters/dev/kustomization/flux-pr.yaml`](../../../../../clusters/dev/kustomization/flux-pr.yaml),
listed in [`clusters/dev/kustomization.yaml`](../../../../../clusters/dev/kustomization.yaml). They
use different namespaces, so they coexist without fighting.

### Example 1 — while the branch exists

- [`resourcesetinputprovider.yaml`](resourcesetinputprovider.yaml) — `type: GitHubBranch` against
  `github.com/andreyolv/pikakube`, filtered to `includeBranch: "^dev$"`, polled every `1m`.
- [`resourceset.yaml`](resourceset.yaml) — renders a `Namespace`, a podinfo `Deployment` and a
  `Service` into `preview-dev`.

The environment exists for as long as the branch does. That is the cheapest thing to demonstrate and
the wrong lifecycle for a real preview: a long-lived `dev` branch means a permanently-running
"ephemeral" environment.

### Example 2 — while a pull request is open

- [`resourcesetinputprovider-pr.yaml`](resourcesetinputprovider-pr.yaml) —
  `type: GitHubPullRequest`, same repository and secret, `includeBranch: "^dev$"`.
- [`resourceset-pr.yaml`](resourceset-pr.yaml) — renders into `preview-pr-<< inputs.id >>`, and
  records the PR number, source branch and author as labels, the PR title as an annotation.

This is the lifecycle the feature is for: `dev` can exist indefinitely, and the environment appears
only once someone opens a PR and disappears when it is merged or closed.

## Two decisions shared by both

- **`secretRef: flux-system`** reuses the GitHub App secret the `FluxInstance` already references as
  `spec.sync.pullSecret` — see [`flux-operator/`](../flux-operator/README.md). The
  `ResourceSetInputProvider` accepts the same `githubAppID` / `githubAppInstallationID` /
  `githubAppPrivateKey` keys, so the POC adds no new credential. If the repository is public the
  block can be deleted entirely, at the cost of GitHub's 60 requests/hour unauthenticated limit —
  which a `1m` interval on two providers would exhaust.
- **How the namespace is named.** For `GitHubBranch` the exported `id` is an adler32 checksum, so
  `preview-<< inputs.id >>` would give `preview-1f2a04c9`; example 1 uses
  `<< inputs.branch | slugify >>` instead. For `GitHubPullRequest` the `id` **is** the PR number, so
  example 2 uses it directly — stable across force-pushes and immediately recognisable.

## Exported inputs, by provider

What the template can reference. This is the practical difference between the two examples:

| Provider | Exported inputs |
|---|---|
| `GitHubBranch` | `id` (adler32 checksum), `branch`, `sha` |
| `GitHubPullRequest` | `id` (**PR number**), `branch` (source), `sha`, `author`, `title` |

Plus `inputs.provider.{apiVersion,kind,name,namespace}` on every input set, and anything added under
the provider's `spec.defaultValues`.

## Testing example 1 (branch)

```sh
git switch -c dev && git push -u origin dev
```

Then, within a minute or two:

```sh
kubectl get resourcesetinputprovider -n flux-system pikakube-preview-branches -o yaml   # status.exportedInputs
kubectl get resourceset -n flux-system pikakube-preview
kubectl get all -n preview-dev
```

Tear down — and note that this is the point of example 2: **the branch has to be deleted.**

```sh
git push origin --delete dev
```

## Testing example 2 (pull request)

The branch can already exist; nothing is created by pushing it.

```sh
git switch -c dev && git push -u origin dev
gh pr create --base main --head dev --title "preview poc" --body "testing flux-operator previews"
```

Then:

```sh
kubectl get resourcesetinputprovider -n flux-system pikakube-preview-pull-requests -o yaml
kubectl get ns -l pikakube.dev/preview-kind=pull-request
kubectl get all -n preview-pr-1        # replace 1 with the PR number
```

Tear down — the branch stays, the environment goes:

```sh
gh pr close 1
```

`spec.wait: true` on both `ResourceSet`s means `Ready` is reported only once the Deployment is
actually available, so the condition is a real answer rather than "the apply succeeded".

To confirm the inputs reached the template, the container's UI message carries them
(`PR #1 by andreyolv (dev @ <sha>)`):

```sh
kubectl port-forward -n preview-pr-1 svc/podinfo 8080:80
```

Faster loop while iterating on the templates — skip Git and apply directly:

```sh
kubectl apply -f resourcesetinputprovider-pr.yaml -f resourceset-pr.yaml
flux-operator reconcile inputprovider pikakube-preview-pull-requests -n flux-system
flux-operator reconcile resourceset pikakube-preview-pr -n flux-system
```

## "dev → main" is only half expressible

The filter struct is `includeBranch` / `excludeBranch` / `includeTag` / `excludeTag` /
`includeEnvironment` / `excludeEnvironment` / `labels` / `limit` / `semver`. **There is no
base-branch or target-branch filter.** `includeBranch: "^dev$"` on a change-request provider matches
the pull request's *source* branch, and the base is not part of the exported inputs either.

So a PR `dev → main` and a PR `dev → staging` are indistinguishable to the provider, and both get an
environment. Three ways out, in order of how much they cost:

1. **Accept it.** With one long-lived branch and one base branch this distinction never comes up.
2. **A label.** Uncomment `filter.labels: ["deploy/preview"]` and require the opt-in on the PR. This
   is the honest answer and it is what the upstream examples use, because it also solves the bigger
   problem below.
3. **`type: ExternalService`.** Point it at a small endpoint that queries the GitHub API itself and
   returns whatever inputs you want, base branch included.

The `labels` filter matters more than it looks. Without it, every PR whose head matches — including
dependabot's — gets a namespace. That is the failure mode of every preview-environment system, which
is why it is left in the manifest as a commented-out line rather than omitted.

## Gotchas

| Gotcha | Why |
|---|---|
| The provider polls an **API**, not the `GitRepository` | source-controller is not involved. The branch does not have to be reconciled by Flux, and the repository does not even have to be the one Flux syncs. |
| A force-push moves `sha`, not `id` | for PRs the environment is updated in place. For branches the `id` is a checksum of the branch name, so it is also stable. |
| No `serviceAccountName` on either `ResourceSet` | they apply with flux-operator's own service account, which is cluster-wide. Fine for a POC; on a shared cluster set `spec.serviceAccountName` to something scoped. |
| `prune: false` on the Flux `Kustomization` | deleting these files does **not** remove the CRs. Delete the `ResourceSet` first (which prunes the previews), then the provider. |
| `<< >>`, not `{{ }}` | the operator uses different delimiters so templates can contain Helm ones. |
| Rate limits | one poll per interval **per provider**, and there are two here. `1m` each is fine with a GitHub App (5000 req/h) and wrong unauthenticated. |
| A preview environment is a **real** environment | it gets the same admission policies, image pulls and resource quotas as anything else. Requests are set here for that reason, and `filter.limit` caps the blast radius. |
| Flux Operator version | the chart is pinned to `0.24.1` in [`flux-operator/helm/`](../flux-operator/helm/ocirepository.yaml). `spec.skip` and `spec.schedule` on the provider are newer additions — check the CRD before using them. |

`spec.skip` is worth knowing about once the label filter is in use: `"deploy/preview-pause"`
suspends an environment without closing the PR, and `"!ci/passed"` refuses to build one until a
label is present.

---

[← Flux](../README.md)
