[← NewSQL](../README.md)

# Vitess

<https://github.com/vitessio/vitess>

---

## The problem it solves

Scaling MySQL **without leaving MySQL**.

Everything else in [`newsql/`](../README.md) is a new database that speaks a familiar protocol.
Vitess is different in kind: the shards are **real MySQL instances**, with a routing and topology
layer in front of them.

| | A natively distributed engine | Vitess |
|---|---|---|
| The database is | built distributed from the storage up | **actual MySQL**, sharded |
| Backups, tooling, expertise | new | **still applies** |
| Compatibility | a wire protocol, with gaps | **MySQL, including its quirks** |
| Migration from an existing estate | a migration | comparatively incremental |
| Transactions | distributed, across any rows | local to a shard by default |

That is the pragmatic path, and it is routinely overlooked in favour of the more exciting option.
YouTube ran on Vitess, which is the answer to whether it is real. It is a CNCF graduated project.

| Component | Role |
|---|---|
| **VTGate** | the proxy applications connect to; it routes queries to shards |
| **VTTablet** | sits beside each MySQL instance, managing it |
| **Topology service** | etcd or ZooKeeper, holding the cluster's shape |
| VSchema | the sharding configuration — which key splits which table |

## When to use it

- an **existing MySQL estate** that has outgrown one machine, where leaving MySQL is unacceptable
- the operational knowledge, backup tooling and monitoring around MySQL are worth preserving
- sharding is the actual requirement, and it should be incremental rather than a migration
- online resharding without downtime matters — this is one of Vitess's strongest features

## When not to use it

- **greenfield** — a natively distributed engine is simpler than MySQL plus a routing layer
- PostgreSQL is the engine — nothing here applies
- **cross-shard transactions are common** — see below
- the operational surface is a concern: this is MySQL *plus* VTGate *plus* VTTablet *plus* a
  topology service

## The constraint: the sharding key

The same decision that dominates [`nosql/column/`](../../../nosql/column/README.md), in a
different form.

Each table is assigned a sharding key in the VSchema. Queries that specify it are routed to one
shard and behave like ordinary MySQL. Queries that do not are **scatter-gather** — sent to every
shard and merged — which works and does not scale.

| Query | Behaviour |
|---|---|
| Filters on the sharding key | one shard; fast |
| Does not | **every shard**, results merged |
| Joins within a shard | ordinary MySQL |
| **Joins across shards** | limited, and expensive |
| Transactions within a shard | ordinary MySQL |
| **Transactions across shards** | two-phase commit, opt-in, with real cost |

Vitess mitigates this with **table sequences** and **materialised views**, and the fundamental
requirement stands: related data must share a sharding key, or the queries that join it will be
expensive.

Choosing that key is the design decision, and unlike Cassandra's partition key, Vitess can
**reshard online** — which makes it revisable at operational cost rather than permanent.

## Notes

Nothing here is deployed, and on a single Kind cluster nothing should be.

**This is the interesting entry in [`newsql/`](../README.md) for this platform**, and the reason
is structural: MySQL appears in this repository as a **source system** — see
[`sql/mysql/`](../../../sql/mysql/README.md) — and Vitess is the only option that scales it
without it ceasing to be MySQL.

That matters because a data platform reading from MySQL depends on MySQL's own mechanisms:
row-based binlogs, CDC connectors, and logical dumps. A migration to a MySQL-*compatible* engine
puts all of that in question; sharding with Vitess does not, because the shards are still MySQL
emitting real binlogs.

It is the answer to a question nobody here is asking yet, and the right answer if they ever do.

---

[← NewSQL](../README.md)
