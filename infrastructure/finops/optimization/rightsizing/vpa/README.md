[← Right-sizing](../README.md)

# VPA — Vertical Pod Autoscaler

<https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler>
<https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/installation.md>

---

## The problem it solves

Someone picked the CPU and memory requests once, from a template, and nothing has revisited them
since. The workload is either paying for capacity it never touches, or quietly running on borrowed
slack that disappears the first time the cluster gets packed tightly.

VPA is the Kubernetes-native answer: three controllers that observe actual container usage, produce
a recommended request per container, and — optionally — apply it.

| Component | Job |
|---|---|
| **Recommender** | watches usage, maintains history, computes target / lower bound / upper bound |
| **Updater** | evicts pods whose resources are outside the recommended range, so they come back resized |
| **Admission controller** | rewrites the pod's resources at admission time |

Its second role is the more important one: **VPA's recommender is the substrate other tools build
on.** [Goldilocks](../goldilocks/README.md) is a UI over these recommendations. It is the reference
implementation everything else in this folder is compared against.

A `VerticalPodAutoscaler` object targets a workload and picks a mode:

| `updateMode` | Behaviour |
|---|---|
| `Off` | **recommendations only** — nothing is changed |
| `Initial` | requests applied at pod creation, never afterwards |
| `Auto` / `Recreate` | pods are evicted and recreated to apply new requests |

## When to use it

- **`Off` mode as a recommendation engine** — the safe, generally correct default, and enough on its
  own to drive pull requests
- stateless Deployments with several replicas and a PodDisruptionBudget, where `Auto` mode's
  restarts are absorbed
- workloads with genuinely variable demand that nobody is going to keep tuning by hand
- as the engine underneath [Goldilocks](../goldilocks/README.md)

## When not to use it

- **alongside an HPA on the same resource** — both react to CPU usage and each changes the other's
  input; see [`rightsizing/`](../README.md) section 5
- single-replica or stateful workloads in `Auto` mode: resizing means restarting the pod
- **against GitOps, without a decision.** A mutating VPA and a manifest in Git disagree permanently,
  and every later debugging session starts with working out which number is real
- as the only source of truth for a workload with a seasonal or startup peak that its window never saw
- when a CLI report would answer the question — [KRR](../krr/README.md) installs nothing

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/installation.md>**
— the official installation document. Worth reading rather than going straight to a chart, because
it is where the CRDs, the three components and the certificate requirements of the admission webhook
are laid out. The admission controller is a webhook in the pod-creation path, which is the part
people underestimate: if it is broken or unreachable, pod creation is affected cluster-wide.

**<https://ttanay.github.io/blog/vpa-algorithm>** — a blog post reverse-engineering the VPA
recommendation algorithm from the source. The short version: the recommender keeps **decaying
histograms** of observed CPU and memory usage per container — recent samples weighted more heavily
than old ones — and derives a target from a high percentile of that distribution, plus lower and
upper bounds used to decide whether a running pod is far enough out of range to be worth evicting.
Memory is treated more conservatively than CPU, which is the asymmetry in
[`rightsizing/`](../README.md) section 2.

This post exists because that behaviour is **not officially documented**, which is the next note.

**<https://github.com/kubernetes/autoscaler/issues/2747#issuecomment-616037197>** — *"VPA — Document
the current recommendation algorithm"*, opened January 2020 and **still open**. The linked comment is
one of the better explanations available. The significance is not the issue itself but what it
implies: the most widely used right-sizing engine in Kubernetes has had its algorithm undocumented
for years, so understanding why it recommended a particular number means reading the source or a
third-party blog post. Factor that into how much you trust it unattended — and it is a fair part of
what the commercial tools in this folder are selling against.

**"not ready for production use" —
<https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler/charts/vertical-pod-autoscaler>**
The upstream project's own Helm chart carries that warning. It is the reason this repository uses
the **Fairwinds** chart instead, which is maintained alongside [Goldilocks](../goldilocks/README.md)
and is the de facto community route. Worth knowing before someone "fixes" the source to point at
upstream.

**"not support oci repository" — <https://github.com/FairwindsOps/charts/issues/1817>** — *"Support
OCI artifact for the helm charts"*, opened May 2026, **still open**. Fairwinds publishes only over
classic HTTP chart repositories, not as OCI artefacts. That matters on this platform because Flux
handles OCI sources better — `OCIRepository` supports digest pinning and verification in a way an
index-based `HelmRepository` does not — and several other releases here (Karpenter, StormForge) are
already OCI. Both Fairwinds charts in this folder therefore need the older `HelmRepository` shape,
and the inconsistency is upstream's, not a mistake here.

**On the deployment here.** Flux, Fairwinds chart `vpa` version **4.7.2** from
`https://charts.fairwinds.com/stable/`, into `kube-system`.

The block that matters is commented out:

```yaml
#recommender:
#  extraArgs:
#    storage: prometheus
#    prometheus-address: http://kube-prometheus-stack-prometheus.monitoring.svc.cluster.local:9090
```

By default the recommender keeps history in memory with periodic checkpoints, so a restart costs it
most of its context and recommendations resume from a short, cold window — the exact failure that
produces a confident recommendation from a period that never contained the peak. Pointing it at the
platform's existing Prometheus gives it real history immediately and makes it restart-tolerant. This
should be enabled.

**The example is a good one.** `example/` deploys the upstream `hamster` workload — a container that
deliberately burns CPU in a loop — with a `VerticalPodAutoscaler` in `updateMode: Auto` and a
`resourcePolicy` bounded by `minAllowed` 100m/50Mi and `maxAllowed` 1 CPU/500Mi.

Two things worth generalising from it:

1. **Bound an enforcing VPA.** `minAllowed` is the floor that protects a workload whose steady state
   is far below its startup peak; `maxAllowed` is what stops one pathological container from
   requesting a whole node.
2. `controlledResources: ["cpu", "memory"]` is explicit. Restricting it to `["memory"]` is the
   documented way to run VPA next to an HPA on CPU without the two fighting.

---

[← Right-sizing](../README.md)
