[← Flux](../README.md)

# flux-pr — ephemeral preview environments

A minimal proof of concept for the flux-operator feature that creates a set of Kubernetes resources
while a branch (or a pull request) exists, and deletes them when it goes away.

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
                                (branch ^dev$ exists → 1 input)
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

- [`resourcesetinputprovider.yaml`](resourcesetinputprovider.yaml) — `type: GitHubBranch` against
  `github.com/andreyolv/pikakube`, filtered to `includeBranch: "^dev$"`, polled every `1m`.
- [`resourceset.yaml`](resourceset.yaml) — renders a `Namespace`, a podinfo `Deployment` and a
  `Service` per input, into `preview-<branch>`.
- [`clusters/dev/kustomization/flux-pr.yaml`](../../../../../clusters/dev/kustomization/flux-pr.yaml)
  — the Flux `Kustomization` that reconciles this folder, listed in
  [`clusters/dev/kustomization.yaml`](../../../../../clusters/dev/kustomization.yaml).

Two decisions worth reading:

- **`secretRef: flux-system`** reuses the GitHub App secret the `FluxInstance` already references as
  `spec.sync.pullSecret` — see [`flux-operator/`](../flux-operator/README.md). The
  `ResourceSetInputProvider` accepts the same `githubAppID` / `githubAppInstallationID` /
  `githubAppPrivateKey` keys, so the POC adds no new credential. If the repository is public the
  block can be deleted entirely, at the cost of GitHub's 60 requests/hour unauthenticated limit —
  which a `1m` interval would exhaust exactly.
- **`preview-<< inputs.branch | slugify >>`** rather than `<< inputs.id >>`. For `GitHubBranch` the
  `id` is an adler32 checksum, so namespaces would be called `preview-1f2a04c9`. For
  `GitHubPullRequest` the `id` *is* the PR number, and `preview-<< inputs.id >>` is the right choice.

## Testing it

```sh
git switch -c dev && git push -u origin dev
```

Then, within a minute or two:

```sh
kubectl get resourcesetinputprovider -n flux-system pikakube-preview-branches -o yaml   # status.exportedInputs
kubectl get resourceset -n flux-system pikakube-preview                                 # Ready
kubectl get ns -l pikakube.dev/preview=true
kubectl get all -n preview-dev
```

`spec.wait: true` means the `ResourceSet` reports `Ready` only once the Deployment is actually
available, so a `Ready` condition is a real answer rather than "the apply succeeded".

To see the inputs arrived in the template — the container's UI message is
`preview of <branch> @ <sha>`:

```sh
kubectl port-forward -n preview-dev svc/podinfo 8080:80
```

Tear down:

```sh
git push origin --delete dev
```

The namespace and everything in it goes away on the next provider poll. Nothing else to clean up.

Faster loop while iterating on the templates — skip Git and apply directly:

```sh
kubectl apply -f resourcesetinputprovider.yaml -f resourceset.yaml
flux-operator reconcile inputprovider pikakube-preview-branches -n flux-system
flux-operator reconcile resourceset pikakube-preview -n flux-system
```

## Switching to pull requests

The branch provider was chosen because testing it costs one `git push` rather than an open PR. The
actual ephemeral-environment pattern is PR-driven, and the change is confined to the provider:

```yaml
spec:
  type: GitHubPullRequest
  filter:
    labels:
      - "deploy/preview"     # only PRs a human opted in
    limit: 5
```

With `GitHubPullRequest` the exported inputs become `id` (the PR number), `sha`, `branch`, `author`
and `title` — so the `ResourceSet` can name namespaces `preview-<< inputs.id >>` and pass the PR
author or title into the workload. `spec.skip.labels` is the complement: `"deploy/preview-pause"`
suspends an environment without closing the PR, and `"!ci/passed"` refuses to build one until a
label is present.

The `labels` filter matters more than it looks. Without it, every PR opened by anyone — including
dependabot — gets a namespace. That is the failure mode of every preview-environment system.

## Gotchas

| Gotcha | Why |
|---|---|
| The provider polls an **API**, not the `GitRepository` | source-controller is not involved. The branch does not have to be reconciled by Flux, and the repository does not even have to be the one Flux syncs. |
| No `serviceAccountName` on the `ResourceSet` | it applies with flux-operator's own service account, which is cluster-wide. Fine for a POC; on a shared cluster set `spec.serviceAccountName` to something scoped. |
| `prune: false` on the Flux `Kustomization` | deleting these files does **not** remove the CRs. Delete the `ResourceSet` first (which prunes the previews), then the provider. |
| `<< >>`, not `{{ }}` | the operator uses different delimiters so templates can contain Helm ones. |
| Rate limits | one poll per interval per provider. `1m` is fine with a GitHub App (5000 req/h) and wrong unauthenticated. |
| A preview environment is a **real** environment | it gets the same admission policies, image pulls and resource quotas as anything else. Requests are set here for that reason. |
| Flux Operator version | the `FluxInstance` chart is pinned to `0.24.1` in [`flux-operator/helm/`](../flux-operator/helm/ocirepository.yaml). `spec.skip` and `spec.schedule` on the provider are newer additions — check the CRD before using them. |

---

[← Flux](../README.md)
