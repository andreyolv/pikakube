[← API contracts](../README.md)

# AsyncAPI

<https://github.com/asyncapi/spec>

---

## The problem it solves

REST endpoints get documented as a matter of course. The Kafka topic carrying the same data does
not — and in most organisations its shape, its owner, its delivery guarantees and its semantics
live entirely in people's heads.

The practical consequence is that *"what is in this topic, who owns it, and what breaks if I
change it?"* is a conversation with whoever has been there longest, rather than a document.

AsyncAPI is [OpenAPI](../openapi/README.md)'s sibling for **event-driven interfaces**:

| | OpenAPI | AsyncAPI |
|---|---|---|
| The unit | paths and operations | **channels and messages** |
| Protocols | HTTP | Kafka, MQTT, AMQP, WebSockets, SSE, NATS |
| Describes | request and response | publish and subscribe, per channel |
| Adoption | near-universal | **rare — which is the opportunity** |

## What goes in the document

| Section | What it records |
|---|---|
| **Channels** | the topics, with their protocol bindings |
| **Messages** | payload schemas — referencing Avro, Protobuf or JSON Schema |
| Operations | who publishes, who subscribes |
| **Bindings** | Kafka specifics: partitions, keys, cleanup policy |
| Servers | the brokers, and their security schemes |
| Tags and descriptions | ownership and semantics — the part nobody writes down |

The bindings section is the one that carries operational value. Partition key and cleanup policy
are decisions with permanent consequences — see
[`data-streaming/`](../../../data-streaming/README.md) — and they are otherwise recorded in a
`Topic` manifest that no consumer ever reads.

## Spec and registry are different things

A recurring confusion, and worth being precise about:

| | Schema registry | AsyncAPI |
|---|---|---|
| Governs | the **payload** | the **interface** around it |
| Enforces | compatibility, at serialisation time | nothing; it documents |
| Answers | "is this message valid?" | "what is this channel, who owns it, what guarantees does it make?" |
| Lives | in the cluster | in the repository |

A topic with a registered Avro schema and no AsyncAPI document has an enforced payload and an
undocumented interface. Both are needed, and they answer different questions.

[Apicurio Registry](../../../data-streaming/schema-registry/apicurio-registry/README.md) stores
both, which is its actual argument over a Kafka-only registry.

## When to use it

- **topics that cross a team boundary** — the ones where a change breaks somebody else
- an event-driven platform where consumers must be discovered before a schema is changed
- generating consumer or producer code from the contract
- documenting event semantics alongside REST, rather than at half the standard

## When not to use it

- internal topics with one producer and one consumer, in the same repository
- HTTP request/response — [OpenAPI](../openapi/README.md)
- as a substitute for a schema registry; it documents, it does not enforce

## Notes

**This is the entry in this folder with real value for this repository.**

The reasoning is already recorded in
[apicurio-registry](../../../data-streaming/schema-registry/apicurio-registry/README.md): event
contracts are almost universally undocumented, Kafka topics have owners and semantics that live
in people's heads, and turning that into a query rather than a conversation is the same goal as
[`data-governance/`](../../../data-governance/README.md) applied to interfaces.

The sequence that would pay off, none of which requires deploying anything to the cluster:

1. **AsyncAPI documents** for the topics that cross a boundary
2. **[EventCatalog](../eventcatalog/README.md)** to render them as a map of producers and
   consumers
3. Compatibility enforced by the registry, ownership and semantics by the spec

Step 2 is the one that changes behaviour, because the question asked before a schema change is
almost never "what fields does this have" and almost always "who breaks?"

---

[← API contracts](../README.md)
