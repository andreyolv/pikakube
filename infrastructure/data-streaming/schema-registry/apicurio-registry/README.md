[← Schema registry](../README.md)

# Apicurio Registry

<https://github.com/Apicurio/apicurio-registry>
<https://github.com/Apicurio/apicurio-registry-operator>
<https://github.com/eshepelyuk/apicurio-registry-helm>

---

## What it is

Apache-2.0, and broader than a schema registry: it stores **API contracts of every kind** —
Avro, Protobuf and JSON Schema, plus OpenAPI, AsyncAPI, GraphQL and WSDL.

That breadth is the argument. A platform ends up with schemas in one registry, OpenAPI specs in
a repository somewhere, and AsyncAPI definitions nowhere — Apicurio is one place for all of it,
with versioning and compatibility rules applied uniformly.

| Supports | Where it usually lives otherwise |
|---|---|
| Avro, Protobuf, JSON Schema | a Kafka schema registry |
| **OpenAPI** | a repository, or a wiki |
| **AsyncAPI** | typically nowhere |
| GraphQL, WSDL | scattered |

It also provides a Confluent-compatible API, so Kafka clients work unchanged.

## When to use it

- **all interface definitions** should live in one governed place, not just Kafka schemas
- AsyncAPI matters — event-driven contracts documented as deliberately as REST ones
- Apache licensing, with an operator for Kubernetes

## When not to use it

- Kafka schemas are the only requirement — [Karapace](../karapace/README.md) is smaller and does exactly that
- broker-side enforcement is what you need — [Bufstream](../../event-streaming/bufstream/README.md)

## Karapace or Apicurio

| | [Karapace](../karapace/README.md) | Apicurio |
|---|---|---|
| Scope | Kafka schemas, plus REST proxy | **any API contract** |
| Footprint | smaller | larger |
| Operator | no | **yes** |
| Choose it when | you want a drop-in registry | contracts are a platform-wide concern |

## Where this connects

The interesting angle for a data platform: **AsyncAPI is the contract for event-driven
integration**, and it is almost universally undocumented. Kafka topics have owners, schemas and
semantics that live in people's heads.

Registering them alongside REST contracts turns "what does this topic contain and who owns it"
into a query rather than a conversation — which is the same goal as
[`data-governance/`](../../../data-governance/README.md), applied to interfaces.

---

[← Schema registry](../README.md)
