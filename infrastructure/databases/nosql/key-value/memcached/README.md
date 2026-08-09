[← Key-value stores](../README.md)

# Memcached

<https://github.com/memcached/memcached>
<https://github.com/pinterest/pymemcache>

---

## The problem it solves

A cache, and nothing else.

Strings by key, LRU eviction, multi-threaded, **no persistence at all**. That list is complete —
there are no data structures, no replication, no modules, no configuration to speak of.

The simplicity is the argument, and it is stronger than it first appears:

| | Memcached | [Redis](../redis/README.md) |
|---|---|---|
| Data structures | strings only | many |
| Persistence | **none** | RDB, AOF — and see the caveat |
| Threading | **multi-threaded** | single-threaded core |
| Memory efficiency | **slab allocator, very predictable** | more overhead per key |
| Configuration surface | tiny | large |
| Temptation to misuse it | **none** | considerable |

The last row is not a joke. The most common failure in this folder is Redis gradually becoming a
system of record — cache, then sessions, then the only copy of something — because it *can*
persist. Memcached cannot, so nobody tries.

## When to use it

- **the requirement is genuinely a cache**, and the data is rebuildable by definition
- memory efficiency at scale matters; the slab allocator is predictable and low-overhead
- multi-threaded throughput on a single instance is wanted
- the smallest possible operational surface is the goal

## When not to use it

- **data structures are needed** — counters, sorted sets, queues, streams —
  [Redis](../redis/README.md) or [Valkey](../valkey/README.md)
- anything must survive a restart
- pub/sub, or any messaging
- values larger than 1 MB, which is the default item-size limit

## What to know before deploying it

| Concern | Detail |
|---|---|
| **Item size limit** | 1 MB by default; larger values are rejected rather than truncated |
| **No replication** | scale by adding independent nodes; the client shards across them |
| **Client-side sharding** | consistent hashing lives in the client, so all clients must agree |
| Eviction | LRU, always; there is no policy to choose |
| Memory | allocated up front in slabs, which makes usage predictable and fragmentation possible |
| `NetworkPolicy` | no authentication worth the name — SASL exists and is rarely used |

The sharding row is the real architectural difference from Redis Cluster. There is no cluster
protocol: each node is independent, and the client library decides which node a key belongs to.
That is simple and it means every client must use the same hashing configuration, or they will
disagree about where a key lives.

## The honest comparison

For most new work, Redis or Valkey is chosen and that is usually right — the data structures get
used, and having them available costs nothing.

Memcached's case is narrower and real: a very large, purely string-based cache where memory
efficiency and multi-threaded throughput matter, and where the absence of persistence is a
feature because it removes the possibility of the cache quietly becoming important.

## Notes

[pymemcache](https://github.com/pinterest/pymemcache) is recorded alongside it — Pinterest's
Python client, which is the well-maintained option and supports the consistent-hashing setup that
multi-node deployments require.

Mapped rather than deployed here. [Redis](../redis/README.md) is what this platform uses for
caching, and the data structures are part of why. Memcached is catalogued so that the choice is a
choice — and as a reminder that "we need a cache" does not automatically mean "we need something
that can also persist".

---

[← Key-value stores](../README.md)
