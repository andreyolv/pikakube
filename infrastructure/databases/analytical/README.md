[← Databases](../README.md)

# Analytical databases

Built for scans and aggregations, not for transactions.

Tools covered: [`byconity`](byconity/README.md) · [`databend`](databend/README.md) · [`kyuubi`](kyuubi/README.md)

---

## OLTP and OLAP are different machines

| | Transactional (OLTP) | Analytical (OLAP) |
|---|---|---|
| Reads | a few rows, by key | millions of rows, a few columns |
| Writes | many small, concurrent | bulk loads, or streaming appends |
| Storage | row-oriented | **columnar** |
| Indexes | many, for point lookups | few — scanning is the plan |
| Optimises for | latency per transaction | throughput per scan |

Running analytics on an OLTP database is the most common version of getting this wrong. One
aggregation over a large table competes for the same buffers and locks as the transactions, and
the outage appears somewhere unrelated.

The rule: **analytics reads a replica, the warehouse, or a query engine** — never the primary.

## Where these sit against the neighbours

This folder overlaps deliberately with two others, and the boundary is about **who is waiting**:

| Question | Where |
|---|---|
| Analysts querying the lakehouse, ad-hoc | [`data-engineering/query-engine/`](../../data-engineering/query-engine/README.md) — Trino |
| **An application** needing millisecond answers at high concurrency | [`data-streaming/olap/`](../../data-streaming/olap/README.md) — ClickHouse, StarRocks, Pinot |
| An analytical **database** as a system in its own right | here |

The distinction is real but narrow, and the tools blur it. ClickHouse is discussed under
`data-streaming/olap/` because its most interesting use is serving applications; it is equally a
database.

## The tools

| Tool | What it is | Shines when | Detail |
|---|---|---|---|
| **ByConity** | cloud-native fork of ClickHouse, separating storage and compute | you want ClickHouse semantics with elastic compute and shared storage | [→](byconity/README.md) |
| **Databend** | Rust, object-storage-native, Snowflake-inspired architecture | an elastic warehouse on object storage, without a vendor | [→](databend/README.md) |
| **Kyuubi** | **not a database** — a multi-tenant SQL gateway over Spark, Flink and Trino | many users need governed SQL access to an existing engine | [→](kyuubi/README.md) |

**Kyuubi is the odd one and worth knowing about.** It provides a JDBC/Thrift front end to
engines you already run, with multi-tenancy, isolation and authentication — solving "how do
analysts get to Spark safely" rather than storing anything itself.

The other two share a design point that matters: **storage separated from compute, on object
storage**. That is the same architectural bet as Snowflake and BigQuery, and it is what makes
compute elastic rather than provisioned.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Analytics on the production OLTP primary | it causes outages in unrelated services | a replica, warehouse or query engine |
| An analytical database used transactionally | no efficient point updates; every write is a scan-shaped operation | keep OLTP where it belongs |
| Adopting one when a query engine suffices | another system to operate for questions Trino already answers | measure the latency requirement |
| Row-oriented storage for analytics | every query reads every column | Parquet or a columnar engine — see [file formats](../../data-engineering/file-formats.md) |
| No lifecycle policy | analytical data grows without bound | tiering and retention |

## How this applies to pikakube

Nothing here is deployed, and that is consistent: this repository's analytical path is
[Trino](../../data-engineering/query-engine/README.md) over a lakehouse, which covers the analyst case
without a separate database.

These are mapped as the alternatives for two specific situations — when compute needs to be
elastic and separated from storage (ByConity, Databend), and when many users need governed SQL
access to an existing engine (Kyuubi).

---

[← Databases](../README.md)
