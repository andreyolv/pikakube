[← API contracts](../README.md)

# Swagger UI

<https://github.com/swagger-api/swagger-ui>

---

## What it is

A renderer for [OpenAPI](../openapi/README.md) documents, and the one distinguishing feature is
**Try it out**: every operation becomes a form that sends a real request from the browser and
shows the real response.

That is the difference between a reference someone reads and an API someone learns. Reading a
schema tells you the shape; calling the endpoint and seeing what comes back tells you what it
means.

## When to use it

- developers need to **explore** the API, not just look up a field
- an internal API where a live console against a development environment is a fair thing to
  expose
- onboarding, where the fastest path to understanding is making a call
- there is a sandbox environment safe to call from a browser

## When not to use it

- a **readable reference document**, meant to be read end to end —
  [Redoc](../redoc/README.md) is better at that
- exposing an interactive console against production, unless that is a deliberate decision with
  authentication in front
- event-driven interfaces — [AsyncAPI](../asyncapi/README.md) and its renderers

## Swagger UI or Redoc

They render the same document and are good at different jobs:

| | Swagger UI | Redoc |
|---|---|---|
| Layout | operations expanded in a list | **three-panel**, reference-style |
| Try it out | **yes** | no |
| Reading a long spec | tiring | pleasant |
| Nested schemas | workable | clearer |
| Best for | **learning and exploring** | **looking things up** |

Publishing both is common and not a failure to decide — they serve the developer integrating for
the first time and the developer checking a field name six months later.

## What to be careful with

| Concern | Detail |
|---|---|
| **Which server it points at** | the `servers` block decides what Try it out calls; production by accident is a real outcome |
| Authentication | the console needs credentials, and the browser is where they end up |
| CORS | calling from the documentation origin requires it to be allowed |
| Exposure | an interactive console on a public site is an interactive console for everyone |
| Version drift | it renders whatever spec it is given; serve the one matching the deployment |

The first row is the one that causes incidents. A spec listing production first, rendered on an
internal documentation site, gives everyone a one-click production client.

## Notes

Mapped rather than deployed. This repository is infrastructure rather than services, so there is
no OpenAPI document of its own to render.

Worth knowing that many platform components ship it already — Kubernetes itself, several
operators, and a number of the tools catalogued here expose a Swagger UI at some path. That is
usually the fastest way to explore an unfamiliar component's API, and it is also worth checking
whether it is exposed where it should not be.

---

[← API contracts](../README.md)
