[← Load balancer](../README.md)

# MetalLB

<https://github.com/metallb/metallb>
<https://metallb.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

On bare metal there is no cloud controller watching for `type: LoadBalancer` Services, so
the external IP stays `<pending>` forever. MetalLB is that missing controller: it owns a
pool of addresses and assigns them.

Two modes:

| Mode | How | Trade |
|---|---|---|
| **L2 (ARP)** | one node claims the IP and answers ARP; another takes over on failure | works on any flat LAN, nothing to negotiate — but **all traffic for an IP enters through one node**. Failover, not balancing |
| **BGP** | nodes peer with the network's routers and advertise the IP | real ECMP balancing across nodes — but you need routers to peer with and a network team that agrees |

## When to use it

- **the default answer for bare metal and on-prem** — mature and widely deployed
- a home lab or local cluster that needs real `LoadBalancer` Services

## When not to use it

- on EKS, AKS or GKE, where a controller already exists
- when you also need a virtual IP for the **API server** — [kube-vip](../kube-vip/) does both jobs

## Address pool on Kind

The pool has to sit inside the subnet Kind's Docker network uses:

```bash
docker network inspect -f '{{.IPAM.Config}}' kind
```

Pick a range inside that subnet, and outside anything DHCP might hand out — an overlapping
pool produces intermittent address conflicts that look like random network faults.

## Remember

Point **one** MetalLB address at the ingress controller and route HTTP from there. One
`LoadBalancer` Service per application burns addresses and skips the layer that does routing.

---

[← Load balancer](../README.md)
