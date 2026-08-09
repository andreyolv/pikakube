[← NATS](../README.md)

# NUI

<https://github.com/nats-nui/nui>
<https://github.com/nats-nui/k8s>

Client: [nats.py](https://github.com/nats-io/nats.py)

---

## The problem it solves

[NATS](../README.md) ships no web interface. The server exposes a monitoring HTTP endpoint and
there is the `nats` CLI, but there is nothing equivalent to RabbitMQ's management UI — and that
gap is felt immediately, because NATS subjects are invisible by design. Nothing is declared, so
there is no list of "what exists" to read.

NUI is that missing interface:

| What it gives you | Why it matters |
|---|---|
| **Publish and subscribe from the browser** | check a subject is live without writing a client |
| Live message view | see what is actually flowing, with wildcards like `orders.>` |
| **JetStream browsing** | streams, consumers, their configuration and pending counts |
| Message inspection on a stream | read stored messages by sequence — the replay story, visible |
| KV and object store browsing | the JetStream-backed stores, inspectable |
| Several connections | dev, staging and production from one place |

The honest positioning: this is a **development and debugging tool**, not monitoring. It answers
"is anything being published on this subject" and "why is this consumer not acknowledging" in
seconds — questions that otherwise mean writing a throwaway script. It does not replace metrics
and alerts; see [`observability/`](../../../../../observability/README.md).

## When to use it

- developing against NATS, where seeing live messages shortens every debugging loop
- **JetStream** is in use — stream and consumer state is genuinely hard to reason about from the CLI
- onboarding: it makes an otherwise invisible subject space concrete
- verifying a consumer's pending and redelivery counts during an incident

## When not to use it

- as monitoring — it is a UI a human opens, and nobody has it open at 03:00
- exposed publicly without authentication in front of it: it can **publish** to any subject and
  read any stream, which makes it a write path into the broker, not a dashboard
- for automation — the `nats` CLI is the scriptable interface, and belongs in CI

## Notes

Recorded links:

- <https://github.com/nats-nui/nui> — the application itself.
- <https://github.com/nats-nui/k8s> — the Helm chart repository, and the source of the `nui`
  chart used here. Its `values.yaml` is the reference for configuring the connection to the
  server.
- <https://github.com/nats-io/nats.py> — the Python client for NATS. Recorded alongside NUI
  because they answer the same need from two directions: NUI to look at a subject by hand,
  `nats.py` to produce and consume from code. Async and `asyncio`-based, with JetStream available
  as `nc.jetstream()` on the same connection.

In this repository NUI is a Flux `HelmRelease` deployed into the **`nats` namespace**, next to
the server it inspects. Reaching it is a `port-forward` rather than an Ingress, which is the
right default given that it can publish to any subject.

---

[← NATS](../README.md)
