[← Event streaming](../README.md)

# Apache Pulsar

<https://github.com/apache/pulsar>
<https://github.com/apache/pulsar-helm-chart>
<https://pulsar.apache.org/>

---

## The problem it solves

Kafka couples storage to brokers: a partition lives on specific brokers, so scaling means
moving data and rebalancing is a data-movement operation.

Pulsar separates them. Brokers are **stateless** serving nodes; storage is BookKeeper, in
segments. Adding a broker adds serving capacity immediately, with no data to move.

On top of that, two things Kafka does not have natively:

| Capability | Detail |
|---|---|
| **Multi-tenancy** | tenants, namespaces and topics as a real hierarchy, with quotas and isolation per tenant |
| **Tiered storage** | old segments offloaded to object storage automatically, so retention is not bounded by broker disk |
| Geo-replication | built in, rather than assembled with MirrorMaker |
| Queue **and** stream semantics | shared subscriptions behave like a queue; exclusive like a log |

The subscription model is genuinely broader than Kafka's consumer groups — the same topic can
be consumed as a work queue or as an ordered log, depending on the subscription type.

## When to use it

- **multi-tenancy** is a first-order requirement — many teams, one platform, with isolation
- **geo-replication** across regions
- retention beyond what broker disks allow, without operating tiered storage separately
- both queue and stream patterns are needed

## When not to use it

- **the ecosystem.** Kafka's is far larger — connectors, clients, tooling, documented answers, and people who have run it
- operational simplicity is the goal; Pulsar has more components (brokers, BookKeeper, ZooKeeper or its replacement)
- Kafka compatibility matters — [Redpanda](../redpanda/README.md) or [AutoMQ](../automq/README.md) keep the protocol

## The honest comparison

Pulsar is arguably the better architecture. Kafka has the ecosystem, and in practice the
ecosystem wins most decisions — connectors that already exist, clients that are already
battle-tested, and answers that already exist when something breaks.

The cases where Pulsar is clearly right are the ones its architecture was designed for:
**multi-tenancy and geo-replication**, where Kafka requires assembling what Pulsar includes.

---

[← Event streaming](../README.md)
