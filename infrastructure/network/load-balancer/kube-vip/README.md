[← Load balancer](../README.md)

# kube-vip

<https://github.com/kube-vip/kube-vip>
<https://github.com/kube-vip/helm-charts>
<https://kube-vip.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

Two problems, which is the reason to pick it over [MetalLB](../metallb/README.md):

**1. `LoadBalancer` Services need an IP** — same job as MetalLB, via L2 (ARP) or BGP.

**2. A self-managed control plane needs a virtual IP.** With three API server nodes, clients
need one stable address that survives losing any of them. Managed clusters get this from the
cloud; self-managed ones have to build it, and the usual answer is keepalived plus HAProxy
as separate components.

kube-vip does both with one daemon.

## When to use it

- **self-managed control plane** that needs an API server VIP — this is the deciding case
- you would rather run one component than MetalLB plus keepalived
- bare metal, on-prem, or `kubeadm` clusters built by hand

## When not to use it

- you only need Service IPs and have no control-plane VIP problem — MetalLB is the more common and better-documented path
- managed Kubernetes, where the control plane endpoint is already provided

## Address pool on Kind

The VIP must sit inside the subnet Kind's Docker network uses:

```bash
docker network inspect kind -f '{{ range $i, $a := .IPAM.Config }}{{ println .Subnet }}{{ end }}'
```

---

[← Load balancer](../README.md)
