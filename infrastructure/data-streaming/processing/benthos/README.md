[← Stream processing](../README.md)

# Benthos

<https://github.com/redpanda-data/benthos>
<https://github.com/redpanda-data/redpanda-connect-plugin-example>

> Now maintained by Redpanda as **Redpanda Connect**.

---

## The problem it solves

Most streaming work is not stateful. It is: read from here, reshape the payload, drop what does
not match, enrich from a lookup, write to there.

Doing that with [Flink](../flink/README.md) means an engine, checkpoints, a state backend and a job to
operate — for a `map()`.

Benthos is a **single binary** with a declarative configuration:

```yaml
input:
  kafka: { addresses: [kafka:9092], topics: [orders] }
pipeline:
  processors:
    - mapping: |
        root.order_id = this.id
        root.total = this.items.sum()
output:
  aws_s3: { bucket: lake, path: orders/${!timestamp_unix()}.json }
```

Its **Bloblang** mapping language is the reason it works: expressive enough for real reshaping,
and not a general-purpose language — which keeps the configuration readable.

## When to use it

- **stateless** work, which is the majority: routing, reshaping, filtering, enrichment
- connecting systems: Kafka to S3, HTTP to Kafka, database to topic
- you want one binary rather than a cluster

## When not to use it

- **stateful** processing — joins between streams, windowed aggregations. That is [Flink](../flink/README.md)
- SQL is the preferred interface — [RisingWave](../risingwave/README.md) or [ksqlDB](../ksqldb/README.md)

## Why it belongs at the front of this folder

The most common mistake in stream processing is reaching for the heaviest tool first. Flink for
a filter is the same category of error as
[Spark for a gigabyte](../../../data-engineering/processing/README.md#1-the-question-to-ask-first).

Start here. Move to Flink when state genuinely appears.

## Extending it

[Plugin example](https://github.com/redpanda-data/redpanda-connect-plugin-example) — for the
cases where a connector or processor does not exist and the mapping language is not enough.

## Note on the project

Originally an independent project, now under Redpanda as Redpanda Connect. Licensing changed
with that move — worth checking the terms for the version you deploy, since the older Benthos
releases and the current Connect are not under identical licences.

---

[← Stream processing](../README.md)
