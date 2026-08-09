[← Gateway API](../README.md)

# Kuadrant

<https://github.com/Kuadrant/kuadrant-operator>
<https://docs.kuadrant.io/>

Context and comparison: [../README.md](../README.md)

---

> **Not a gateway.** Kuadrant adds policy to a Gateway API implementation you already run —
> Envoy Gateway, Istio and others. It needs one; it does not replace one.

## The problem it solves

The Gateway API standardised routing, and deliberately left **policy** — rate limiting,
authentication, authorisation — to extensions. So each implementation invented its own, and
portability stopped at the routing layer.

Kuadrant fills that gap using the API's own **policy attachment** mechanism, with typed
resources bound to a `Gateway` or an `HTTPRoute`:

| Policy | What it does |
|---|---|
| `RateLimitPolicy` | limits, including per-caller counters |
| `AuthPolicy` | authentication and authorisation — API keys, OIDC, JWT |
| `DNSPolicy` | DNS and traffic distribution across clusters |
| `TLSPolicy` | certificate handling, integrated with cert-manager |

## When to use it

- you run a Gateway API implementation and need rate limiting or auth **without** adopting a full [API gateway](../../api-gateway/README.md)
- you want policy expressed in Gateway API resources rather than vendor annotations
- multi-cluster, where `DNSPolicy` overlaps with what [k8gb](../../load-balancer/k8gb/README.md) does

## When not to use it

- you have no Gateway API implementation yet — install one first
- the requirement is full API management with a developer portal, consumers and plans; that is [Kong](../../api-gateway/kong/README.md) or [Tyk](../../api-gateway/tyk/README.md)

## Reference

[Rate limiting overview](https://docs.kuadrant.io/1.1.x/kuadrant-operator/doc/overviews/rate-limiting/)

Kuadrant also maintains [gateway-api-state-metrics](https://github.com/Kuadrant/gateway-api-state-metrics),
useful for observing Gateway API objects in Prometheus.

---

[← Gateway API](../README.md)
