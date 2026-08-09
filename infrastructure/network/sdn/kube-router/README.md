[← SDN](../README.md)

# kube-router

<https://github.com/cloudnativelabs/kube-router>
<https://www.kube-router.io/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A normal cluster runs three separate things for networking: a CNI plugin, `kube-proxy` for
Services, and a policy controller.

kube-router collapses all three into **one daemon**:

- **CNI** — pod networking with **BGP**, native routing, no overlay and no encapsulation cost
- **service proxy** — IPVS-based, replacing `kube-proxy`
- **NetworkPolicy** enforcement

Fewer components means less to deploy, less to version and less to reason about when
something breaks.

## When to use it

- you want the **smallest possible** networking stack that still enforces policy
- **BGP** is available and native routing is preferred over an overlay
- resource-constrained environments — edge, small on-prem clusters — where every daemon counts

## When not to use it

- you need the richer constructs from [kube-ovn](../kube-ovn/README.md) — VPCs, subnets, QoS
- you want eBPF, deep observability or L7 policy — [Cilium](../../cni/cilium/README.md) is a different class of tool
- your network cannot do BGP, which removes the main reason to pick it

## The trade

Its virtue and its limit are the same thing: it is **deliberately lean**. It does the three
jobs competently and stops there. If the requirement list grows past them, it is the wrong
starting point rather than something to extend.

---

[← SDN](../README.md)
