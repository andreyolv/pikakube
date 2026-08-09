[← Distributed key-value stores](../README.md)

# TiKV

<https://github.com/tikv/tikv>

---

## What it is

A distributed transactional key-value store, written in Rust, and a **CNCF graduated project**.

It is the storage layer [TiDB](../../newsql/tidb/README.md) is built on — TiDB is a SQL engine,
and TiKV is where the data actually lives. Understanding that split explains most of TiDB's
behaviour.

| Property | Detail |
|---|---|
| **Regions** | the keyspace is split into ranges, each replicated by its own **Raft** group |
| **Automatic sharding and rebalancing** | regions split and move as data grows |
| Transactions | distributed, using a Percolator-style two-phase commit |
| **Placement Driver (PD)** | the component that tracks regions and decides where they live |
| Coprocessor | pushes filters and aggregations down to the storage nodes |
| API | raw key-value, or transactional |

The coprocessor is why TiDB is faster than "a SQL layer over a key-value store" sounds: a `WHERE`
clause is evaluated at the storage node, so only matching rows cross the network.

## Why understanding it explains TiDB

The most useful thing about this page, and the reason the folder exists at all — see
[`../README.md`](../README.md#what-this-folder-is-and-is-not).

| TiDB behaviour | Because of TiKV |
|---|---|
| **Single-row writes are slower than PostgreSQL's** | a write is a Raft round trip, not an `fsync` |
| A sequential primary key creates a bottleneck | it concentrates writes on **one region**, so one Raft leader takes all of them |
| Cross-row transactions cost more when spread out | each region is a separate Raft group to coordinate with |
| Scaling out actually works | regions split and rebalance automatically |
| It survives node loss | each region has replicas, with their own election |

The second row is the practical one, and it is the same warning given in
[`newsql/`](../../newsql/README.md#5-what-to-model-differently). Knowing *why* — that a
monotonic key maps to one region and one leader — makes it a consequence rather than a rule to
memorise.

## When to use it directly

- **building a system** that needs distributed transactional storage without implementing Raft
- the raw key-value API is a good fit and a SQL layer is unwanted overhead
- an existing TiDB deployment where understanding the layer matters operationally

## When not to use it

- as an application database — there is no SQL, no schema and no query planner; use
  [TiDB](../../newsql/tidb/README.md)
- coordination and small configuration — [etcd](../etcd/README.md) is purpose-built, and TiKV's
  PD component actually uses etcd itself
- caching — [`nosql/key-value/`](../../../nosql/key-value/README.md)

## TiKV or FoundationDB

Both are transactional distributed key-value substrates, and they differ in emphasis:

| | TiKV | [FoundationDB](../foundationdb/README.md) |
|---|---|---|
| Consensus | Raft, per region | its own |
| Transaction limits | large | **5 s / 10 MB, deliberately** |
| Ecosystem | TiDB, and the CNCF | layers built by adopters |
| Governance | **CNCF graduated** | Apple, open source |
| Reputation for | production scale with TiDB | **deterministic simulation testing** |

## Notes

Nothing here is deployed, and for a single Kind cluster nothing should be.

Its value in this catalogue is explanatory. [`distributed/`](../../README.md) argues that NewSQL
engines are SQL layers over consensus-replicated key-value stores, and TiKV is the clearest
example — the two halves are separate projects, so the boundary is visible rather than implied.

Reading this before [TiDB](../../newsql/tidb/README.md) makes that page's trade-offs read as
consequences rather than as arbitrary limitations.

---

[← Distributed key-value stores](../README.md)
