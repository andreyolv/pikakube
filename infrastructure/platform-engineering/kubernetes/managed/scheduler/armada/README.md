[← Scheduler](../README.md)

# Armada

<https://github.com/armadaproject/armada>
<https://github.com/armadaproject/armada-operator>

---

## The problem it solves

Armada is a **multi-cluster batch queue**. Jobs are submitted to Armada rather than to a cluster;
Armada holds them in queues with fair-share policies, and dispatches them to whichever of several
Kubernetes clusters has capacity.

That framing solves a problem the other schedulers here do not touch. Volcano, YuniKorn and Kueue all
operate within one cluster. When the workload is millions of short jobs across dozens of clusters, the
bottleneck stops being placement and becomes throughput and queueing — and a single cluster's API
server becomes the limit long before its nodes do.

It came out of finance — G-Research built it for large-scale quantitative computation — and the scale
it targets is unusual.

## When to use it

- Very high job throughput, beyond what one cluster's API server sustains
- Many clusters forming one logical compute pool
- Fair-share queueing across teams at that scale
- Long-running batch estates where the queue itself is the system

## When not to use it

- One cluster — [Volcano](../volcano/README.md), [YuniKorn](../yunikorn/README.md) or
  [Kueue](../kueue/README.md) are all better fits
- Interactive or latency-sensitive workloads; this is a batch system throughout
- Small job volumes; the operational weight is substantial
- If multi-cluster is not already solved for networking, identity and observability —
  see [`multi-cluster/`](../../multi-cluster/README.md)

## Notes

**Two projects recorded**, which is the useful distinction:

- **`armada`** — the system itself: the server, the queues, the executors that run in each cluster
- **`armada-operator`** — a Kubernetes operator for installing and managing Armada, so its components
  are declared as custom resources rather than assembled by hand

Installed here with a `HelmRelease`, a `HelmRepository` and a namespace manifest, values empty.
Recorded as links only.

**Its architecture is the reason it exists**, and it is worth stating because it explains why the
other tools cannot simply be scaled up: Armada's queue lives **outside** Kubernetes. Jobs are
submitted to Armada's own API, held in its own store, and only become Kubernetes objects at the moment
an executor in some cluster is ready to run them. A cluster never holds a backlog.

That is precisely the inversion needed at high throughput. Kueue, by contrast, suspends `Job` objects
that already exist in the cluster — elegant, and it means the backlog is API-server-resident. At tens
of thousands of queued jobs that difference stops being architectural taste.

**The trade** is equally clear: jobs are submitted to Armada, not with `kubectl`. Workloads are
written against its API, its client and its concepts. That coupling is much deeper than choosing a
`schedulerName`, and it is only worth accepting at the scale it was designed for.

Filed here as a bookmark for a category — very-large-scale batch — that nothing in this repository
approaches.

---

[← Scheduler](../README.md)
