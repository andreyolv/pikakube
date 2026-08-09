[← Data Streaming](../README.md)

# Schema registry

The contract between producers and consumers.

Tools covered: [`schema-registry`](schema-registry/) · [`apicurio-registry`](apicurio-registry/README.md) ·
[`karapace`](karapace/README.md)

---

## The problem it solves

A topic is bytes. Nothing in Kafka knows or cares what shape they are, so a producer that adds
a required field, renames one, or changes a type breaks every consumer — at runtime, in
production, usually at night.

A schema registry makes the shape **explicit and enforced**:

| Capability | What it prevents |
|---|---|
| Schemas stored and versioned centrally | consumers guessing, or hardcoding the shape |
| **Compatibility checking** | a producer publishing a change that breaks existing consumers |
| Schema ID in the message | consumers resolving the exact version that was written |
| Evolution rules | ad-hoc changes that work for the author and nobody else |

The compatibility check is the actual product. Registration without enforcement is
documentation.

## Compatibility modes

The setting that decides what producers may do, and it is worth understanding before choosing
one:

| Mode | Means | Safe to |
|---|---|---|
| **BACKWARD** | new schema can read old data | upgrade **consumers** first |
| **FORWARD** | old schema can read new data | upgrade **producers** first |
| **FULL** | both | upgrade in any order |
| NONE | no checking | nothing — this is the default that causes the outage |

`BACKWARD` is the usual choice, because consumers are typically upgraded before producers. But
the mode is a **deployment-order decision**, not a preference — and picking one without knowing
which side upgrades first is how a "compatible" change still breaks production.

## Formats

| Format | Notes |
|---|---|
| **Avro** | the Kafka default; compact, schema always required, strong evolution rules |
| **Protobuf** | widely used beyond Kafka, good tooling, strong typing |
| **JSON Schema** | readable and verbose; weakest evolution guarantees |

Avro's requirement that a schema always be present is a feature here — it makes schemaless
messages impossible rather than merely discouraged.

## The tools

| Tool | Notes | Detail |
|---|---|---|
| **Confluent Schema Registry** | the reference implementation; check the licence for the version you deploy | [→](schema-registry/) |
| **Apicurio Registry** | Apache-2.0, broader artefact support beyond schemas — OpenAPI, AsyncAPI | [→](apicurio-registry/README.md) |
| **Karapace** | Apache-2.0 drop-in replacement for the Confluent API | [→](karapace/README.md) |

**Karapace exists because of the licensing question.** It speaks the same API, so clients do not
change — which makes it the straightforward answer when Apache licensing is required.

**Apicurio is broader than schemas**, registering API contracts too, which matters if the
platform wants one place for all interface definitions rather than one per protocol.

## The structural weakness

In the conventional setup the registry is **advisory**. A producer that skips it can publish
anything, and the first indication is a consumer failing to deserialise.

Two ways to close that gap:

- discipline and client configuration — the usual approach, and it depends on nobody bypassing it
- **broker-side enforcement** — [Bufstream](../event-streaming/bufstream/README.md) validates at the broker, so invalid messages never enter the log

Worth knowing the second option exists, because "we have a schema registry" and "invalid
messages cannot be published" are different statements.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| No registry at all | one producer change breaks every consumer, discovered in production | register and enforce |
| Compatibility set to `NONE` | the registry becomes documentation | pick a mode from your deployment order |
| Choosing a mode without knowing upgrade order | "compatible" changes still break things | `BACKWARD` if consumers go first, `FORWARD` if producers do |
| Schemas not in version control | the registry becomes the only source of truth, and it is mutable | schemas in Git, registered from CI |
| Adding a required field | it breaks old consumers under every mode | optional fields with defaults |
| Reusing a topic for a different event type | the schema stops meaning anything | one event type per topic |

## How this applies to pikakube

Kafka with Strimzi is deployed; the registry is mapped rather than run.

Worth recording as a genuine gap rather than an omission: **topic and user governance exists in
this repository, schema governance does not**. Access is controlled, and the shape of the data
flowing through those topics is not — which is the same class of problem one level up.

If it were adopted, **Karapace** is the low-friction path: Apache-licensed, and the API is
compatible so clients do not change.

---

[← Data Streaming](../README.md)
