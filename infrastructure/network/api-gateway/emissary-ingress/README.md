[← API gateway](../README.md)

# Emissary-ingress

<https://github.com/emissary-ingress/emissary>
<https://www.getambassador.io/docs/emissary/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A CNCF, **Envoy**-based API gateway, formerly Ambassador. Configuration is entirely
CRD-driven — `Mapping`, `Host`, `Module`, `Filter` — rather than annotations, which was
unusual when it appeared and is now the direction everything has taken.

It sits between an ingress controller and a full management platform: routing, rate limiting,
authentication and traffic splitting, without a developer portal or consumer plans.

## When to use it

- you want Envoy with a CRD model and a CNCF home
- routing, auth and rate limiting are the requirement — not portals and quotas
- the team prefers declarative CRDs over the annotation approach

## When not to use it

- the requirement is per-consumer plans, keys and analytics — [Kong](../kong/) or [Tyk](../tyk/)
- you are adopting the [Gateway API](../../gateway-api/README.md), where [Envoy Gateway](../../gateway-api/envoy-gateway/) is the more natural Envoy choice

---

## Notes

The CRDs must be applied **before** the `HelmRelease`:

```bash
kubectl apply -f https://app.getambassador.io/yaml/emissary/3.6.0/emissary-crds.yaml
```

In a Flux setup this means an ordered dependency — a `Kustomization` for the CRDs that the
`HelmRelease` depends on — rather than a single release.

---

[← API gateway](../README.md)
