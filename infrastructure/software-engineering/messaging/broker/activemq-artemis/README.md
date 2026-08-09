[← Broker](../README.md)

# ActiveMQ Artemis

<https://github.com/apache/activemq>
<https://github.com/apache/activemq-artemis>

---

## The problem it solves

**One broker, many protocols** — and a home for JMS.

Artemis is the next-generation ActiveMQ broker (the "classic" ActiveMQ in the first repository is
the older codebase). Its distinguishing feature is that clients speaking entirely different wire
protocols use the same addresses and the same queues:

| Protocol | Who brings it |
|---|---|
| **AMQP 1.0** | the standardised wire protocol — .NET, Python, Go, Qpid clients |
| **JMS 2.0** | Java applications, usually an existing estate |
| **MQTT** | devices and IoT |
| **STOMP** | scripting languages and browsers via WebSocket |
| **OpenWire** | ActiveMQ Classic clients, for migration |

Internally it uses an *address* model rather than AMQP 0-9-1's exchange model: an address has
routing type `anycast` (queue semantics — one consumer gets it) or `multicast` (topic semantics —
every subscriber gets a copy). That is deliberately more abstract than
[RabbitMQ's exchanges](../rabbitmq/README.md), because it has to express the same thing for five
protocols at once.

The other genuine strength is **JMS**. If Java services already use `javax.jms` / `jakarta.jms`,
Artemis is a drop-in destination; RabbitMQ and NATS are not.

## When to use it

- an existing **JMS** estate that is not being rewritten
- several client ecosystems — MQTT devices and AMQP services — must reach **one** broker
- migrating off ActiveMQ Classic, where OpenWire compatibility is what makes the move possible
- large messages and message paging matter, which Artemis handles well

## When not to use it

- **greenfield on Kubernetes in this repository** — see the note below; there is no Helm chart,
  and everything here is a Flux `HelmRelease`
- routing rules are the point — [RabbitMQ](../rabbitmq/README.md)'s exchange and binding model is
  more direct and far better documented
- latency and footprint are the constraint — [NATS](../nats/README.md)
- an event log with replay — [`data-streaming/`](../../../../data-streaming/README.md)

## Notes

Recorded during evaluation:

> **no helm chart**

That is the whole finding, and in this repository it is decisive rather than inconvenient.

Every other broker here is installed as a Flux `HelmRelease` pointing at a `HelmRepository`. There
is no upstream Helm chart for Artemis, so that path does not exist. The supported way to run it on
Kubernetes is **ArtemisCloud**, an operator, which changes the shape of the deployment:

| | The Helm path used elsewhere here | ArtemisCloud operator |
|---|---|---|
| What Flux installs | the broker itself, from a chart | the **operator**, from its manifests |
| What creates the broker | the chart's values | an `ActiveMQArtemis` custom resource |
| What creates addresses/queues | broker config in values | `ActiveMQArtemisAddress` resources |
| Configuration drift | one `HelmRelease` to review | a controller reconciling CRs |

So adopting Artemis here means adding **two** things to the GitOps tree — the operator's install
manifests (via a Flux `Kustomization`, since there is no chart to release) and the custom resources
that describe the actual broker — rather than one `HelmRelease` like every sibling folder.

That is not a reason to reject it: the operator model is the same one
[`rabbitmq-cluster-operator/`](../rabbitmq/rabbitmq-cluster-operator/README.md) uses, and it makes
addresses and queues Kubernetes resources, which is an advantage. It is a reason to know the cost
before starting — the install is unlike everything else in this repository, and the reason to pay
it should be **JMS or multi-protocol**, not curiosity.

---

[← Broker](../README.md)
