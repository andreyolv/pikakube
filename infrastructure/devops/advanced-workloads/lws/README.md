[← Advanced workloads](../README.md)

# LWS — LeaderWorkerSet

<https://github.com/kubernetes-sigs/lws>
<https://github.com/kubernetes-sigs/lws/tree/main/docs/examples>

---

## The problem it solves

Kubernetes has no concept of a **group of pods as one replica**. `Deployment` scales identical
pods; `StatefulSet` scales identified pods in order. Neither can say *"one replica of this
workload is four pods that live and die together"*.

That is exactly the shape of **multi-node inference**. When a model is too large for a single node
and is sharded across machines with tensor or pipeline parallelism, the serving unit is a leader
that receives requests and coordinates, plus N workers holding the remaining shards. The group
has properties nothing built-in provides:

| Requirement | What built-in controllers do instead |
|---|---|
| The **group** is the unit of scale | they scale individual pods |
| Readiness is all-or-nothing | pods become ready independently, so the group serves before it can |
| A dead member breaks the group | the pod is replaced, but the group is not repaired or restarted |
| Rolling updates must be per group | pod-by-pod leaves mixed-version shards mid-inference |
| Members should be co-located | no notion of "these pods belong on the same fast interconnect" |

`LeaderWorkerSet` makes the group first-class. `spec.replicas` counts **groups**;
`spec.leaderWorkerTemplate.size` says how many pods form one group. Restart policy, readiness
gating, rolling update and topology-aware placement all operate at group granularity.

It is a Kubernetes SIG project (`kubernetes-sigs/lws`), which matters for the same reason it
always does: it is the community's answer to this problem rather than one vendor's.

## When to use it

- **Serving a model that does not fit on one node** — the case the project was built for, and the
  one that connects this folder to `infrastructure/ai/llm/` (vLLM in particular deploys in exactly
  this leader/worker shape)
- Any workload where **a failure in one member invalidates the whole group** and the correct
  recovery is restarting the group, not the pod
- A **sharded index or cache with a coordinator**, where partial availability is worse than being
  unavailable
- MPI-style or gang-scheduled batch work that needs all ranks running simultaneously
- You want the group **placed on shared topology** — same rack, same high-bandwidth interconnect

## When not to use it

- The workload is a set of independent replicas. That is a `Deployment`, and adding LWS buys
  nothing
- The model **fits on one node**. Single-node serving with a `Deployment` or `StatefulSet` is
  simpler in every dimension — reach for LWS only when it genuinely does not fit
- You need general workload extensions — in-place updates, sidecar management, spread rules. That
  is [`kruise`](../kruise/README.md); LWS is deliberately narrow and does one thing
- You expect LWS to shard the model. **It does not.** The serving engine performs the sharding;
  LWS only guarantees the pods exist together, become ready together and restart together
- The batch scheduler already gang-schedules for you and the workload is a job rather than a
  service

## Notes

The two recorded links:

- <https://github.com/kubernetes-sigs/lws> — the controller and the `LeaderWorkerSet` CRD.
- <https://github.com/kubernetes-sigs/lws/tree/main/docs/examples> — the upstream examples
  directory. This is the practically important one: the multi-node **vLLM** deployments live
  there, and they are the reference for what a real leader/worker inference group looks like, as
  opposed to the trivial one committed here.

**What is deployed here:** a Flux `HelmRelease` in its own `lws` namespace, with two details worth
naming.

**The chart comes from an `OCIRepository`, not a `HelmRepository`.** LWS publishes its chart as an
OCI artifact at `oci://registry.k8s.io/lws/charts/lws`, tag `0.6.1`, so the HelmRelease uses
`chartRef` rather than the usual `chart.spec` + `HelmRepository` pair. That is the pattern every
`registry.k8s.io`-hosted chart needs, and it is the reason this manifest looks different from its
neighbours. Values are left at defaults.

**The committed example is nginx, not a model.** `example/leaderworkerset.yaml` is the upstream
sample: `replicas: 3` with `leaderWorkerTemplate.size: 4`, running
`nginxinc/nginx-unprivileged:1.27` — twelve pods in three groups of four. It proves the controller
reconciles and shows the two fields that define the topology, and it deliberately demonstrates
nothing about inference. Reading it, the thing to take away is the arithmetic:
**`replicas` × `size` = total pods**, and `replicas` is the number the group-level operations act
on.

The gap between that example and the real use is the point. LWS here is a **mapped primitive**:
installed, understood, waiting for the workload that needs it. The trigger to make it real is a
model under `infrastructure/ai/llm/` that does not fit on a single node — at which point the
upstream vLLM examples above are the starting point, not this one.

---

[← Advanced workloads](../README.md)
