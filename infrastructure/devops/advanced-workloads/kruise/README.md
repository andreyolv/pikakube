[← Advanced workloads](../README.md)

# OpenKruise

<https://github.com/openkruise/kruise>
<https://github.com/openkruise/charts>

---

## The problem it solves

Kubernetes' built-in workload controllers have one update semantic: **any change to the pod spec
destroys the pod and creates a new one.** For most applications that is fine and even desirable.
For some it is ruinously expensive — a multi-gigabyte image, a model loaded into memory, a GPU
that takes minutes to initialise, a JIT-warmed runtime, a populated local cache.

OpenKruise adds a parallel set of workload controllers that keep the Kubernetes model but change
the parts that hurt:

| Resource | What it fixes |
|---|---|
| `CloneSet` | a `Deployment` replacement with **in-place update**, per-pod deletion, and rollout control |
| `Advanced StatefulSet` | `StatefulSet` plus in-place update, parallel rollout, and MaxUnavailable |
| `Advanced DaemonSet` | `DaemonSet` plus surging, selective rollout, and pause |
| `SidecarSet` | define a sidecar **once, cluster-wide**, inject it into matching pods, update it **without touching the application container** |
| `BroadcastJob` | run a job **once on every node** — the thing `DaemonSet` cannot express because it never terminates |
| `AdvancedCronJob` | cron that can drive a `BroadcastJob`, not only a `Job` |
| `UnitedDeployment` | one logical workload spread across several node groups or zones with different sizes |
| `WorkloadSpread` | distribute pods of an existing workload across domains by rules |
| `PodUnavailableBudget` | a PDB that also covers **updates**, not only voluntary evictions |
| `ContainerLaunchPriority` | force ordering of container startup inside a pod |
| `ImagePullJob` | pre-pull an image onto nodes before it is needed |
| `ResourceDistribution` | replicate a Secret or ConfigMap across many namespaces |

**The headline is in-place update.** Changing a container image on an existing pod, letting the
kubelet restart that container, keeps the pod name, UID, IP, node, volumes and already-pulled
layers. The rollout stops being *create, warm, drain, repeat* and becomes *restart one container*.

## When to use it

- A workload whose **rollout is dominated by image pull or warm-up** — large images, cached data,
  GPU or model initialisation
- **Sidecars managed centrally**: a mesh proxy or log shipper defined once and upgraded without
  restarting every application that carries it
- A one-shot task that must run **on every node** — node preparation, a driver install, a
  migration — which `BroadcastJob` expresses and `DaemonSet` cannot
- Pods that must be **spread across zones or node pools with different weights**, beyond what
  topology spread constraints handle
- You need a disruption budget that also **covers updates**, not just evictions
- Container start order matters inside a pod and init containers are the wrong shape for it

## When not to use it

- The built-in controllers are working. A `Deployment` that rolls out in seconds gains nothing and
  costs a controller, CRDs and admission webhooks
- **The real problem is a slow start-up or a badly tuned readiness probe.** In-place update hides
  it rather than fixing it, and it is still there on every scale-up and every eviction
- You need to change **resources, node placement, or most of the pod spec** — in-place update
  covers the image and little else; everything else falls back to recreation
- Your tooling only understands built-in kinds. HPA targets, PDBs, dashboards, cost allocation and
  policy engines may not recognise a `CloneSet`
- You cannot accept **admission webhooks in the pod-creation path**. OpenKruise runs mutating and
  validating webhooks; their availability becomes a cluster concern
- A single narrow need, such as leader-worker groups — that is
  [`lws`](../lws/README.md), and it is far smaller

## Notes

The recorded links are the two upstream repositories, and the split between them is the useful
part:

- <https://github.com/openkruise/kruise> — the controllers and CRDs themselves. This is where the
  behaviour of `CloneSet`, `SidecarSet` and in-place update is defined, and where the
  version-to-Kubernetes-version compatibility matrix lives.
- <https://github.com/openkruise/charts> — the Helm charts, kept in a **separate repository** from
  the source. Worth knowing because the chart version and the Kruise version are not the same
  number, and the chart repo is what a `HelmRepository` in this cluster actually points at.

**What is deployed here:** a Flux `HelmRelease` for chart `kruise` version `1.7.3`, sourced from
the `openkruise` `HelmRepository` in `flux-system`, into its own `kruise` namespace, with **default
values** — nothing customised. That is a mapping, not a production configuration: no feature gates
were selected, so the full set of controllers is enabled by default rather than only the ones that
are needed.

Two consequences of that default install worth being aware of before anything depends on it:

1. **The CRDs are cluster-scoped and outlive the release.** Removing the HelmRelease does not
   necessarily remove them, and anything still holding a `CloneSet` becomes an orphan.
2. **The webhooks are installed too.** Once OpenKruise is running, its admission webhooks see pod
   creations across the cluster; that is how `SidecarSet` injection works, and it is why the
   controller's availability matters more than an unused feature set suggests.

The trigger to revisit this from "installed" to "used" is specific: a workload where the rollout
time is dominated by pulling or warming, rather than by the application itself.

---

[← Advanced workloads](../README.md)
