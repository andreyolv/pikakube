[← Load balancer](../README.md)

# k8gb

<https://github.com/k8gb-io/k8gb>
<https://www.k8gb.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Every other tool in this folder hands out an IP **inside one cluster**. k8gb answers a
different question: **which cluster should a user reach at all?**

It is a global load balancer built entirely on **DNS**. Each cluster runs k8gb, health-checks
its own ingress, and they coordinate so the DNS answer for a hostname points at a cluster
that is actually healthy. When a region fails, the record changes and traffic follows.

No tunnels, no shared pod network, no commercial GSLB appliance.

## When to use it

- **multi-region or multi-cluster failover** driven by health rather than by a human editing DNS
- active/passive or active/active across clusters that are otherwise independent
- you want GSLB behaviour without buying an F5 or equivalent

## When not to use it

- a single cluster — there is nothing to steer between
- you need the **clusters themselves to talk to each other**; that is a different capability, see [`cluster-interconnection/`](../../cluster-interconnection/README.md)

## What it does not replace

Each cluster still needs its own ingress IP from [MetalLB](../metallb/README.md) or a cloud
controller. k8gb sits above that, choosing between the addresses those produce.

## The DNS caveat

Because it works through DNS, it inherits DNS behaviour — **TTL bounds how fast failover
actually happens**, and some resolvers ignore low TTLs. Failover is measured in TTL, not in
seconds. Plan the record's TTL deliberately; see
[`dns/`](../../dns/README.md#ttl-and-caching--the-part-that-bites-during-migrations).

---

[← Load balancer](../README.md)
