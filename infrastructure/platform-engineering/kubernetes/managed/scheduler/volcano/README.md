[← Scheduler](../README.md)

# Volcano

<https://github.com/volcano-sh/volcano>

---

## The problem it solves

Volcano is a batch scheduler that replaces the default one for the workloads assigned to it. It
brings the things batch and ML need and the default scheduler does not have:

- **Gang scheduling** — all pods of a job are placed together, or none are. A distributed training job
  with 8 workers gets 8 slots or waits.
- **Queues with weights and hierarchy** — teams share a pool according to a policy rather than
  first-come-first-served.
- **Job-level lifecycle** — retries, dependencies between tasks, and job states, expressed in a
  `Job` CRD of its own.
- **Fair-share and priority preemption** designed around jobs rather than services.

It is a CNCF project, originating from Huawei's work on Kubernetes batch, and it is the most
established option of its kind.

## When to use it

- Distributed training, MPI, Spark on Kubernetes — anything all-or-nothing
- Several teams competing for a GPU pool, needing a defined sharing policy
- Job dependencies and retry semantics that Kubernetes `Job` does not express
- ML frameworks that integrate with it directly, which many do

## When not to use it

- Long-running services; the default scheduler is built for those and does them better
- Only gang scheduling is needed and you would rather not replace the scheduler — [Kueue](../kueue/README.md) queues without replacing it
- Small clusters where FIFO is genuinely fine
- Without a plan for two schedulers coexisting — see below

## Notes

**Chart** `volcano` from the project's Helm repository, with a namespace manifest and empty values.
Recorded as a link only.

**Why gang scheduling is not a nicety.** Without it, the default scheduler places pods
independently. A job needing 8 GPUs on a cluster with 6 free gets 6 pods running and 2 pending — 6
GPUs consumed, no work done, indefinitely. Two such jobs deadlock each other completely: each holds
part of what the other needs, and neither can proceed. Gang scheduling makes the placement atomic, so
the job waits instead of half-starting.

**Coexistence with the default scheduler** is the operational detail to plan. Volcano schedules pods
that specify its `schedulerName` (or that belong to its `Job` CRD); everything else continues to use
the default. Two schedulers making independent decisions about the same nodes can race — both may
consider the same free capacity, and one loses. In practice this is managed by keeping batch on
dedicated node pools, which is worth doing anyway for GPUs.

**The `Job` CRD is not the Kubernetes `Job`.** Volcano introduces its own, with task groups,
per-task replicas and lifecycle policies. Adopting Volcano means workloads are written against it,
which is a real coupling — the reason [Kueue](../kueue/README.md) exists as a more conservative
alternative that keeps the standard `Job`.

The natural comparison set is [YuniKorn](../yunikorn/README.md) — hierarchical queues from the Hadoop
tradition — and [Koordinator](../koordinator/README.md), which focuses on co-locating batch with
latency-sensitive services rather than on batch alone.

---

[← Scheduler](../README.md)
