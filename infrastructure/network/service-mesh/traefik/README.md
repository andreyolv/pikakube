[← Service mesh](../README.md)

# Traefik Mesh

<https://github.com/traefik/mesh>
<https://github.com/traefik/mesh-helm-chart>

Context and comparison: [../README.md](../README.md)

---

> **Historical reference, not a candidate.** Traefik Mesh is no longer actively developed.
> Traefik Labs has focused on the proxy and its ingress and gateway roles instead. New
> deployments should choose from the other options in this folder.

## The problem it solved

A deliberately **non-invasive** mesh: no sidecar injected into every pod, opt-in per service,
and a much smaller conceptual surface than Istio. It targeted teams who wanted some mesh
benefits without adopting a full mesh platform.

That positioning was reasonable, and the market largely answered it in two other ways —
Linkerd got small enough, and Istio added ambient mode.

## Why it is still mapped here

To record that the "lightweight, non-invasive mesh" approach was evaluated, and where it
went. Traefik itself remains relevant in this repo as an
[ingress controller](../../ingress-controller/traefik/).

## What to use instead

| Wanted from Traefik Mesh | Go to |
|---|---|
| Small, low-overhead mesh | [Linkerd](../linkerd/) |
| No per-pod sidecar | [Istio ambient mode](../istio-ambient-mode/) |
| Traefik as a proxy, not a mesh | [`ingress-controller/`](../../ingress-controller/) · [`gateway-api/`](../../gateway-api/) |

---

[← Service mesh](../README.md)
