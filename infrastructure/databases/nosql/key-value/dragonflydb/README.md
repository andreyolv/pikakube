[← Key-value stores](../README.md)

# DragonflyDB

<https://github.com/dragonflydb/dragonfly>

---

## The problem it solves

Redis is single-threaded at its core. One instance uses one core, so growing past it means
clustering — which constrains multi-key operations and the data model for every client. See
[`redis-cluster/`](../redis/redis-cluster/README.md).

DragonflyDB is a **from-scratch rewrite**, not a fork: multi-threaded, shared-nothing internally,
and designed to use a whole machine. It speaks the Redis protocol, so clients connect unchanged.

| | Redis | DragonflyDB |
|---|---|---|
| Threading | single-threaded core | **multi-threaded** |
| Scaling | out, via cluster | **up, on one machine** |
| Protocol | — | Redis-compatible |
| Memory efficiency | baseline | better, per their design |
| Snapshotting | fork-based, with a memory spike | point-in-time, without the spike |
| Licence | RSALv2 / SSPL / AGPL | **BSL** |
| Maturity | two decades | young |

## The architectural argument

Worth stating because it is the whole point.

The conventional answer to "Redis is at 100% of one core" is Redis Cluster: shard the keyspace
across nodes. That works and it moves a constraint into the application — multi-key operations
must stay within a slot, hash tags become part of the key design, and every client must be
cluster-aware.

DragonflyDB's position is that this is solving the wrong problem. A modern server has many cores;
a single-threaded database uses one of them. Using all of them removes the need to shard for a
very wide range of workloads, and **not sharding is a simpler system**.

The snapshotting difference is a related and underrated benefit. Redis forks to write a snapshot,
which can double memory usage momentarily and is a well-known cause of OOM kills on a
tightly-sized container. DragonflyDB's snapshot algorithm avoids the fork.

## When to use it

- Redis is **measurably** CPU-bound on one core, and clustering is the alternative
- a large dataset should fit on one machine rather than be sharded across several
- the fork-related memory spike during snapshots has caused real problems
- vertical scale is preferred to the operational surface of a cluster

## When not to use it

- **the BSL licence** is a constraint — this is the main reason to decline it
- Redis is not actually the bottleneck, which it usually is not
- production dependence on a young project with a smaller community
- Redis modules are in use; compatibility is with core Redis
- the ecosystem matters — tooling, answers, and people who have operated it

## The licence, plainly

Business Source License. Not open source by the OSI definition: it restricts offering the software
as a competing managed service, and converts to Apache after a period.

For running it internally that is usually acceptable. For a platform that might be offered to
others it needs checking, and it is the single most common reason teams choose
[Valkey](../valkey/README.md) instead — which is BSD, and answers the licence question rather
than the threading one.

## Notes

Mapped as the vertical-scale answer. The decision tree in
[`../README.md`](../README.md#4-decision-tree) puts it at the end deliberately: the question
*"does one core become the limit?"* is one most deployments answer no to, and reaching for a
rewrite before measuring is how platforms acquire young dependencies for no benefit.

For this cluster it is not relevant — Redis here is a cache well within one core. It is
catalogued because the alternative it competes with is Redis Cluster, and Redis Cluster is a
significantly worse thing to adopt casually.

---

[← Key-value stores](../README.md)
