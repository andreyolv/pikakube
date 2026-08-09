[← Scheduler](../README.md)

# YuniKorn

<https://github.com/apache/yunikorn-core>
<https://github.com/apache/yunikorn-k8shim>
<https://github.com/apache/yunikorn-k8shim/tree/master/deployments/examples>

---

## The problem it solves

Apache YuniKorn brings the **hierarchical queue** model from the Hadoop/YARN world to Kubernetes. The
cluster's capacity is divided into a tree of queues — `root.engineering.ml`,
`root.engineering.ci`, `root.analytics` — each with guaranteed capacity, maximum capacity and a
sharing policy. Work submitted to a queue is scheduled within its share, and idle capacity can be
borrowed by other queues and reclaimed when the owner needs it.

It also supports gang scheduling, so it covers the all-or-nothing case as well as the fair-share one.

## When to use it

- Many teams sharing one cluster with a defined, hierarchical capacity policy
- Organisations coming from YARN, where the queue model is already understood
- Mixed batch and service workloads needing consistent resource governance
- Borrowable quota: let teams use idle capacity without giving it away permanently

## When not to use it

- A single team; a queue hierarchy of one is pure overhead
- Where namespace `ResourceQuota` already expresses what you need
- Only gang scheduling is needed — [Volcano](../volcano/README.md) or [Kueue](../kueue/README.md) are more direct
- Without understanding the queue model, which is the whole product and takes real study

## Notes

**Two repositories, and the split matters:**

- **`yunikorn-core`** — the scheduling engine, which is Kubernetes-agnostic. Queues, hierarchies,
  fair-share and preemption logic live here.
- **`yunikorn-k8shim`** — the Kubernetes integration: watches pods, speaks to the API server, binds
  pods to nodes.

That separation is a deliberate design choice with a practical consequence: **the documentation and
issues are split across two projects**, and a problem is frequently in the shim rather than in the
core. Knowing which to search saves time.

**Chart** from the project's Helm repository, with a namespace manifest, plus a committed
`examples/pod.yaml`. The upstream example set is recorded at
<https://github.com/apache/yunikorn-k8shim/tree/master/deployments/examples>, which is the right
starting point — the queue configuration is the hard part and reading working examples is faster than
reading the reference.

**How queues are assigned** is the thing to understand first: a pod carries labels or annotations
naming its application and its queue, and YuniKorn's placement rules can also derive a queue from the
namespace or the user. The last of those is what makes adoption possible without editing every
workload — the same idea as the Gatekeeper mutation in
[`custom-scheduler/`](../custom-scheduler/README.md), reached from a different direction.

**Where it differs from Volcano**, since they are the two obvious alternatives: Volcano is
job-centric, with its own `Job` CRD and strong ML framework integration. YuniKorn is
capacity-centric — the queue tree is the primary object, and jobs are things that flow through it.
For "our teams argue about who gets the GPUs", YuniKorn's model is the more direct answer. For
"our training jobs need atomic placement", Volcano's is.

---

[← Scheduler](../README.md)
