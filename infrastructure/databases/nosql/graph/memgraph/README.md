[← Graph databases](../README.md)

# Memgraph

<https://github.com/memgraph/memgraph>
<https://github.com/memgraph/helm-charts>

---

## The problem it solves

A graph database that is **in-memory and built for streaming ingestion** — the graph is updated
continuously and queried with very low latency.

It is Cypher-compatible, which means the queries and much of the knowledge transfer directly from
[Neo4j](../neo4j/README.md). The difference is where it is pointed:

| | Neo4j | Memgraph |
|---|---|---|
| Storage | disk-based, with caching | **in-memory**, with durability on disk |
| Written in | Java | **C++** |
| Ingestion | batch and transactional | **streaming — Kafka, Pulsar, Redpanda natively** |
| Latency | good | **very low** |
| Ecosystem | much larger | growing |
| Dataset size | limited by disk | **limited by RAM** |

## The real differentiator: streaming ingestion

Memgraph consumes from Kafka, Pulsar and Redpanda directly, with a transformation defined in the
database — so events become nodes and relationships without a pipeline in between.

That closes a gap that otherwise has to be built. In a conventional setup, keeping a graph current
from an event stream means a consumer application that reads messages and issues writes — code
that must be deployed, monitored and kept correct.

For a platform that already runs [Kafka or Redpanda](../../../../data-streaming/README.md), that
is a meaningful simplification, and it is what makes the fraud-detection case work: transactions
arrive on a topic, the graph reflects them within milliseconds, and the traversal query runs
against current state.

## When to use it

- **real-time graph analysis** — fraud, network monitoring, live recommendations
- the graph is fed from an **event stream**, continuously
- traversal latency matters at single-digit milliseconds
- the working set fits in memory

## When not to use it

- the graph is **larger than RAM** — this is the hard constraint
- the ecosystem matters — [Neo4j](../neo4j/README.md) has far more tooling, answers and people
- batch analytical graph work, where in-memory buys little
- PostgreSQL is already running and the graph is moderate —
  [Apache AGE](../age/README.md)

## The memory constraint

In-memory is the whole design, and it must be sized honestly.

The graph lives in RAM; persistence is snapshots and a write-ahead log for durability, not a
storage tier. That means the memory requirement is the dataset plus working overhead, and
exceeding it is not a slow degradation — it is failure.

On Kubernetes that translates to a concrete requirement: the pod's memory limit must
accommodate the whole graph plus headroom, and it must be monitored as a hard ceiling rather than
as a utilisation metric. This is the same class of failure described for
[Redis](../../key-value/README.md#6-running-them-on-kubernetes), and it applies with more force
because the data is not a rebuildable cache.

## Notes

Mapped with the [official Helm chart](https://github.com/memgraph/helm-charts).

Its licence is worth checking against how the platform ships — Memgraph has used a
source-available licence for the main engine with an open-source community edition, and the
terms have moved over time.

For this platform it is the interesting graph option for a specific reason: the streaming layer
already exists in [`data-streaming/`](../../../../data-streaming/README.md), and Memgraph is the
one entry in this folder that consumes from it natively. If a graph requirement ever appears here
that is fed by events rather than by batch loads, this is the one to evaluate first — with
[AGE](../age/README.md) as the answer when it is not.

---

[← Graph databases](../README.md)
