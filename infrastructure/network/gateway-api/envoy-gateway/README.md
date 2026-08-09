[← Gateway API](../README.md)

# Envoy Gateway

<https://github.com/envoyproxy/gateway>
<https://github.com/envoyproxy/envoy>
<https://gateway.envoyproxy.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Envoy is the data path behind a large share of the tools in this repository — Contour,
Emissary, Gloo, Istio — but configuring it directly means writing xDS, which almost nobody
wants to do.

Envoy Gateway is the Envoy project's **own** answer: an implementation of the
[Gateway API](../README.md) that manages Envoy for you. It exists specifically to be the
reference-grade way to run Envoy at the edge.

Beyond the standard API it adds typed extensions — `ClientTrafficPolicy`,
`BackendTrafficPolicy`, `SecurityPolicy` — covering rate limiting, JWT validation, OIDC and
CORS without dropping to raw Envoy config.

## When to use it

- adopting the Gateway API and wanting the implementation closest to Envoy itself
- you want Envoy's capability without maintaining xDS
- the extension policies cover the API-level needs, avoiding a full [API gateway](../../api-gateway/README.md)

## When not to use it

- you are staying on `Ingress` — a controller from [`ingress-controller/`](../../ingress-controller/README.md) is simpler
- you need a developer portal, consumers and plans — that is API management

## Related

The same Envoy foundation appears across the repo: [`ai/ai-gateway/`](../../../ai/ai-gateway/)
for LLM traffic, [`service-mesh/istio/`](../../service-mesh/istio/README.md) for east-west.

---

[← Gateway API](../README.md)
