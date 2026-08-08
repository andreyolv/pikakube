[← Events](../README.md)

# kspan

<https://github.com/weaveworks-experiments/kspan>

---

> **Experimental**, from Weaveworks, which ceased operations in 2024. Mapped for the idea
> rather than for production use.

## The problem it solves

Cluster events and application traces live on separate timelines. During an incident you have
a latency spike in Tempo and a node eviction in the events, and correlating them is manual —
comparing timestamps across two tools.

kspan converts Kubernetes events into **OpenTelemetry spans**, so they land in the tracing
backend alongside application traces. A pod eviction and the request slowdown it caused then
appear on the same timeline, in the same view.

## When to use it

- as a concept worth understanding: signal boundaries are a tooling artefact, not a property of reality
- experimentation, where OpenTelemetry is already the backbone

## When not to use it

- production — it is experimental and its parent company is gone
- routine event retention, which [kubernetes-event-exporter](../kubernetes-event-exporter/) does reliably

## Why the idea outlived the project

Putting infrastructure events on the trace timeline is a genuinely good instinct, and it has
since shown up in more actively maintained forms. Worth knowing the pattern exists when
evaluating anything in [`tracing/`](../../tracing/README.md).

---

[← Events](../README.md)
