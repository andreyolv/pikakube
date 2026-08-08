[← Ingress controller](../README.md)

# HAProxy

<https://github.com/haproxy/haproxy>
<https://github.com/haproxytech/helm-charts>
<https://www.haproxy.com/documentation/kubernetes-ingress/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

An ingress controller on top of HAProxy — a proxy with a long track record in high-throughput
L4 and L7 load balancing, well outside Kubernetes.

Reasons it gets chosen:

- **raw performance** and predictable behaviour under load
- **existing expertise** — teams that have run HAProxy for years already know how to tune, observe and debug it
- strong **L4** handling, not only HTTP

## When to use it

- HAProxy is already the organisation's proxy and that knowledge should be reused
- throughput or latency requirements are strict enough to be worth benchmarking
- significant TCP/L4 traffic alongside HTTP

## When not to use it

- no existing HAProxy background — the ecosystem around [ingress-nginx](../ingress-nginx/) and [Traefik](../traefik/) is much larger in a Kubernetes context
- you want API management or a rich CRD model

---

[← Ingress controller](../README.md)
