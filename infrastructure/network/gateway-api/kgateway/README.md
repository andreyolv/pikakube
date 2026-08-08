[← Gateway API](../README.md)

# kgateway

<https://github.com/kgateway-dev/kgateway>
<https://kgateway.dev/>

Context and comparison: [../README.md](../README.md)

---

## What it is

An Envoy-based [Gateway API](../README.md) implementation, donated to the CNCF and
continuing the open-source line of Solo.io's [Gloo](../../api-gateway/gloo/) edge.

Its distinguishing focus is **AI and LLM traffic**: routing to model providers, failover
between them, token-based rate limiting, and credential handling at the gateway rather than
in every application.

That is a real and awkward gap — normal rate limiting counts requests, while LLM cost is
driven by tokens, and normal failover does not understand a provider returning a
context-length error.

## When to use it

- adopting the Gateway API **and** routing traffic to LLM providers
- you want token-aware limits and provider failover handled at the edge
- coming from Gloo's open-source edge and looking for where it continued

## When not to use it

- plain HTTP with no AI dimension — [Envoy Gateway](../envoy-gateway/) is the more neutral choice
- staying on `Ingress`

## Related

Other AI-traffic tooling in this repo: [`ai/ai-gateway/`](../../../ai/ai-gateway/), including
Envoy AI Gateway and Higress.

---

[← Gateway API](../README.md)
