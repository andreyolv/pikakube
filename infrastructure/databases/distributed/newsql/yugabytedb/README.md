[← NewSQL](../README.md)

# YugabyteDB

<https://github.com/yugabyte/yugabyte-db>
<https://github.com/yugabyte/charts>

---

## The problem it solves

Distributed SQL that is **closest to real PostgreSQL** — because it reuses PostgreSQL's actual
query layer.

That is the architectural decision that distinguishes it. Where
[CockroachDB](../cockroachdb/README.md) reimplements the PostgreSQL wire protocol over its own
engine, YugabyteDB takes the PostgreSQL upper half and replaces the storage beneath it:

| Layer | What it is |
|---|---|
| **YSQL** | the **actual PostgreSQL query layer**, reused |
| DocDB | distributed document storage, Raft-replicated, RocksDB-based |
| YCQL | a second API, Cassandra-compatible, over the same storage |

The consequence is compatibility that goes further than the protocol: many PostgreSQL
**extensions** work, plan behaviour is familiar, and SQL surface that trips up reimplementations
generally works here.

It is **Apache 2.0**, which is a material difference from CockroachDB's source-available licence.

## When to use it

- a **measured** ceiling on one machine, and PostgreSQL compatibility matters closely
- extensions or PostgreSQL-specific behaviour are in use
- an Apache licence is a requirement
- multi-region with row-level geo-placement

## When not to use it

- **the ceiling has not been measured** — this is slower than PostgreSQL for a workload that fits
  on one machine; see [`../README.md`](../README.md#2-the-cost-stated-first)
- MySQL compatibility — [TiDB](../tidb/README.md) or [Vitess](../vitess/README.md)
- analytics on the same data — TiDB's [HTAP](../tidb/README.md) story has no equivalent here
- single region, where the design's cost is paid and its benefit is unused

## The two-API question

YugabyteDB exposes YSQL (PostgreSQL) and YCQL (Cassandra) over the same storage, which looks like
flexibility and is worth treating carefully.

They are **not interchangeable views of the same data.** A table created through YSQL is not
queryable through YCQL. Choosing one is choosing the data model, and the presence of the other is
not an escape hatch.

For a platform, YSQL is almost always the answer — it is the reason to choose YugabyteDB at all.
YCQL exists for teams migrating from Cassandra who want transactions, which is a genuine but
narrow case, and one where [`nosql/column/`](../../../nosql/column/README.md) is the folder to read
first.

## Compatibility, honestly

Closer than the alternatives, and still not identical:

| Area | Status |
|---|---|
| SQL surface | **very high** — it is the real PostgreSQL parser and planner front-end |
| **Extensions** | many work; not all, and the supported list is worth checking |
| **Latency** | every write is a consensus round trip — this does not change |
| Plan behaviour | familiar, though costs and choices differ over distributed storage |
| Sequences | monotonic keys concentrate writes on one tablet — use `UUID` or hash sharding |

The latency row is the one people are surprised by despite it being unavoidable. Reusing
PostgreSQL's query layer makes the *semantics* familiar; it does not make a distributed commit as
fast as a local `fsync`.

## Notes

Mapped with the [official charts](https://github.com/yugabyte/charts).

Nothing is deployed, and on a single Kind cluster nothing should be.

Its position in [`newsql/`](../README.md): **the best PostgreSQL compatibility and an Apache
licence**, which is the combination that would make it the candidate if this platform ever
outgrew [CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md).

That prior question is the one that matters more, and
[`../README.md`](../README.md#4-decision-tree) answers it plainly: read replicas and connection
pooling solve most of what people reach for distributed SQL to fix, and the threshold is a
measured ceiling rather than an expectation of growth.

---

[← NewSQL](../README.md)
