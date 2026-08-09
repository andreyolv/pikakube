[← Platforms](../README.md)

# Conduktor Console

<https://github.com/conduktor/conduktor-platform>
<https://github.com/conduktor/conduktor-public-charts/>

---

## The problem it solves

Kafka has no usable interface for anyone who is not operating it. Browsing a topic, checking
consumer lag, or finding out why a consumer is stuck all require CLI tools, a broker
connection, and knowing which flags to use.

The practical consequence is that **two people can work with Kafka**, and everyone else opens a
ticket.

Conduktor Console sits in front of an existing cluster — it does not replace anything:

| Capability | Detail |
|---|---|
| Topic browsing | inspect messages, with schema-aware deserialisation |
| **Consumer groups** | lag per partition, and where a consumer is stuck |
| **RBAC over Kafka** | who may read which topic, enforced by the console |
| Schema registry integration | schemas alongside the messages they describe |
| Audit | who did what |

The RBAC row is the differentiator against a plain UI. It gives read access to a topic without
giving cluster credentials, which is the thing that actually blocks wider access.

## When to use it

- **more people need to work with Kafka** than currently can safely
- consumer lag investigation is a recurring support request
- governance over who can see which topic, without handing out broker credentials

## When not to use it

- open source is a requirement — the console is commercial beyond a limited tier. [Redpanda Console](../../event-streaming/redpanda/redpanda-operator/README.md) works against Kafka and is a lighter alternative
- the team operating Kafka is the only team using it
- you want a platform rather than a UI — see [`../README.md`](../README.md)

## The gap it addresses in this repository

Kafka runs here with Strimzi, with topic and user governance. What is missing is the
**interface**: nothing lets a data engineer inspect a topic or diagnose a stuck consumer without
CLI access to the cluster.

That is the actual pain a console solves, and it is worth separating from the question of
whether to adopt a full platform — see
[`../README.md`](../README.md#the-middle-path).

---

[← Platforms](../README.md)
