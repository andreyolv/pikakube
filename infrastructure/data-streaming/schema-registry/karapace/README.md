[← Schema registry](../README.md)

# Karapace

<https://github.com/Aiven-Open/karapace>

---

## The problem it solves

The Confluent Schema Registry is the reference implementation and the licensing is restrictive.
Karapace, from Aiven, is an **Apache-2.0 drop-in replacement**: same REST API, so clients,
serialisers and tooling connect without changes.

It also implements the Confluent REST Proxy API, which is the second piece teams usually need.

| | Confluent Schema Registry | Karapace |
|---|---|---|
| Licence | Confluent Community | **Apache 2.0** |
| API | the reference | **compatible** |
| Client changes | — | none |
| REST Proxy | separate product | included |

## When to use it

- **Apache licensing is required**, which is the main reason it exists
- an existing Confluent Schema Registry needs replacing without touching producers or consumers
- you want one component covering both the registry and the REST proxy

## When not to use it

- broader artefact management is wanted — OpenAPI, AsyncAPI as well as schemas — [Apicurio](../apicurio-registry/README.md)
- broker-side enforcement is the actual requirement — [Bufstream](../../event-streaming/bufstream/README.md), since any registry is advisory

## What to configure

The compatibility mode, and it is a **deployment-order decision** rather than a preference:

| Mode | Safe to upgrade first |
|---|---|
| `BACKWARD` | consumers |
| `FORWARD` | producers |
| `FULL` | either |

`NONE` is the default in some setups and turns the registry into documentation — see
[`../README.md`](../README.md#compatibility-modes).

## The remaining gap

Karapace enforces compatibility **when clients use it**. A producer configured to skip the
registry can still publish anything.

Closing that requires either discipline and client configuration, or broker-side validation.
Worth being explicit about which one you have, because "we run a schema registry" is often
assumed to mean the second.

---

[← Schema registry](../README.md)
