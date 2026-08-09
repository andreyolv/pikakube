[← Image update automation](../README.md)

# Argo CD Image Updater

<https://github.com/argoproj-labs/argocd-image-updater>

---

## The problem it solves

**The same job as [Flux's image automation](../flux-image-update/README.md), for Argo CD.** It
watches registries for new tags matching a policy and updates the `Application` so the new image
is deployed.

Configuration is by **annotation on the `Application`** rather than by separate resources:

```yaml
metadata:
  annotations:
    argocd-image-updater.argoproj.io/image-list: app=myrepo/myapp
    argocd-image-updater.argoproj.io/app.update-strategy: semver
    argocd-image-updater.argoproj.io/write-back-method: git
```

The update strategies available:

| Strategy | Selects |
|---|---|
| `semver` | the highest version matching a constraint |
| `latest` / `newest-build` | the most recently pushed tag by creation time |
| `digest` | the current digest of a mutable tag — pinning content while following a tag |
| `alphabetical` | the last in lexical order, for sortable tags |

The `digest` strategy is a genuinely useful one that has no direct Flux equivalent: it follows a
tag like `stable` but deploys the **digest** it currently points at, so the deployment is
reproducible even though the upstream tag is mutable.

## When to use it

- **Argo CD is the GitOps engine** — this is the tool built for it
- new builds should deploy without a pipeline editing manifests
- the `digest` strategy solves a real problem: tracking a third-party mutable tag while keeping
  deployments pinned to exact content
- development environments, where automatic updates are wanted and review is not

## When not to use it

- **Flux is the engine** — use [its own image automation](../flux-image-update/README.md), which is
  a first-class part of the toolkit rather than a companion project
- in `argocd` write-back mode anywhere the repository is meant to be authoritative; see below
- in production without a pull-request step, for the reasons in
  [§6 of the parent](../README.md#6-when-not-to-automate)
- where the annotation-based configuration is a problem: policies live on the `Application`
  resource, which makes them harder to review as a set than Flux's separate `ImagePolicy` objects

## Notes

Recorded link:

- <https://github.com/argoproj-labs/argocd-image-updater> — the project.

**The organisation matters.** `argoproj-labs` is the incubation area, not `argoproj` proper. Image
Updater is a companion project to Argo CD rather than part of it, with correspondingly lighter
support and release guarantees. That is a real difference from Flux, where image automation is a
maintained part of the GitOps Toolkit. It works, it is widely used, and it should be evaluated
knowing where it sits.

**The write-back mode is the decision that matters**, and the default is not the safe one:

| Mode | Behaviour | Verdict |
|---|---|---|
| **`git`** | commits the new image into the Git repository | the repository stays authoritative |
| `argocd` | sets a parameter override on the live `Application`, **without touching Git** | produces exactly the drift GitOps exists to remove |

In `argocd` mode the running state no longer matches what the repository says. Argo CD will report
the `Application` as synced, because the override is part of its own state — so the drift is
invisible in the place you would look for it. Rebuilding the cluster from Git produces the old
image, and nobody finds out until they try.

There is a narrow case for it: a preview environment that is torn down anyway, where the
repository was never meant to describe it. Everywhere else, **`write-back-method: git`**.

What is configured here: a Flux `HelmRelease` at chart version **0.11.3** from the `argo` chart
repository, in its own namespace, with values left as comments pointing at the chart's
`values.yaml`. That is worth noting for what it is — the tool is mapped and installable, not in
use, since Argo CD is not the engine reconciling this repository.

## Where it fits here

Mapped as the Argo-side equivalent for completeness. **This repository runs Flux**, so
[`../flux-image-update/`](../flux-image-update/README.md) is the applicable implementation and the
one with a full worked example.

The comparison is useful in one direction: Flux splits scanning, policy and writing across three
inspectable resources; Argo CD Image Updater puts all of it in annotations on one. The Flux model
is easier to debug — an `ImagePolicy` can be created and its selection read before anything is
given write access to Git.

---

[← Image update automation](../README.md)
