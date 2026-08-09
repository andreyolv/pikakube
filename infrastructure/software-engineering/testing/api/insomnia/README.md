[← API testing](../README.md)

# Insomnia

<https://github.com/Kong/insomnia>

---

## The problem it solves

**A fast, clean API client that covers more than HTTP.**

Insomnia is the middle ground in this folder: a polished desktop client with good support for
**REST, GraphQL, gRPC and WebSocket** in one place — which is more than [Bruno](../bruno/README.md)
covers — without being the platform that [Postman](../postman/README.md) is.

It is maintained by **Kong**, which shows in what it is good at: it sits close to API gateway
workflows, can import and export OpenAPI specifications, and treats a spec as a first-class input
rather than an afterthought.

It ships `inso`, a CLI that runs collections and lints specifications headlessly, so a collection
can become a pipeline stage rather than a desktop-only artefact.

## When to use it

- **gRPC, GraphQL or WebSocket** alongside plain HTTP, in one client
- working from an OpenAPI specification — import it, then exercise the endpoints
- a Kong-based API estate, where the tooling lines up
- a better day-to-day client than Bruno, when git-native storage is not the deciding factor

## When not to use it

- **when the collection must be a reviewable file in git** — that is
  [Bruno](../bruno/README.md)'s reason to exist, and Insomnia's storage model has moved between
  local and cloud-synced across versions
- SOAP and WSDL — [SoapUI](../soapui/README.md)
- team workspaces, mock servers and hosted documentation — [Postman](../postman/README.md)
- **load testing** — [`load/`](../../load/README.md)
- as the whole test suite, in place of [`unit/`](../../unit/README.md)

## Notes

The recorded note is <https://github.com/Kong/insomnia> — a GitHub repository, so it is open source,
and specifically **Kong's**, which was not always the case: the project was independent before Kong
acquired it. That ownership is worth knowing because it explains the API-gateway-shaped features.

The caveat to check before adopting it is **where a given version puts your data**. Insomnia's
default between purely local storage and a cloud-synced account has changed across major releases,
and that is exactly the axis
[`api/`](../README.md) section 2 says is the one that matters. Verify it against the version you
intend to use rather than against a blog post.

Nothing is deployed here — Insomnia is a desktop application. If it is adopted for CI, the artefact
that belongs in a repository is the exported collection plus the `inso` invocation, kept next to the
service it tests.

---

[← API testing](../README.md)
