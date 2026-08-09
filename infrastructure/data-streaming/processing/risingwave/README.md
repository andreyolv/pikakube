[← Stream processing](../README.md)

# RisingWave

<https://github.com/risingwavelabs/risingwave>
<https://github.com/risingwavelabs/helm-charts>
<https://docs.risingwave.com/>

---

## The problem it solves

Stateful stream processing normally means writing a **job**: define a pipeline, manage state,
configure checkpoints, handle restarts, and operate it.

RisingWave replaces that with a **materialised view**:

```sql
CREATE MATERIALIZED VIEW orders_by_region AS
SELECT region, count(*) AS orders, sum(amount) AS revenue
FROM orders_stream
GROUP BY region;
```

That view stays current as events arrive, and it is **queryable like a table** — over the
PostgreSQL wire protocol, so existing clients and BI tools connect to it directly.

The conceptual jump is much smaller than Flink's for a team that already thinks in SQL and dbt
models.

| | Flink | RisingWave |
|---|---|---|
| Unit of work | a job | a **materialised view** |
| Interface | Java, Scala, Python, SQL | **SQL** |
| Result | a stream, or a write to a sink | a queryable table |
| State | you configure the backend | managed |
| Clients | none — it is a job | PostgreSQL protocol |

## When to use it

- continuously-updated aggregations that should be **queryable**, not just emitted
- the team is SQL-first — analytics engineers rather than JVM developers
- serving real-time metrics to a dashboard or an application without a separate OLAP store

## When not to use it

- arbitrary logic that is not expressible in SQL — [Flink](../flink/README.md)
- stateless plumbing, where [Benthos](../benthos/README.md) is far lighter
- very large state with complex event-time semantics, where Flink's control is the point

## Where it fits in a lakehouse

The interesting position: it can consume from Kafka and **sink to Delta Lake**, which makes it a
streaming path into the lakehouse that is defined entirely in SQL.

- [Kafka source](https://docs.risingwave.com/docs/current/create-source-kafka/)
- [Delta Lake sink](https://docs.risingwave.com/docs/current/sink-to-delta-lake/)

For a platform that already models in [dbt](../../../analytics-engineering/transform/dbt/README.md), that
is a materially smaller step than adopting a job-based engine — and it is the reason this is
worth a real evaluation rather than a mention.

---

[← Stream processing](../README.md)
