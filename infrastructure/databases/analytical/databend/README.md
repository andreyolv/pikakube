[← Analytical databases](../README.md)

# Databend

<https://github.com/databendlabs/databend>
<https://github.com/databendlabs/helm-charts>

---

## The problem it solves

A cloud-native data warehouse in **Rust**, with storage and compute genuinely separated: data
lives in object storage, and compute clusters are stateless and disposable.

That architecture is the point. Where [ClickHouse](../../../data-streaming/olap/clickhouse/README.md)
attaches storage to nodes, Databend keeps everything in S3-compatible storage and treats compute
as something you start, use and stop.

| Property | Consequence |
|---|---|
| **Storage on object storage** | capacity is the bucket's; nodes hold no durable state |
| **Stateless compute** | scale to zero, or run several isolated clusters over the same data |
| Snowflake-compatible SQL | much of the dialect and semantics carry across |
| Written in Rust | no JVM, no garbage collector |
| Time travel | query the table as of an earlier point |
| Elastic | add compute for a heavy query, remove it afterwards |

The multi-cluster property is the underrated one: separate warehouses for ETL and for analysts,
sized differently, reading the same data with no copying.

## When to use it

- **elasticity matters** — bursty analytical load, where paying for idle compute is the problem
- a Snowflake-like model is wanted on self-hosted infrastructure
- object storage is already the platform's foundation
- workloads should be isolated from each other without duplicating data

## When not to use it

- **low-latency, high-concurrency serving** —
  [ClickHouse](../../../data-streaming/olap/clickhouse/README.md) or
  [Pinot](../../../data-streaming/olap/pinot/README.md) are built for that
- a lakehouse with open table formats is the direction —
  [`data-governance/lakehouse/`](../../../data-governance/lakehouse/README.md) and a query engine
  like Trino answer that without loading data in
- the ecosystem matters; this is a much smaller project than ClickHouse
- object-storage latency is unacceptable for the query profile

## The trade-off to understand

Separating storage from compute buys elasticity and costs **latency**.

Every query reads from object storage. Caching mitigates it, and a cold query is fundamentally
slower than one against local NVMe. That is the correct trade for warehouse-style analytical
queries measured in seconds, and the wrong one for application-facing queries measured in
milliseconds.

Deciding which of those the workload is comes before comparing anything else.

## Where it sits in this repository

Analytical databases appear in two folders, and the split is deliberate:

| Folder | Focus |
|---|---|
| **`databases/analytical/`** | warehouse-shaped — batch analytics, elasticity, SQL over large volumes |
| [`data-streaming/olap/`](../../../data-streaming/olap/README.md) | **real-time** — ClickHouse, StarRocks, Druid, Pinot; low latency and high concurrency |

Databend belongs here because its argument is elasticity and cost over object storage, not
millisecond serving.

## Notes

Mapped with the [official Helm charts](https://github.com/databendlabs/helm-charts).

The architectural idea is the same one that appears repeatedly across this repository —
[AutoMQ](../../../data-streaming/event-streaming/automq/README.md) for the event log,
[Quickwit](../../../observability/logs/storage/quickwit/README.md) for search, and the lakehouse
table formats generally. **Separating storage from compute on object storage is the recurring
pattern of this generation of infrastructure**, and Databend is the warehouse instance of it.

For this platform, with [MinIO](../../../site-reliability-engineering/storage/object-storage/minio/README.md)
already deployed, the storage side requires nothing new. The prior question is whether an
analytical database is needed at all when the lakehouse plus a query engine covers the same ground
without loading data into a system that owns it — which is the discussion in
[`data-governance/lakehouse/`](../../../data-governance/lakehouse/README.md).

---

[← Analytical databases](../README.md)
