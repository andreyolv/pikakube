[← Key-value stores](../README.md)

# Redis

<https://github.com/redis/redis>
<https://github.com/redis/redis-py>

Deployment shapes: [`redis-simple/`](redis-simple/README.md) — a pod and a Service ·
[`redis/`](redis/README.md) — the Helm chart ·
[`redis-operator/`](redis-operator/README.md) — Redis as a custom resource ·
[`redis-cluster/`](redis-cluster/README.md) — sharded

---

## The problem it solves

An in-memory data structure server: strings, hashes, lists, sets, sorted sets and streams, with
sub-millisecond access and atomic operations over all of them.

The distinction from a cache like [Memcached](../memcached/README.md) is the data structures. A
rate limiter is an atomic `INCR` with a TTL. A leaderboard is a sorted set. A work queue is a list
or a stream. Each of those is one command rather than a read-modify-write cycle the application
has to make safe.

| Structure | What it is used for |
|---|---|
| String | cache entries, counters |
| Hash | an object stored by field |
| List | queues, recent-items |
| **Sorted set** | leaderboards, priority queues, time-ordered indexes |
| Set | membership, deduplication |
| **Stream** | an append-only log with consumer groups |
| Bitmap, HyperLogLog | presence and cardinality, very cheaply |

## When to use it

- **caching** — the primary case, and the one it is unambiguously right for
- sessions and other ephemeral state
- rate limiting, locks and leases, where atomicity matters
- queues and pub/sub where a full broker is disproportionate
- anything on the structure list above that is awkward in SQL

## When not to use it

- **as a system of record** — persistence is best-effort, and everyone treats it as ephemeral.
  See [`../README.md`](../README.md#5-persistence-and-why-it-is-not-durability)
- large values, which block the single-threaded event loop for every other client
- correctness-critical distributed locks —
  [etcd](../../../distributed/key-value/etcd/README.md) is built for that
- new deployments where the licence matters — [Valkey](../valkey/README.md) is the BSD drop-in

## The licence, in one paragraph

Redis moved away from BSD in 2024 (RSALv2/SSPL) and added AGPL as an option in 2025. The Linux
Foundation fork, [Valkey](../valkey/README.md), carries the original BSD licence and most of the
original maintainers, backed by AWS, Google and Oracle.

For anything new, Valkey is the safe default and the migration cost is close to zero — clients
cannot tell them apart. See
[`../README.md`](../README.md#2-the-licence-split-which-is-why-this-folder-is-crowded).

## The two settings that decide production behaviour

Stated here because they are the most common cause of a real incident in this folder:

| Setting | Why |
|---|---|
| **`maxmemory`, below the container limit** | otherwise the kernel OOM-kills the pod before eviction ever runs — the cache goes cold and the database receives the full load it was shielded from |
| **`maxmemory-policy`** | with an eviction policy, keys somebody assumed permanent get discarded; with `noeviction`, writes fail instead. Both are defensible; the default is rarely chosen |

## The four deployment shapes

| Shape | Use |
|---|---|
| [`redis-simple/`](redis-simple/README.md) | development — two manifests, no persistence |
| [`redis/`](redis/README.md) | **one Redis, configured properly** — the usual answer |
| [`redis-operator/`](redis-operator/README.md) | many instances, with automatic failover |
| [`redis-cluster/`](redis-cluster/README.md) | one dataset too large for one node — and it constrains every client |

The last is worth a warning that bears repeating: **Redis Cluster is for sharding, not for
availability.** Replicas plus Sentinel give failover without constraining multi-key operations.

## Notes

Also recorded in the original notes:

| Project | What it is |
|---|---|
| [redis-py](https://github.com/redis/redis-py) | the reference Python client — works unchanged against Valkey |
| [redis-stack](https://github.com/redis-stack/redis-stack) | Redis plus modules — JSON, search, time-series, probabilistic structures |
| [AnotherRedisDesktopManager](https://github.com/qishibo/AnotherRedisDesktopManager) | a desktop GUI for inspecting keys |
| [OT-CONTAINER-KIT/redis-operator](https://github.com/OT-CONTAINER-KIT/redis-operator) | the operator used in [`redis-operator/`](redis-operator/README.md) |

**redis-stack** is worth knowing before adopting a second database: RedisJSON and RediSearch turn
Redis into something that stores and queries documents. It also pulls Redis further from "a cache
everyone treats as ephemeral", which is exactly the drift that ends with a cache holding the only
copy of something.

Redis is the one tool in [`nosql/`](../../README.md) genuinely used in the platform sense here —
caching and ephemeral state, which is what the category is for.

---

[← Key-value stores](../README.md)
