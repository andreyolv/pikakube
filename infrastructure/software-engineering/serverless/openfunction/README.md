[← Serverless](../README.md)

# OpenFunction

<https://github.com/OpenFunction/OpenFunction>
<https://github.com/OpenFunction/charts>

---

## The problem it solves

OpenFunction does not implement a function platform. It **composes** one out of projects that
already exist, and puts a single `Function` CRD in front of them:

| Concern | Delegated to |
|---|---|
| Building the image from source | Tekton Pipelines or Shipwright Build |
| Running synchronous functions | Knative Serving |
| Running asynchronous, event-driven functions | Dapr, for bindings and pub/sub |
| Scaling those async functions on event backlog | KEDA |
| Ingress for the resulting services | Contour |

You write one `Function` resource — source repository, builder, runtime — and the operator turns
it into a build, an image, and a running workload of the appropriate kind.

The appeal is obvious: each piece is a well-known project, and you get the whole path from Git to
a scaled, triggered function without integrating them yourself.

The cost is equally obvious, and is the thing to weigh: **you now own all of them.** Every
component is a control plane to upgrade, a CRD set to keep compatible, and a place a failure can
come from — reached through an abstraction that makes it less obvious which one broke.

## When to use it

- you want **source-to-function** on Kubernetes and are prepared to run the stack that makes it
  possible
- you would have deployed Knative, Dapr and KEDA anyway, and want them wired together
- both sync (HTTP) and async (event-driven) functions are needed, with one authoring model

## When not to use it

- you want one thing, not five — [OpenFaaS](../openfaas/README.md) or
  [Fission](../fission/README.md) are self-contained
- you already run [Knative](../knative/README.md) directly and are happy building images in CI —
  OpenFunction's main value is the part you have already solved
- the composition-layer risk matters to you: an integration project's fate depends on five
  upstreams it does not control, and on someone keeping the seams working across their releases

## Notes

**What is deployed here:** chart `openfunction` 0.7.0 from
`https://openfunction.github.io/charts/`, in the `openfunction` namespace, with these global
toggles:

```yaml
global:
  Dapr:
    enabled: false
  Keda:
    enabled: false
  KnativeServing:
    enabled: true
  TektonPipelines:
    enabled: false
  ShipwrightBuild:
    enabled: false
  Contour:
    enabled: false
```

**Only Knative Serving is on.** That is a deliberate and sensible choice for an evaluation — the
chart can otherwise install five subsystems into the cluster in one apply, and refusing that is
the right instinct. It is worth being precise about what it leaves:

| Turned off | What stops working |
|---|---|
| Tekton and Shipwright | **no in-cluster build** — a `Function` cannot be built from source |
| Dapr and KEDA | **no async runtime** — event-driven functions and backlog-based scaling are gone |
| Contour | no ingress from this chart; whatever ingress the cluster already has must serve it |

What remains is Knative Serving with a `Function` CRD in front of it — which is very close to
running Knative directly, and raises the fair question of what OpenFunction is adding at these
settings.

**The committed example would not run as-is**, and the reason is exactly the table above. The
example `Function` in `examples/function.yaml` declares a `build:` block — an
`openfunction/builder-go` builder, a `srcRepo` pointing at the OpenFunction samples repository, a
`git-repo-secret` and a `push-secret` — and the build components that would act on it are
disabled. Its `serving.runtime` is `knative`, which *is* enabled, so the serving half would work
from a pre-built image. If this is picked up again, that mismatch is the first thing to reconcile:
either enable a build backend and provide the two secrets, or drop the `build` block and point the
function at an image that already exists.

**Dapr appears twice in this repository**, and the judgement recorded against it in
[`integration/dapr/`](../../integration/dapr/README.md) — *"cool, but too much overengineering"* —
applies here too. Enabling OpenFunction's async runtime means adopting Dapr as a dependency of the
function platform, which is a larger commitment than adopting it for one service.

---

[← Serverless](../README.md)
