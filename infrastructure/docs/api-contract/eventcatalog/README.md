[← API contracts](../README.md)

# EventCatalog

<https://github.com/event-catalog/eventcatalog>

---

## The problem it solves

An [AsyncAPI](../asyncapi/README.md) document describes one interface. It does not answer the
question people actually ask before changing anything:

> **Who consumes this, and what breaks if I change it?**

In an event-driven system that question is genuinely hard, because consumers are decoupled by
design. Nothing in Kafka records who reads a topic and why, and the answer usually comes from
asking around.

EventCatalog turns a set of AsyncAPI documents into a **browsable domain map** — services,
the events they publish, the events they consume, and the schemas involved, with the
relationships drawn.

| It shows | Which answers |
|---|---|
| **Producers and consumers per event** | who breaks if this changes |
| Events per service | what this service is responsible for |
| **Schema versions and history** | what changed, and when |
| Ownership | who to ask |
| Domain grouping | how the landscape is organised |
| Visualisations | the flow between services |

## When to use it

- an event-driven platform with **enough services that the landscape is not in one head**
- schema changes require finding consumers, and that is currently a Slack message
- ownership of topics is unclear, which is the usual state
- AsyncAPI documents already exist, or writing them is planned

## When not to use it

- a handful of topics with known consumers
- there are no AsyncAPI documents, and none are coming — it consumes them, it does not create
  them
- the actual need is enforcing payload compatibility — that is a
  [schema registry](../../../data-streaming/schema-registry/README.md)
- REST-only architecture; nothing here applies

## What it is not

Worth being precise, because the boundary with adjacent tools gets blurred:

| | EventCatalog | Schema registry | Data catalogue |
|---|---|---|---|
| Scope | events and services | payload schemas | datasets and tables |
| Enforces | nothing | **compatibility** | nothing |
| Answers | who produces and consumes | is this message valid | where did this data come from |
| Runs | a static site, in CI | in the cluster | as a service |

It is documentation, generated and published. It cannot prevent a breaking change — it makes the
blast radius visible before someone ships one.

For the third column, see [`data-governance/`](../../../data-governance/README.md): lineage and dataset
ownership are a related concern at a different layer.

## Notes

Not deployed, and it is the natural third step of the sequence in
[`asyncapi/`](../asyncapi/README.md):

1. AsyncAPI documents for the topics that cross a team boundary
2. **EventCatalog** to render them as a map
3. Compatibility enforced by the registry, semantics and ownership by the specs

Step 2 is what changes behaviour. This repository's streaming layer —
[`data-streaming/`](../../../data-streaming/README.md) — already documents that partition keys,
retention and compatibility mode are decisions with permanent consequences. The missing piece is
knowing *who is affected* when one of them is revisited.

Because it builds a static site from files in the repository, it requires nothing running in the
cluster — which makes it unusually cheap for what it answers.

---

[← API contracts](../README.md)
