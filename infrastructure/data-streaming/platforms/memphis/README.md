[← Platforms](../README.md)

# Memphis

<https://github.com/superstreamlabs/memphis>
<https://github.com/superstreamlabs/memphis-k8s>

---

## What it is

A message platform positioned as **developer-friendly** rather than Kafka-compatible: a UI from
the start, simpler concepts, schema management built in, and dead-letter handling as a
first-class feature rather than something you assemble.

Built on NATS JetStream underneath.

| Included | Which with Kafka means |
|---|---|
| UI | a separate console |
| Schema management | a separate registry |
| **Dead-letter queues** | building retry and DLQ logic yourself |
| Simple client SDKs | more configuration than most applications need |

The dead-letter handling is the genuinely useful one. Kafka has no built-in concept of it, and
every team reimplements retry-and-park differently.

## When it is interesting

- **a message queue is what you actually need**, not an event log with replay
- the team wants to send and receive messages without learning Kafka's model
- built-in DLQ and retry remove real work

## When it is not

- **Kafka compatibility** — this is not that, and existing clients do not connect
- the ecosystem matters: connectors, integrations, and people who know it
- the project's trajectory is a concern. Memphis has changed hands and direction; check its current status before depending on it

## The question underneath it

Worth asking honestly: **is this a queue problem or a log problem?**

| Queue | Log |
|---|---|
| A message is processed once and gone | events are retained and replayable |
| Consumers are workers | consumers are independent readers at their own position |
| DLQ and retry are the hard parts | ordering and reprocessing are the hard parts |
| **Memphis, RabbitMQ, NATS** | **Kafka, Pulsar, Redpanda** |

A large amount of Kafka gets deployed for what is really the left column — and
[RabbitMQ](../../../software-engineering/message-queue/rabbitmq/) or NATS would be a fraction of
the operational cost.

That distinction is the useful thing this tool surfaces, whether or not it is the answer.

---

[← Platforms](../README.md)
