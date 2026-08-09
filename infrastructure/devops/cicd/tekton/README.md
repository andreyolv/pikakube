[← CI/CD](../README.md)

# Tekton

<https://github.com/tektoncd/pipeline>
<https://github.com/tektoncd/operator>

---

## The problem it solves

Every CI system invents its own execution model — its own job scheduler, its own container runtime
integration, its own artifact handling. On Kubernetes, all of that already exists. Tekton's premise
is that CI should be **Kubernetes primitives**, not a product bolted onto Kubernetes.

The model is four CRDs and almost nothing else:

| Resource | What it is |
|---|---|
| `Task` | a sequence of steps; **each step is a container**, all sharing one pod |
| `TaskRun` | one execution of a `Task`, with parameters bound |
| `Pipeline` | a graph of `Task`s, with `runAfter` ordering and parameter/result passing |
| `PipelineRun` | one execution of a `Pipeline` |

Everything else follows from being Kubernetes-native: RBAC controls who can run what, `Workspace`s
are PVCs or ConfigMaps, results pass between tasks as strings, and a run is an object you can
`kubectl get`. Tekton Chains adds signed provenance for supply-chain attestation; Triggers adds
webhook-driven runs.

**The important thing to understand is what Tekton deliberately does not provide.** No UI worth
using, no promotion model, no built-in triggers, no notifications, no opinion about how a pipeline
should be structured. That is the design: **Tekton is a substrate other people build CI products
on.** Jenkins X, OpenShift Pipelines, Red Hat's CI offering and several vendor platforms are all
Tekton underneath.

## When to use it

- **You are building a CI platform for other teams**, and you want the execution engine to be
  Kubernetes-native and standard rather than something you wrote
- Everything must be **CRDs**, reconciled and RBAC-controlled, because that is the platform's
  model and CI should not be an exception
- **Supply-chain attestation matters** — Tekton Chains signs build provenance (SLSA) at the
  controller level, which is stronger than signing inside a pipeline step
- You are on OpenShift, where Tekton ships as OpenShift Pipelines and is the supported path
- You need pipelines callable from many places with strong multi-tenancy, where Kubernetes RBAC
  is the right access-control mechanism

## When not to use it

- **You want to use CI, not build it.** Out of the box Tekton has no PR integration, no usable
  dashboard and no ecosystem comparable to the Actions Marketplace. The gap between "installed"
  and "a team can ship with it" is months of platform work
- The code is on GitHub and normal CI is the requirement.
  [GitHub Actions](../github-actions/README.md) with self-hosted runners answers it immediately
- You want **general DAGs of containers** rather than CI specifically —
  [Argo Workflows](../argo-workflows/README.md) is the better-shaped tool, with a real UI
- You want to escape YAML. Tekton is *more* YAML than most, not less; every task is a manifest.
  [Dagger](../dagger/README.md) is the opposite direction
- A small team. The operational cost — a controller, webhooks, CRDs, and the missing product layer
  around it — is not repaid at that scale

## Notes

The two recorded repositories, and the split matters:

- <https://github.com/tektoncd/pipeline> — the core controller and the `Task` / `Pipeline` CRDs.
  This is Tekton itself.
- <https://github.com/tektoncd/operator> — the **operator**, which is what this repository deploys.
  It installs and lifecycles the components (Pipelines, Triggers, Chains, Dashboard) through a
  `TektonConfig` resource, instead of applying each component's release YAML separately. Given how
  many moving pieces Tekton has, the operator is the sane installation path — but note it means
  **two levels of indirection**: Helm installs the operator, the operator installs Tekton, and the
  component versions come from the operator's version, not from the chart.

**What is deployed here**, and it has a defect:

| Piece | Detail |
|---|---|
| Source | a Flux `GitRepository` named `tekton` in `flux-system`, tag `v0.74.0` |
| Path filter | `ignore:` excludes everything except `/charts/tekton-operator` |
| Release | HelmRelease `tekton` in namespace `tekton`, `chart: charts/tekton-operator` |
| Values | defaults only |

**The `GitRepository` URL is broken.** It reads:

```
url: https://github.com/tektoncd/operator.git]
```

with a trailing `]`. That is a typo, and Flux cannot clone it — the source will fail to reconcile
and the HelmRelease will never install. Recording it rather than silently fixing it, because it is
the kind of defect that explains why a component appears "deployed" in the repository and absent
in the cluster.

Two things worth understanding about the rest of that configuration:

**The chart is pulled from Git, not from a Helm repository.** Tekton's operator does not publish a
chart to a registry, so the chart source is the operator's own repository at a tag, with an
`ignore:` block narrowing the clone to just the chart directory. That pattern — `GitRepository` +
path filter + `chart:` as a path — is the fallback for any project that ships a chart in-tree
without publishing it, and it is worth knowing because it recurs.

**Pinning by tag is deliberate.** `ref.tag: v0.74.0` means the chart cannot move under you; a
branch ref would make every reconcile a potential upgrade. For an operator that then controls
component versions, that pin is the only version control you have.

The wider point for this repository: Tekton here is **mapped, not adopted**, and given the platform
already runs [GitHub Actions](../github-actions/README.md) for CI and Flux for delivery, the case
for adopting it would have to come from somewhere specific — most plausibly **Tekton Chains** and
signed build provenance, which is the one capability nothing else in this folder provides at the
controller level. That connects directly to the unfinished Cosign signing noted in
[`github-actions/workflows/`](../github-actions/workflows/README.md).

---

[← CI/CD](../README.md)
