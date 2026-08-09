[← OLAP](../README.md)

# Apache Pinot

<https://github.com/apache/pinot>
<https://docs.pinot.apache.org/>

---

## What it is

Built at LinkedIn for a specific problem: **user-facing analytics at thousands of queries per
second**, with millisecond latency — the "who viewed your profile" class of feature, where the
person waiting is a customer and there are a lot of them.

That origin explains everything about it:

| Property | Why |
|---|---|
| **Heavy indexing** | inverted, sorted, range, star-tree, text — chosen per column |
| **Star-tree index** | pre-computed aggregations inside the index, so common queries need almost no work |
| Low latency at high QPS | the design target, not a side effect |
| Real-time and offline tables | streaming ingest and batch load, unified at query time |
| Upserts on real-time tables | which most OLAP engines do not offer |

The star-tree index is the distinctive one: it materialises aggregation combinations inside the
index structure, which is how it answers pre-modelled queries in single-digit milliseconds.

## When to use it

- **thousands of QPS** from an application, not from analysts
- query patterns are known and stable enough to index for
- latency budget is measured in milliseconds

## When not to use it

- **joins** — it is not built for them; [StarRocks](../starrocks/README.md) is
- ad-hoc or exploratory queries — indexing for the unknown is not possible
- moderate concurrency, where [ClickHouse](../clickhouse/README.md) is simpler and more flexible
- the operational surface is a concern; like Druid, it has several component roles

## Pinot or Druid

Closest comparison in this folder, and both are specialists:

| | Pinot | Druid |
|---|---|---|
| Optimised for | **QPS** — many concurrent queries | **time-series** event analysis |
| Indexing | very rich, per column | time-partitioned, dimension-indexed |
| Rollup | optional | central to the design |
| Upserts | supported on real-time tables | limited |

Choose Pinot when concurrency is the constraint, Druid when time-series rollup is the shape.
Choose neither if the queries are not known in advance.

## The recurring caution

Everything in this folder trades flexibility for speed, and Pinot trades the most. The index
strategy **is** the schema, and changing which queries are fast means rebuilding it.

Worth being certain about the access pattern before adopting it — see
[`../README.md`](../README.md#2-what-makes-them-fast).

---

[← OLAP](../README.md)
