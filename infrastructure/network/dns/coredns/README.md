[← DNS](../README.md)

# CoreDNS

<https://github.com/coredns/coredns>
<https://github.com/coredns/helm>
<https://coredns.io/plugins/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Pods need to reach each other by name. CoreDNS is the cluster's resolver: it answers
`<service>.<namespace>.svc.cluster.local` and forwards everything else upstream.

It is already running in every cluster, so the useful question is not whether to install it
— it is **when you need to change it**.

## When you touch it

- **stub zones** — pointing an internal corporate domain at a specific resolver instead of relying on the node's, which is what fixes "works on VPN, fails in the pod"
- **rewrite rules** — mapping one name to another inside the cluster
- **forwarding** — sending upstream queries somewhere specific rather than to the node's resolver
- **custom domains** — serving names the cluster is authoritative for

Configuration is a **plugin chain** in a Corefile, and order matters — plugins execute in a
fixed sequence, not the order you wrote them.

## What it is not

Not an alternative to Route 53, Azure DNS or Cloud DNS. Those are **authoritative servers for
public zones**; CoreDNS is a resolver for the cluster's internal namespace. Publishing names
to the outside world is [external-dns](../external-dns/README.md).

## Related

- resolution behaviour inside pods, including the `ndots:5` trap: [../README.md](../README.md#2-dns-inside-kubernetes)
- per-node caching when CoreDNS is under load: [node-local-dns](../node-local-dns/README.md)

---

[← DNS](../README.md)
