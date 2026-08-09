[← API contracts](../README.md)

# Redoc

<https://github.com/Redocly/redoc>

---

## What it is

A renderer for [OpenAPI](../openapi/README.md) documents that produces a **reference document**
rather than a console: three panels — navigation, description, and examples — laid out to be read.

Where [Swagger UI](../swagger-ui/README.md) optimises for calling the endpoint, Redoc optimises
for understanding it. Nested schemas expand cleanly, descriptions get room, and a long
specification stays navigable.

## When to use it

- **published API documentation** with an audience that reads before integrating
- specifications with deeply nested schemas, which Swagger UI renders awkwardly
- documentation that should look like a product rather than a debugging tool
- a static page is wanted, with no interactive console to secure

## When not to use it

- developers should be able to **call** the endpoint from the page —
  [Swagger UI](../swagger-ui/README.md)
- an internal sandbox where exploration matters more than presentation
- event-driven interfaces — [AsyncAPI](../asyncapi/README.md)

## Practical notes

| Concern | Detail |
|---|---|
| **Single-file output** | `redoc-cli bundle` produces one self-contained HTML file, which is trivial to host |
| Descriptions | it gives them real space, so a spec with good descriptions looks good and a bare one looks empty |
| `x-` extensions | code samples, logos and tag grouping via vendor extensions |
| Tag ordering | controls the navigation; without it the order is arbitrary |
| Open source vs. Redocly | the renderer is open source; the surrounding platform is commercial |

The second row is worth acting on. Redoc rewards a specification that has been written rather
than merely generated — descriptions, examples and tag grouping are what fill the layout. A
code-first spec with no prose renders as a lot of whitespace.

## Publishing both

Not indecision. The two renderers answer different questions:

| Reader | Wants | Tool |
|---|---|---|
| Integrating for the first time | to call it and see what happens | Swagger UI |
| Checking a field six months later | to find it quickly and read the constraints | Redoc |

Both build from the same document, so publishing both costs one extra CI step.

## Notes

Mapped rather than deployed, for the same reason as the rest of this folder — this repository is
infrastructure, and there is no API of its own to document.

The pairing to remember: **Redoc for the published reference, Swagger UI for the sandbox.** If
only one is deployed, the deciding question is whether the audience needs to call the API or
read about it.

---

[← API contracts](../README.md)
