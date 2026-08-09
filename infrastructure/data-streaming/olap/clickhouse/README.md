[← OLAP](../README.md)

# ClickHouse

<https://github.com/ClickHouse/ClickHouse>
<https://github.com/Altinity/clickhouse-operator>
<https://clickhouse.com/docs>

---

## The problem it solves

The generalist of this folder, and usually the right default: a columnar database that scans
enormous volumes very fast, ingests from Kafka directly, and answers analytical queries in
milliseconds.

Where [Druid](../druid/README.md) and [Pinot](../pinot/README.md) require committing to a query shape in advance,
ClickHouse is fast at a much wider range of queries — which is what makes it the safest first
choice when the access pattern is not fully known.

| Strength | Detail |
|---|---|
| **Scan speed** | vectorised, columnar, aggressively compressed |
| **Kafka engine** | consumes topics natively, no separate ingestion job |
| Materialised views | transform on insert, which is how pre-aggregation is done here |
| Wide format support | Parquet, JSON, and object storage as a table |
| Flexible queries | not restricted to a modelled pattern |

## When to use it

- **the default** for real-time analytics, logs and event data at scale
- ingesting from Kafka without an intermediate processing job
- application-facing analytics where queries vary

## When not to use it

- transactional workloads — no efficient point updates, and every write is scan-shaped
- high-QPS point lookups on pre-aggregated data — [Pinot](../pinot/README.md) is built for that
- analysts doing ad-hoc exploration over a lakehouse — [Trino](../../../data-engineering/query-engine/README.md) does not need the data loaded

## What decides performance

The **sorting key**, more than anything else. ClickHouse skips data using sparse indexes built
from it, so a table sorted by the column you filter on reads a fraction of the data — and one
sorted by something else reads all of it.

That is chosen at table creation and is expensive to change. Model for the query pattern
first — see [`../README.md`](../README.md#2-what-makes-them-fast).

---

## Notes

### Status

Done:

- Integrated with **MySQL** and **MinIO**

To do:

- Integrate with **Kafka**

The Kafka engine is the piece that makes it a streaming sink rather than a database that
something loads into — worth prioritising for that reason.

### Related

<https://github.com/ClickHouse/ClickHouse/issues/53218>

[chDB](https://github.com/chdb-io/chdb) — ClickHouse as an **embedded** engine, in-process like
[DuckDB](../../../data-engineering/processing/duckdb/README.md). Useful for the same reason: not every
analytical query needs a server.

The [Altinity operator](https://github.com/Altinity/clickhouse-operator) is the established way
to run it on Kubernetes.

---

[← OLAP](../README.md)
