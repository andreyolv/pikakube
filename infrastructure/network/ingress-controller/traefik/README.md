[← Ingress controller](../README.md)

# Traefik

<https://github.com/traefik/traefik>
<https://github.com/traefik/traefik-helm-chart>
<https://doc.traefik.io/traefik/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

An ingress controller built around **automatic service discovery**: it watches the cluster
and reconfigures itself, with no reload step and no config to regenerate.

What people pick it for:

- **simple defaults** — it works with very little configuration
- a genuinely useful **dashboard** showing routers, services and middlewares
- **middlewares** as CRDs — auth, rate limit, retries, headers — composable and typed, rather than annotation strings
- built-in ACME, so it can obtain Let's Encrypt certificates on its own

## When to use it

- you want the shortest path from install to working ingress
- the middleware model fits better than annotations
- a small cluster where the dashboard is genuinely helpful

## When not to use it

- you want the most documented option with the largest body of community answers — that is [ingress-nginx](../ingress-nginx/README.md)
- you need API management features

> **The API gateway and API management tiers are not open source.** Traefik Proxy is; the
> product tiers above it are commercial. If the requirement is API management, compare
> against [`api-gateway/`](../../api-gateway/README.md) rather than assuming Traefik covers it.

## Related

Traefik also appears in [`service-mesh/traefik/`](../../service-mesh/traefik/README.md) as Traefik
Mesh — a separate, now-discontinued product.

---

[← Ingress controller](../README.md)
