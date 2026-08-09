[← Stream processing](../README.md)

# Bytewax

<https://github.com/bytewax/bytewax>
<https://github.com/bytewax/helm-charts>

---

## The problem it solves

Stateful stream processing for teams whose language is **Python** — not PyFlink, which is a
wrapper over a JVM engine, but a Python-native dataflow with a Rust core underneath.

That distinction matters in practice. PyFlink pays serialisation crossing the Python/JVM
boundary, and debugging spans two runtimes. Bytewax is a Python library that happens to be fast.

```python
flow = Dataflow("orders")
stream = op.input("in", flow, KafkaSource(["kafka:9092"], ["orders"]))
stream = op.map("parse", stream, json.loads)
stream = op.stateful_map("running_total", stream, accumulate)
op.output("out", stream, KafkaSink(...))
```

Ordinary Python — including the libraries. Which is the point: a model, a parser, a client that
only exists in Python, used directly inside a streaming pipeline.

## When to use it

- the team writes **Python**, and a JVM engine is a real barrier
- the transformation needs Python libraries — ML inference, a specific parser, an SDK
- Flink's operational weight is disproportionate

## When not to use it

- very large state with complex event-time requirements — [Flink](../flink/README.md) is the reference for a reason
- SQL is the preferred interface — [RisingWave](../risingwave/README.md) or [ksqlDB](../ksqldb/README.md)
- stateless plumbing — [Benthos](../benthos/README.md) needs no code at all

## Where it genuinely fits

**Real-time ML inference on a stream.** The model is in Python, the feature engineering is in
Python, and the alternative is either rewriting them for the JVM or paying a boundary crossing
per event.

That case is common on a data platform and awkward with every other tool here.

## Note on the ecosystem

Smaller than Flink's by a wide margin — fewer connectors, less written material, fewer people
who have run it in production.

Worth weighing honestly: the Python-native argument is real, and so is being alone with a
problem at 3am.

---

[← Stream processing](../README.md)
