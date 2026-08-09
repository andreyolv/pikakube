[← Event streaming](../README.md)

# Redpanda

<https://github.com/redpanda-data/redpanda>
<https://github.com/redpanda-data/helm-charts>
<https://docs.redpanda.com/>

Deployment: [`redpanda/`](redpanda/README.md) · [`redpanda-operator/`](redpanda-operator/README.md)

Related: [console](https://github.com/redpanda-data/console) ·
[connect](https://github.com/redpanda-data/connect)

---

## The problem it solves

Kafka's protocol, without Kafka's operational surface.

Written in C++ with a thread-per-core architecture: **no JVM, no ZooKeeper, no separate
controller quorum to operate**. One binary per node, and clients cannot tell the difference —
it speaks the Kafka protocol, so existing producers, consumers and tooling connect unchanged.

| Removed | Consequence |
|---|---|
| The JVM | no heap tuning, no GC pauses in the tail latency |
| ZooKeeper | one fewer distributed system to run and back up |
| Page-cache dependence | it manages memory and IO directly, which makes latency predictable |

The latency argument is the one that holds up: p99 is markedly more stable, because there is no
garbage collector deciding otherwise.

## When to use it

- Kafka semantics with **substantially less to operate**
- latency consistency matters, not just throughput
- small teams where nobody wants to become a Kafka specialist
- existing Kafka clients must keep working

## When not to use it

- the **JVM ecosystem around Kafka** is the reason you are there — Kafka Streams, and JVM-native integrations
- Strimzi already runs Kafka well and there is no pain to solve
- multi-tenancy at the level [Pulsar](../pulsar/README.md) provides
- elasticity through object storage is the goal — [AutoMQ](../automq/README.md)

## The included pieces

**Console** is a genuinely good Kafka UI — topic browsing, consumer groups, schema registry
integration — and it works against Kafka as well, which makes it worth knowing about
independently. See [`platforms/`](../../platforms/README.md), where the missing management
interface is the gap this repository actually has.

**Connect** is the successor to [Benthos](../../processing/benthos/README.md), now maintained by
Redpanda — declarative stream plumbing, and the right tool for the stateless majority of
streaming work.

## Deployment

| Folder | Approach |
|---|---|
| [`redpanda/`](redpanda/README.md) | Helm chart directly |
| [`redpanda-operator/`](redpanda-operator/README.md) | operator-managed clusters |

---

[← Event streaming](../README.md)
