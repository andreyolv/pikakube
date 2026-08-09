[← Table formats](../README.md)

# DuckLake

<https://github.com/duckdb/ducklake>

---

## The idea

Not a variation on the other formats in this folder — an argument about **where metadata belongs.**

Iceberg, Delta, Hudi and Paimon all store table metadata as **files** alongside the data: manifests,
transaction logs, snapshot pointers. That is what makes them self-describing and portable, and it
is also the source of most of their complexity.

DuckLake puts the metadata in a **transactional SQL database** and keeps only the data files in
object storage.

| | File-based metadata | DuckLake |
|---|---|---|
| Metadata lives in | manifests and logs on object storage | **a SQL database** |
| A commit | atomic pointer swap, coordinated by a catalog | **a database transaction** |
| Listing a table's files | read and merge manifests | **a query** |
| Multi-table transactions | not supported | **possible** |
| Small-change overhead | a new metadata file per commit | a row |
| Extra dependency | a catalog service | **a database** |
| Portability | self-describing on object storage | requires the database |

## Why it is a serious argument

The observation behind it is fair: the file-based formats reimplement, in object storage, things a
transactional database already does well — atomic commits, concurrent writers, consistent
listings, referential structure.

Doing that on object storage is hard because object stores have weak consistency guarantees and no
transactions. So each format built a protocol around those limitations, and then needed a
**catalog** — a database, effectively — to serialise the commits anyway. See
[`metadata-catalog/`](../../../metadata-catalog/README.md).

DuckLake's point is that if a database is required regardless, the metadata may as well live in it
rather than being encoded into files that the database then has to point at.

The consequences are real: metadata operations become fast and genuinely transactional, and
transactions can span multiple tables — which none of the file-based formats support.

## When to use it

Honestly: **not yet, in production.** It is early, and the ecosystem around it is small.

Where it is worth attention:

- evaluating lakehouse architecture, where the argument itself is instructive
- DuckDB is already the analytical engine
- multi-table transactions are a requirement nothing else here meets

## When not to use it

- production workloads today — [Iceberg](../iceberg/README.md) is the default for good reason
- multi-engine access; support is narrow
- the metadata must be self-describing on object storage, independent of any service
- the operational appetite for a database in the critical path of every table read is limited

## The trade, stated plainly

**Gained:** fast, genuinely transactional metadata; multi-table transactions; far less protocol
complexity.

**Lost:** portability. A file-based table can be read by any engine that understands the format,
from the bucket alone. A DuckLake table requires the metadata database — which is a service to
run, back up, scale and keep available.

Whether that trade is right is not settled, and both positions are defensible. It is worth noting
that the file-based formats already require a catalog service for safe concurrent writes, so the
difference is smaller than it first appears — the argument is about *how much* lives in the
database, not whether one is needed.

## Notes

Reference material recorded here:

- [duckdb#14525](https://github.com/duckdb/duckdb/discussions/14525)
- [duckdb#18551](https://github.com/duckdb/duckdb/discussions/18551)

Tracked as an **idea rather than a candidate**, which is the right posture for it. Nothing is
deployed and nothing should be.

It pairs naturally with [DuckDB](../../../../data-engineering/processing/duckdb/README.md), which
is mapped in this repository and makes the same broader argument from a different direction: not
every analytical workload needs a cluster, and a great deal of infrastructure exists to solve
problems that only appear at scale.

---

[← Table formats](../README.md)
