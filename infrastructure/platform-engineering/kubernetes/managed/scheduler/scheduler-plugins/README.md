[← Scheduler](../README.md)

# Scheduler plugins

<https://github.com/kubernetes-sigs/scheduler-plugins>

---

## The problem it solves

The default scheduler is built from **plugins** on a documented framework — filter, score, permit,
bind. Anything the built-in set does not do can be added without forking the scheduler.

This `kubernetes-sigs` repository is the collection of out-of-tree plugins: coscheduling (gang
scheduling), capacity scheduling with elastic quota, node resource topology awareness for NUMA,
trimaran for load-aware placement based on real utilisation, and others. It ships both as a library
and as a **pre-built scheduler image** containing them, so using one is a deployment rather than a
build.

## When to use it

- You need one specific capability — usually gang scheduling — without adopting a whole batch platform
- Staying with the upstream scheduler and the `kubernetes-sigs` ecosystem matters
- NUMA-aware placement for latency-sensitive or high-performance workloads
- Load-aware scoring: placing pods by actual node utilisation rather than by requests

## When not to use it

- A complete batch platform is the requirement — [Volcano](../volcano/README.md) or
  [YuniKorn](../yunikorn/README.md) give queues, job CRDs and framework integrations
- Managed clusters where the default scheduler cannot be replaced; run it as a second scheduler
  instead — see [`custom-scheduler/`](../custom-scheduler/README.md)
- If a plugin's version must track the Kubernetes version and nobody will own that
- When affinity or topology spread constraints already express the need

## Notes

Recorded as a link only.

**The trimaran plugins deserve a specific mention**, because they address the flaw described in the
[parent](../README.md): the default scheduler scores nodes on **requested** resources, not on what is
actually being used. Trimaran scores on real utilisation from a metrics provider. On a cluster where
requests are systematically overstated — which is most clusters — that is a materially better
placement decision, and it is the same underlying observation that
[Koordinator](../koordinator/README.md) builds a whole product around.

**Coscheduling** is the plugin most people arrive for: gang scheduling as a plugin, with a `PodGroup`
CRD, keeping the standard scheduler. It is the minimal version of what Volcano provides.

**The version coupling is the practical catch.** These plugins are built against a specific
Kubernetes scheduler version, and the released images are tagged accordingly. Upgrading the cluster
means upgrading the plugin scheduler in step. That is a small ongoing obligation, and it is exactly
the kind of thing that is forgotten until a cluster upgrade leaves a second scheduler running against
an API it no longer understands.

**How to deploy it without replacing the default scheduler:** run the pre-built image as a second
scheduler and set `schedulerName` on the pods that need it — the same mechanism documented in
[`custom-scheduler/`](../custom-scheduler/README.md), which is also the only option on a managed
cluster.

---

[← Scheduler](../README.md)
