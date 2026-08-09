[← AI gateway](../README.md)

# envoyproxy/ai-gateway

<https://github.com/envoyproxy/ai-gateway>

---

**This folder duplicates [`envoy-ai-gateway/`](../envoy-ai-gateway/README.md).** Same project,
two directories: this one holds the GitHub link, the other holds the deployment manifests and
the documentation link. The full write-up lives there — read it instead of this page.

Recorded as an observation about the folder layout, not as a change. Which of the two survives
is a decision for whoever consolidates them; the one with the manifests is the obvious keeper.

---

## The problem it solves

See [`envoy-ai-gateway/`](../envoy-ai-gateway/README.md). In one paragraph: applications call
many LLM providers, each with its own SDK, key, quota and price. Envoy AI Gateway puts one
Envoy-based hop in front of all of them, built as an extension of Envoy Gateway so it inherits
Gateway API, and adds the AI-specific pieces on top — a unified OpenAI-shaped API, provider
credentials held centrally, failover between backends, per-team token metrics, and rate limiting
measured in **tokens rather than requests**.

## When to use it

See [`envoy-ai-gateway/`](../envoy-ai-gateway/README.md). Short version: when the cluster
already speaks Gateway API, when more than one provider is in play, and when someone needs to
answer "which team spent that".

## When not to use it

See [`envoy-ai-gateway/`](../envoy-ai-gateway/README.md). Short version: one application calling
one provider does not need a gateway, and a cluster that does not run Gateway API is paying for
a control plane it did not otherwise want — [Higress](../higress/README.md) is the more
self-contained option in that case.

## Notes

The only thing recorded in this folder's original notes was the project URL:

- <https://github.com/envoyproxy/ai-gateway> — the Envoy AI Gateway repository, from the Envoy
  project itself rather than a vendor fork. That provenance is the main argument for it over the
  other options in this folder: the data plane is Envoy, and the control plane is Envoy Gateway.

Nothing is deployed from this folder. The manifests are in
[`envoy-ai-gateway/`](../envoy-ai-gateway/README.md), pinned at `v0.6.0`.

---

[← AI gateway](../README.md)
