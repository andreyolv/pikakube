[← Ingress controller](../README.md)

# Contour

<https://github.com/projectcontour/contour>
<https://projectcontour.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

An **Envoy** data path with a configuration model that is neither raw Envoy nor annotation
soup.

Its `HTTPProxy` CRD was designed for the gap `Ingress` left: typed fields for timeouts,
retries, load balancing strategy and traffic splitting, plus **delegation** — a team can own
routes under a path prefix without being able to touch anyone else's.

That delegation idea is the same problem the [Gateway API](../../gateway-api/README.md)
later solved upstream, which is worth knowing: Contour arrived at role separation early, and
now also implements the Gateway API.

## When to use it

- you want Envoy's data path and behaviour without writing Envoy configuration
- multi-team clusters where route ownership must be delegated safely
- a CNCF project with a clean, small surface

## When not to use it

- the team knows NGINX and the requirement is ordinary — [ingress-nginx](../ingress-nginx/) will be less new material
- you need API management

---

[← Ingress controller](../README.md)
