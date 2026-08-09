[← Stream processing](../README.md)

# Apache Flink

<https://github.com/apache/flink>
<https://github.com/apache/flink-kubernetes-operator>
<https://flink.apache.org/>

---

## The problem it solves

The reference **stateful** stream processor. Where a simple tool filters and forwards, Flink
handles the problems that make streaming genuinely hard:

| Capability | Why it is hard elsewhere |
|---|---|
| **Event time and watermarks** | deciding how long to wait for late events, and what to do with later ones |
| **Managed state** | joins and aggregations that survive restarts, checkpointed and recoverable |
| **Exactly-once** | end to end, when the sink supports it |
| Windowing | tumbling, sliding, session — over event time, not arrival time |
| Savepoints | stop a job, change it, resume from where it was |

Savepoints are underrated: they are what makes upgrading a stateful job possible without
reprocessing history.

## When to use it

- **stateful** processing — joins between streams, windowed aggregations, deduplication
- correctness under late and out-of-order events matters
- large state that must survive restarts

## When not to use it

- the job is stateless reshaping — [Benthos](../benthos/README.md) is a fraction of the operational cost
- SQL over streams with results queryable as tables — [RisingWave](../risingwave/README.md)
- Kafka-only, and SQL is enough — [ksqlDB](../ksqldb/README.md)

## On Kubernetes

The [Flink Kubernetes Operator](https://github.com/apache/flink-kubernetes-operator) is the
right way to run it: `FlinkDeployment` as a CRD, with savepoint management, upgrades and
recovery handled by the controller rather than by scripts.

Metrics:
[enabling Prometheus](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-release-1.7/docs/operations/metrics-logging/#how-to-enable-prometheus-example)
— worth doing on day one, because checkpoint duration and backpressure are the two signals that
explain almost every Flink problem.

## What to configure before production

| Setting | Why |
|---|---|
| **Checkpointing** | interval and storage. Without it, a restart reprocesses from the beginning or loses state |
| **State backend** | RocksDB for large state, with a durable checkpoint directory on object storage |
| **State TTL** | a keyed aggregation with no expiry grows until the job dies |
| Restart strategy | how many times, and how fast, before it stops trying |
| Watermark strategy | how long to wait for late events — a correctness decision, not a tuning one |

State TTL is the one most often missed, and its failure mode is a job that runs perfectly for
three months and then cannot recover.

---

## Notes

### Examples and learning

- [Python example](https://github.com/apache/flink-kubernetes-operator/tree/main/examples/flink-python-example) for the operator
- [Stream processing with Apache Flink](https://github.com/polyzos/stream-processing-with-apache-flink)

```bash
pip install kafka-python
```

### Status

Done:

- PoC with the connector generator

To do:

- PoC with other connectors, on Kafka

---

[← Stream processing](../README.md)
