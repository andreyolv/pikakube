[← API contracts](../README.md)

# OpenAPI

<https://github.com/OAI/OpenAPI-Specification>

---

## What it is

The specification for describing **HTTP APIs** in a machine-readable document — paths,
operations, parameters, request and response schemas, authentication.

It is not documentation in the sense of prose. It is a data file that documentation, clients,
servers, validators and tests are all generated from.

Formerly Swagger, and the old name persists in the tooling — [Swagger UI](../swagger-ui/README.md)
is a renderer for OpenAPI documents, not a separate format.

## What it enables

| Output | How it changes things |
|---|---|
| **Reference documentation** | generated, so it cannot drift from the spec |
| **Client SDKs** | consumers get typed clients rather than hand-written HTTP calls |
| Server stubs | routing and validation scaffolded from the contract |
| **Request validation** | a non-conforming request is rejected at the edge, not misinterpreted |
| **Breaking-change detection** | diff two versions in CI, and fail the build |
| Mock servers | consumers build against the contract before it exists |
| Contract tests | verify the implementation still matches |

The fourth and fifth rows are where the return is. Validation at the gateway means malformed
input never reaches application code; breaking-change detection turns an argument in code review
into a pipeline result.

## When to use it

- **any HTTP API with a consumer who is not you**
- more than one team is involved, so the contract needs agreeing before building
- a gateway can enforce the schema — see [`network/`](../../../network/README.md)
- typed clients would remove a class of integration bug

## When not to use it

- **event-driven interfaces** — that is [AsyncAPI](../asyncapi/README.md)
- gRPC, which has protobuf as its own contract
- GraphQL, whose schema is already the contract
- an internal endpoint with one caller in the same repository, where the types are shared already

## Spec-first or code-first

The recurring question, addressed in [`../README.md`](../README.md#3-spec-first-or-code-first).
The short version:

**Spec-first between teams.** The contract is written and reviewed before either side builds,
which is where the value is — the expensive part of an integration is discovering the mismatch
late.

**Code-first inside one team.** Annotations generate the spec, and it cannot drift because it is
derived. The cost is that nobody designed the API; its accidents become its contract.

## Practical notes

| Concern | Detail |
|---|---|
| **Version** | 3.1 aligns with JSON Schema; 3.0 does not, and the difference matters for tooling |
| Splitting the file | `$ref` across files keeps it maintainable; the tooling support varies |
| Examples | put them in the spec, so the generated documentation shows working ones |
| **Linting** | Spectral for style and consistency rules |
| Breaking changes | `oasdiff` or similar, in CI — this is the check worth having |
| Security schemes | describe authentication in the spec, or every consumer guesses |

The linting row matters more than it sounds. A spec assembled by several people drifts in naming,
pagination and error shapes, and those inconsistencies become permanent once consumers depend on
them.

## Notes

Mapped rather than used. This repository is infrastructure rather than services, so there is no
HTTP API of its own to specify.

Where it does connect: several platform components expose APIs that a gateway would validate
against — see [`network/`](../../../network/README.md) for the API gateway and Gateway API
folders, where schema validation at the edge is one of the capabilities being compared.

For this platform, the sibling specification is the one with real value:
[AsyncAPI](../asyncapi/README.md), because the interfaces that actually cross team boundaries
here are Kafka topics, and they are undocumented in a way REST endpoints rarely are.

---

[← API contracts](../README.md)
