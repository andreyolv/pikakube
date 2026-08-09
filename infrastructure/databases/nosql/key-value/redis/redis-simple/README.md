[← Redis](../README.md)

# redis-simple

The smallest thing that runs: a Deployment and a Service.

---

## What this is

One Redis pod, no persistence, no replication, no chart. Two manifests —
[`deployment.yaml`](deployment.yaml) and [`service.yaml`](service.yaml) — and that is the whole
deployment.

It exists to make the point that for a **cache**, this is frequently sufficient. Redis holds
data that is by definition rebuildable; a pod that restarts empty is a cold cache, not an
incident.

## When this shape fits

- **local development**, where a cache is needed and nothing about it matters
- a genuine cache: sessions, rate limits, memoised query results
- a test fixture
- demonstrating something, where a chart's configuration surface is noise

## When it does not

- anything whose loss is a problem — this has **no persistence** and no replication
- production, where the failure of one pod should not empty the cache — see
  [`redis/`](../redis/README.md) for the chart, or
  [`redis-operator/`](../redis-operator/README.md)
- clustering or sharding — [`redis-cluster/`](../redis-cluster/README.md)

## The one setting to add anyway

Even here, `maxmemory` is worth setting **below the container's memory limit**, with an eviction
policy.

Without it the pod is OOM-killed under memory pressure rather than evicting keys — which turns
"the cache is full" into "the pod restarted", and the database behind it receives the full load
it was shielded from. That failure is the same whether the deployment is two manifests or a chart
with two hundred values, and it is covered in
[`../../README.md`](../../README.md#6-running-them-on-kubernetes).

## Notes

Kept as the minimal reference alongside the three progressively more capable options in this
folder:

| Option | Adds |
|---|---|
| **redis-simple** | nothing — a pod and a Service |
| [`redis/`](../redis/README.md) | the Helm chart, persistence, replication, the Python client examples |
| [`redis-operator/`](../redis-operator/README.md) | Redis as a custom resource, with failover |
| [`redis-cluster/`](../redis-cluster/README.md) | sharding across nodes |

Reading them in that order is the useful path, because each step adds a specific capability and a
specific cost — and for a cache, stopping at the first is a legitimate answer more often than the
existence of the other three suggests.

---

[← Redis](../README.md)
