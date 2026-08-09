[← Stream processing](../README.md)

# Arroyo

<https://github.com/ArroyoSystems/arroyo>
<https://doc.arroyo.dev/>

---

## What it is

Stateful stream processing in **Rust**, with SQL as the interface — Flink-class semantics
(event time, watermarks, exactly-once, windowed aggregations) at a much smaller footprint.

Built on [DataFusion](../../../data-engineering/query-engine/datafusion/README.md), which is the same
foundation as several of the Spark accelerators — see
[`spark-accelerator/`](../../../data-engineering/processing/spark/spark-accelerator/README.md).

| | Flink | Arroyo |
|---|---|---|
| Runtime | JVM | Rust |
| Footprint | substantial | small |
| Interface | Java, Scala, Python, SQL | **SQL** |
| Semantics | the reference | comparable in scope |
| Ecosystem | very large | small |

## When to use it

- **Flink's semantics without Flink's footprint** — the clearest reason
- SQL is the interface, and the team is not JVM-oriented
- resource cost of a Flink deployment is disproportionate to the work

## When not to use it

- the ecosystem matters — connectors, integrations, and answers when something breaks
- production dependence on a younger project with a smaller community
- results should be queryable as tables — [RisingWave](../risingwave/README.md)

## Arroyo or RisingWave

Both are Rust, both are SQL, and they answer different questions:

| | Arroyo | RisingWave |
|---|---|---|
| Model | **jobs** — a pipeline that runs | **materialised views** — state you query |
| Output | to a sink | queryable over the PostgreSQL protocol |
| Closest to | Flink, smaller | a streaming database |

Arroyo is the lighter Flink. RisingWave is a different shape entirely.

---

## Notes

> PostgreSQL is deployed separately.

It stores pipeline metadata and configuration in Postgres, which is not bundled — worth knowing
before deployment, since it is an external dependency the chart expects to exist.

On a cluster already running [CloudNativePG](../../../databases/sql/postgresql/operator/cnpg/README.md),
that is a small addition rather than a new system.

---

[← Stream processing](../README.md)
