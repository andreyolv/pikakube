[← Stream processing](../README.md)

# Quix Streams

<https://github.com/quixio/quix-streams>
<https://quix.io/docs/>

---

## What it is

A Python library for stateful stream processing on Kafka, with a **pandas-like DataFrame API** —
so the code looks like data work rather than like a streaming framework.

```python
sdf = app.dataframe(topic)
sdf = sdf[sdf["amount"] > 100]
sdf["total"] = sdf["amount"] * sdf["quantity"]
sdf = sdf.group_by("region").agg(...)
sdf.to_topic(output)
```

No cluster to submit to: it is a library, so a pipeline is a Python process that scales by
running more of them — Kafka consumer groups handle the partitioning.

## When to use it

- the team is **Python** and the mental model is DataFrames
- Kafka is the source and destination
- you want to deploy a stream processor as an ordinary container, not submit a job

## When not to use it

- complex event-time semantics and very large state — [Flink](../flink/README.md)
- SQL is preferred — [RisingWave](../risingwave/README.md) or [ksqlDB](../ksqldb/README.md)
- stateless plumbing — [Benthos](../benthos/README.md), which needs no code

## Quix or Bytewax

The two Python options here, and they differ in shape:

| | Quix Streams | [Bytewax](../bytewax/README.md) |
|---|---|---|
| API | **DataFrame**, pandas-like | dataflow — operators and steps |
| Core | Python, on Kafka | Rust |
| Scaling | Kafka consumer groups | its own dataflow model |
| Feels like | pandas | a stream processing library |

Quix suits analytics engineers who think in DataFrames. Bytewax suits engineers who think in
pipelines and want a Rust core.

## The deployment property worth noting

Because it is a library, a pipeline is a container running a Python process — deployed with a
Deployment, scaled with replicas, monitored like anything else.

No job submission, no cluster, no separate control plane. For a Kubernetes platform that is a
genuinely simpler operational model than anything else in this folder except
[Benthos](../benthos/README.md).

---

[← Stream processing](../README.md)
