[← Redis](../README.md)

# redis-operator

<https://github.com/OT-CONTAINER-KIT/redis-operator>

---

## What it adds over the chart

The [Helm deployment](../redis/README.md) gives you a Redis. The operator makes Redis instances
**Kubernetes resources**:

| CRD | What it declares |
|---|---|
| `Redis` | a standalone instance |
| `RedisReplication` | a primary with replicas |
| `RedisSentinel` | Sentinel-based automatic failover |
| `RedisCluster` | a sharded cluster |

That matters when there is more than one. Creating a cache for a new service becomes a small
manifest rather than another `HelmRelease` with a copy of the same values — and failover,
reconfiguration and rolling upgrades are handled by a controller rather than by whoever is
available.

## When to use it

- **several Redis instances**, created and destroyed as services come and go
- automatic failover is required, and assembling Sentinel by hand is unattractive
- teams should be able to request a cache without editing platform values files
- the topology may change — standalone today, replicated later

## When not to use it

- **one Redis, with stable configuration** — the [chart](../redis/README.md) is fewer moving
  parts
- a development cache — [`redis-simple/`](../redis-simple/README.md)
- running a controller for a single cache is more machinery than the problem deserves

## The trade

An operator is a controller running permanently, with CRDs, RBAC and its own upgrade path. For
one instance that is a poor exchange; for ten it is obviously the right one.

The threshold is roughly where copying values files starts to feel like a pattern.

## What still has to be decided

The operator manages the topology. It does not decide the two settings that determine behaviour
under pressure, and they remain the platform's responsibility:

| Setting | Why |
|---|---|
| **`maxmemory`, below the container limit** | otherwise the pod is OOM-killed rather than evicting keys |
| **Eviction policy** | keys assumed permanent are discarded, or writes fail — both are choices |

See [`../../README.md`](../../README.md#6-running-them-on-kubernetes). An operator makes it
easier to create many Redis instances with the same misconfiguration.

## Notes

[`example/redis.yaml`](example/redis.yaml) is the minimal custom resource, which is the useful
thing to read first — it shows what replaces the chart's values.

The alternative worth naming: **Valkey**. The licence position in
[`../../README.md`](../../README.md#2-the-licence-split-which-is-why-this-folder-is-crowded)
applies here too, and there are operators for Valkey with the same shape. Since clients cannot
tell the two apart, the migration cost is close to zero and the licence question stops being one.

---

[← Redis](../README.md)
