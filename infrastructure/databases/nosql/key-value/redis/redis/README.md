[← Redis](../README.md)

# redis — the Helm deployment

<https://github.com/redis/redis>
<https://github.com/redis/redis-py>

---

## What this shape is

Redis deployed from a Helm chart, as a `HelmRelease` with its values in Git — the standard
GitOps deployment, and the one to use when a cache needs to be configured rather than merely to
exist.

What it adds over [`redis-simple/`](../redis-simple/README.md):

| Capability | Detail |
|---|---|
| **Persistence** | a PVC, and a choice of RDB, AOF or neither |
| **Replication** | a primary with replicas, and Sentinel for failover |
| Authentication | a password, rather than an open port |
| Metrics | an exporter for Prometheus |
| Resource configuration | `maxmemory` and the eviction policy as values |

## When to use it

- a **single Redis** whose configuration matters — persistence, memory limits, authentication
- GitOps, where the chart is a `HelmRelease` and the values are reviewed in a pull request
- you would rather not operate a controller for one cache

## When not to use it

- many Redis instances, created and destroyed frequently —
  [`redis-operator/`](../redis-operator/README.md) makes them resources
- sharding across nodes — [`redis-cluster/`](../redis-cluster/README.md)
- a throwaway cache in development — [`redis-simple/`](../redis-simple/README.md) is two files

## What to set deliberately

| Setting | Why |
|---|---|
| **`maxmemory`, below the container limit** | otherwise the pod is OOM-killed instead of evicting — the most common production failure in this folder |
| **Eviction policy** | the default surprises people; `allkeys-lru` for a cache, `noeviction` if writes must fail instead |
| Persistence | decide whether it exists at all — a cache does not need a PVC |
| Authentication | there is no meaningful default, and in-cluster reachable means reachable by anything in the cluster |
| `NetworkPolicy` | the other half of the same point |

The first two are covered at length in
[`../../README.md`](../../README.md#5-persistence-and-why-it-is-not-durability), and they are the
settings that separate a cache that degrades gracefully from one that takes the database down
with it.

## The client examples

Kept alongside the manifests, which is unusual in this repository and useful:

| File | What it shows |
|---|---|
| [`redis_connection.py`](redis_connection.py) | connecting with `redis-py` |
| [`redis_get.py`](redis_get.py) | reading values |
| [`redis.ipynb`](redis.ipynb) | the same, interactively |

[redis-py](https://github.com/redis/redis-py) is the reference Python client, and it works
unchanged against [Valkey](../../valkey/README.md) — which is what makes the licence question in
[`../../README.md`](../../README.md#2-the-licence-split-which-is-why-this-folder-is-crowded) a
cheap one to act on.

## Notes

Also recorded in the original notes for this folder:

| Project | What it is |
|---|---|
| [redis-stack](https://github.com/redis-stack/redis-stack) | Redis plus the modules — JSON, search, time-series, probabilistic structures |
| [AnotherRedisDesktopManager](https://github.com/qishibo/AnotherRedisDesktopManager) | a desktop GUI for inspecting keys |

**redis-stack** is worth knowing about before reaching for a second database: RedisJSON and
RediSearch turn Redis into something that can store and query documents, which occasionally
removes a requirement. It also moves Redis further from "a cache everyone treats as ephemeral",
which is the trap in [`../../README.md`](../../README.md#5-persistence-and-why-it-is-not-durability).

This is the deployment with real history in the platform — Redis is the one tool in
[`nosql/`](../../../README.md) genuinely used in the platform sense here, for caching and
ephemeral state.

---

[← Redis](../README.md)
