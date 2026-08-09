[← Stream processing](../README.md)

# GlassFlow

<https://github.com/glassflow/clickhouse-etl>

---

## What it is

Streaming ETL specifically for **Kafka into ClickHouse**, in Python — a narrow tool for a
common path.

The problem it targets is real: ClickHouse's Kafka engine handles simple ingestion, and anything
requiring transformation, deduplication or joins before the insert means a processing engine
between them. That is a lot of machinery for what is often a small amount of Python.

| Handles | Detail |
|---|---|
| Kafka to ClickHouse | the whole path, as one thing |
| **Deduplication** | before the insert, which ClickHouse handles awkwardly after |
| Temporal joins | enriching a stream from another stream |
| Python transformations | ordinary code, no JVM |

Deduplication is the useful one. ClickHouse's `ReplacingMergeTree` deduplicates *eventually*,
which is a frequent source of confusion — doing it before the insert avoids the problem
entirely.

## When it is useful

- the pipeline genuinely **is** Kafka to ClickHouse, and nothing more general is needed
- Python is the language, and Flink is disproportionate
- deduplication or enrichment before insertion is the requirement

## When it is not

- the destination is not ClickHouse — this is purpose-built
- general stream processing — [Benthos](../benthos/README.md) for stateless, [Flink](../flink/README.md) for stateful
- production dependence on a young, narrow project

## The honest framing

A specialised tool, and specialisation is its argument. If the pipeline is exactly this shape,
it removes a general-purpose engine from the picture.

The alternatives for the same path, in order of weight:

1. **ClickHouse Kafka engine** alone — if no transformation is needed, nothing else is required
2. **This**, or [Benthos](../benthos/README.md) — for transformation without state
3. **Flink** — when the transformation is genuinely stateful

Most Kafka-to-ClickHouse pipelines are row 1 or row 2, and reaching for row 3 by default is the
mistake this folder keeps pointing at.

---

[← Stream processing](../README.md)
