[← Broker](../README.md)

# RabbitMQ

<https://github.com/rabbitmq/rabbitmq-server>
<https://github.com/rabbitmq/cluster-operator>
<https://github.com/rabbitmq/messaging-topology-operator>

Deployment: [`rabbitmq/`](rabbitmq/README.md) ·
[`rabbitmq-cluster-operator/`](rabbitmq-cluster-operator/README.md)

Client: [pika](https://github.com/pika/pika)

---

## The problem it solves

**Routing, and per-message reliability.**

RabbitMQ implements AMQP 0-9-1, which means the producer publishes to an *exchange* with a routing
key and never names a queue. Bindings — configured in the broker, not in the producer — decide
which queues receive a copy. Adding a consumer becomes a binding rather than a change to somebody
else's service.

What it gives that lighter brokers do not:

| Capability | Detail |
|---|---|
| **Exchange types** | direct, topic, fanout, headers — see [`broker/`](../README.md#3-routing--rabbitmqs-exchange-types) |
| **Quorum queues** | Raft-replicated, always durable, with a `delivery-limit` for poison messages |
| **Dead-letter exchanges** | a queue property, triggered by reject, TTL, overflow or delivery limit |
| Per-message TTL, priorities, publisher confirms | the reliability knobs, individually |
| **Streams** | an append-only replayable log inside the same broker — see [`rabbitmq/`](rabbitmq/README.md) |
| Virtual hosts | logical isolation, so one cluster serves many applications |
| Management UI and HTTP API | mature, and the reason most people find it operable |

Classic mirrored queues are gone — deprecated, then removed in RabbitMQ 4.0. **Quorum queues are
the current answer** for anything that matters, with classic (unmirrored) queues remaining
appropriate only for short-lived throwaway ones.

## When to use it

- **routing decides who receives a message** — several consumers with different interests
- per-message reliability: acknowledgements, retries with a limit, dead-lettering
- multiple applications on one cluster, isolated by vhost
- a team that will operate it — the UI, the CLI and the documentation are the best in this folder
- one workload needs replay and running a second platform is not worth it — Streams

## When not to use it

- **microsecond latency or a tiny footprint** — [NATS](../nats/README.md)
- **JMS clients** — [ActiveMQ Artemis](../activemq-artemis/README.md)
- an event log as a first-order requirement, across many teams — that is
  [`data-streaming/`](../../../../data-streaming/README.md), and Streams is not a Kafka substitute
- millions of tiny short-lived queues — Erlang handles a lot, but quorum queues each carry a Raft
  cluster

## Notes

Recorded links:

- <https://github.com/rabbitmq/rabbitmq-server> — the broker. Erlang/OTP, which is why clustering
  and process isolation are as good as they are, and why the runtime is unlike anything else here.
- <https://github.com/rabbitmq/cluster-operator> — the **cluster operator**.
- <https://github.com/rabbitmq/messaging-topology-operator> — the **messaging topology operator**.
- <https://github.com/pika/pika> — the standard Python client, synchronous and AMQP 0-9-1. Used in
  the notebook under [`rabbitmq/`](rabbitmq/README.md).

### The two operators, and why the second one is the interesting part

They are separate projects and they answer different questions:

| | **Cluster operator** | **Messaging topology operator** |
|---|---|---|
| Question answered | "who runs the cluster?" | "who creates the queues?" |
| CRD | `RabbitmqCluster` | `Queue`, `Exchange`, `Binding`, `Policy`, `User`, `Permission`, `Vhost`, `Federation`, `Shovel`, `SchemaReplication`, `SuperStream` |
| Reconciles | StatefulSet, PVCs, services, credentials, rolling upgrades | objects **inside** a running broker, via its HTTP API |
| Without it | you deploy a chart instead | topology is created by application code, the UI, or `rabbitmqadmin` |

The cluster operator is a convenience: it replaces a Helm chart with a CRD, adds proper rolling
upgrades and manages the generated credentials.

**The topology operator changes something real.** Queues, exchanges, bindings, users and
permissions stop being things somebody clicked in the management UI and become Kubernetes
resources under review in Git. That converts the most common category of RabbitMQ incident —
"the queue on production was declared with different arguments" — into a diff.

It matters most for the arguments that **cannot be changed after declaration**: queue type
(`quorum` vs classic), durability, `x-dead-letter-exchange`, `delivery-limit`, `max-length`.
Changing any of them means deleting and recreating the queue. A queue declared by whichever
application connected first is a queue whose critical properties were decided by accident; a queue
declared as a `Queue` resource was reviewed.

The catch is worth stating plainly: application code that declares its own queues at startup will
happily fight the operator, and the declaration that wins is whichever ran last. Adopting the
topology operator means **removing declarations from application code**, not adding CRDs alongside
them.

Details of both deployment shapes: [`rabbitmq/`](rabbitmq/README.md) for the chart,
[`rabbitmq-cluster-operator/`](rabbitmq-cluster-operator/README.md) for the operators.

## Deployment

| Folder | Approach |
|---|---|
| [`rabbitmq/`](rabbitmq/README.md) | the Bitnami Helm chart directly — one cluster, stream plugins enabled, and the working Python examples |
| [`rabbitmq-cluster-operator/`](rabbitmq-cluster-operator/README.md) | the cluster operator **and** the messaging topology operator — clusters and topology as Kubernetes resources |

---

[← Broker](../README.md)
