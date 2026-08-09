[← Broker](../README.md)

# NATS

<https://github.com/nats-io/nats-server>
<https://github.com/nats-io/k8s>

Web interface: [`nui/`](nui/README.md)

Client: [nats.py](https://github.com/nats-io/nats.py)

---

## The problem it solves

Messaging with **almost nothing to operate**.

A single Go binary, a few megabytes, no ZooKeeper, no JVM, no external dependency. Subjects are
not declared, provisioned or configured — publishing to `orders.eu.created` requires no prior
setup, and a subscriber to `orders.>` receives it.

What comes out of that:

| Property | Consequence |
|---|---|
| **Nothing is declared** | no exchange, binding or queue to create before publishing |
| Subject wildcards | `*` matches one token, `>` matches the rest — filtering is in the subscription |
| **Request/reply is native** | a protocol operation, not a reply queue plus a correlation id |
| Queue groups | several subscribers on the same subject share the load, competing-consumer style |
| Clustering and leaf nodes | superclusters and edge topologies are configuration, not architecture |

The trade-off is stated up front by NATS itself: **Core NATS is at most once**. If no subscriber is
connected, the message is gone — no error, no queue, no retry. That is a deliberate design for
telemetry, discovery and RPC, and a silent data-loss bug for anything else.

**JetStream** is the answer to that, and it is part of the same binary — a subsystem that adds
streams with file or memory storage, replication, per-consumer acknowledgements, redelivery and
replay from an offset or a timestamp. It also provides a key-value store and an object store,
both built on streams.

The rule worth memorising: **Core for fire-and-forget, JetStream for anything durable.** The
detail is in [`broker/`](../README.md#5-nats-core-vs-jetstream).

## When to use it

- latency and footprint are real constraints
- **request/reply** between services, where NATS is genuinely simpler than everything else
- many subjects with hierarchical names, filtered by wildcards rather than by broker config
- edge, multi-cluster or multi-region topologies — leaf nodes are built for this
- microservice telemetry, health and discovery traffic, where Core NATS is exactly right

## When not to use it

- **AMQP is required** — NATS speaks its own protocol only; use
  [RabbitMQ](../rabbitmq/README.md) or [ActiveMQ Artemis](../activemq-artemis/README.md)
- rich broker-side routing, per-message TTL, priorities, dead-letter exchanges — RabbitMQ's model
  is far more complete and its tooling far more mature
- **JMS clients** — [ActiveMQ Artemis](../activemq-artemis/README.md)
- event streaming as a first-order platform requirement — JetStream stretches that way, but
  [`data-streaming/`](../../../../data-streaming/README.md) is the discipline for it
- a team that will reach for Core NATS and assume messages are stored — the default is not what
  most people expect from a "message broker"

## Notes

Recorded links:

- <https://github.com/nats-io/nats-server> — the broker itself. Single Go binary; JetStream is
  built in and enabled by configuration, not a separate product.
- <https://github.com/nats-io/k8s> — the official Kubernetes repository, and the source of the
  **`nats` Helm chart** used here. Worth reading its `values.yaml` directly: JetStream, its
  storage class and volume size, and cluster replicas are all off or minimal by default.
- <https://github.com/nats-io/nats.py> — the Python client (also recorded under
  [`nui/`](nui/README.md)). Async, `asyncio`-based, with the JetStream API exposed as
  `nc.jetstream()`. The same library covers Core and JetStream, so moving from fire-and-forget to
  durable is a change of call, not of dependency.

In this repository NATS is a Flux `HelmRelease` on the `nats` chart in the `nats` namespace, with
[NUI](nui/README.md) deployed into the same namespace as its web interface.

If JetStream is enabled here, two things must be set deliberately, because neither can be fixed
comfortably later: the **storage class and volume size** for the stream files, and the **number
of replicas** — a stream replicated across three nodes survives losing one, a stream with one
replica does not.

---

[← Broker](../README.md)
