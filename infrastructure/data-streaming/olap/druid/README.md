[← OLAP](../README.md)

# Apache Druid

<https://github.com/apache/druid>
<https://github.com/datainfrahq/druid-operator>
<https://druid.apache.org/>

---

## What it is

A time-series-oriented analytical database, designed for **event data queried by time and
dimension** at very high concurrency.

Its defining choice is **pre-aggregation at ingest**: rollup happens as data arrives, so queries
read summarised segments rather than raw events. That is why it is fast, and why it constrains
what you can ask.

| Property | Consequence |
|---|---|
| Time-partitioned segments | queries with a time filter skip almost everything |
| **Rollup at ingest** | storage shrinks dramatically; raw detail is gone unless retained |
| Dimension indexes | filtering on known dimensions is very fast |
| Real-time ingestion | from Kafka, queryable within seconds |
| Weak joins | it is not built for them |

## When to use it

- **event analytics over time** — clickstream, telemetry, monitoring, ad tech
- known dimensions, and queries that always filter by time
- very high concurrency on those queries
- real-time ingestion where events must be queryable immediately

## When not to use it

- **joins are needed** — [StarRocks](../starrocks/README.md) or [Doris](../doris/README.md)
- the query pattern is not known in advance — [ClickHouse](../clickhouse/README.md) is far more forgiving
- raw event detail must be preserved and queried; rollup discards it by design
- the operational surface is a concern. Druid has many components — coordinator, overlord, broker, historical, middle manager — and that is a real commitment

## The decision that cannot be undone

**Rollup granularity.** Aggregating to the minute at ingest means per-second questions can never
be answered, because that data no longer exists.

That is chosen before the first event lands, and it is the one thing worth being conservative
about — storage is cheaper than the answer you cannot reconstruct.

## Deployment

The [operator](https://github.com/datainfrahq/druid-operator) manages the component roles. Doing
this without one means understanding and coordinating five stateful services, which is the main
reason Druid deployments are considered heavy.

For a smaller footprint with a similar goal, [Pinot](../pinot/README.md) is the comparison; for a
general-purpose alternative, [ClickHouse](../clickhouse/README.md).

---

[← OLAP](../README.md)
