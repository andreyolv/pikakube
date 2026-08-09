[← Version control](../README.md)

# Gitness

<https://github.com/harness/harness>

---

## The problem it solves

**A self-hosted forge with a pipeline engine built into it, rather than bolted alongside.**
Gitness — now named **Harness Open Source** — is Harness's open-source forge: repositories, pull
requests, and CI/CD in one binary.

| Capability | Detail |
|---|---|
| Repositories and pull requests | the forge basics |
| **Built-in pipelines** | CI/CD as a first-class part of the product, not a separate system |
| **Drone lineage** | the pipeline engine descends directly from Drone |
| Container-native steps | every step runs in a container, as in Drone |
| Web IDE | edit and commit from the browser |
| Gitspaces | cloud development environments |
| Single binary | Go, with SQLite for a small deployment or PostgreSQL for a real one |

The distinguishing claim against [Gitea](../gitea/README.md) is integration: Gitea added
Actions-compatible CI later and it is a separate subsystem with its own runners; Gitness was
designed around its pipelines from the start.

## When to use it

- when **CI should come with the forge**, in one product, with one configuration
- **an existing Drone estate** — the pipeline syntax and mental model carry across, which is the
  clearest reason to choose it
- where container-native pipeline steps are the preferred CI model
- when evaluating Harness's commercial platform and an open-source starting point is wanted

## When not to use it

- where **long-term independence from a single vendor** matters — see the note below
- where the ecosystem matters: this is much smaller than GitHub's or even Gitea's
- where the forge should be boring and the CI should be somebody else's problem —
  [Gitea](../gitea/README.md) is the lower-risk self-hosted choice
- **as the source of the GitOps repository on the cluster it deploys** —
  [§4 of the parent](../README.md#4-the-gitops-consequence)

## Notes

Recorded link:

- <https://github.com/harness/harness> — the repository.

**The history matters, and the recorded URL is the evidence of it.** Harness acquired **Drone**,
the container-native CI engine, in 2020. Gitness was built as its successor: rather than a CI
system that integrates with a forge, a forge with Drone's engine inside it. The project was
subsequently renamed **Harness Open Source**, and the repository moved from `harness/gitness` to
`harness/harness` — which is why the recorded link says `harness/harness` while everything in this
folder is named `gitness`.

Two consequences follow:

1. **Drone knowledge transfers directly.** Pipeline definitions, the step-as-a-container model and
   the plugin ecosystem are familiar to anyone who has run Drone. For a team already on Drone,
   this is the natural continuation.
2. **It is one vendor's open-source edition.** Direction, naming and feature emphasis follow
   Harness's commercial product, and the rename is itself an illustration of that. It is not a
   community-governed project like [Gitea](../gitea/README.md), and it is worth weighing that
   before making it the forge a platform depends on.

**What is configured here** — a Flux `HelmRelease` in a `gitness` namespace, and the source is the
detail worth reading:

```yaml
chart:
  spec:
    chart: charts/gitness
    sourceRef:
      kind: GitRepository
      name: gitness
```

**There is no chart repository**, so the release points at a `GitRepository` and the chart
directory inside the project's own repository. Three consequences: there is no chart version to
pin — the release tracks whatever the Git ref resolves to, which is a reproducibility gap; there
are no chart release notes to read before an upgrade; and, most relevant to this platform, **the
release depends on GitHub being reachable at reconciliation time**, which is
[§4 of the parent](../README.md#4-the-gitops-consequence) applied to a chart source rather than a
manifest source. The same pattern appears for
[Kraken](../../image/p2p-mirror/kraken/README.md).

The values are left as a comment pointing at the chart's `values.yaml`, so this is mapped rather
than tuned. Before it is anything more than an experiment, the storage decision is the one to make
first: the default single-binary mode uses SQLite on a volume, which is fine for evaluation and is
not a basis for anything holding real repositories.

## Where it fits here

Mapped in [`version-control/`](../README.md) as the forge-plus-pipelines option, between
[Gitea](../gitea/README.md)'s minimalism and [GitLab](../gitlab/README.md)'s weight.

For this repository the case is narrow. Flux already handles delivery, so an integrated CI engine
is not the gap; and Gitea covers the forge requirement with community governance, a proper chart
and a much larger installed base. Gitness becomes the right answer where Drone is already in use
and the pipelines are the reason for the choice.

---

[← Version control](../README.md)
