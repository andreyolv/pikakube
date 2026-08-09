[← CNI](../README.md)

# Calico

<https://github.com/projectcalico/calico>
<https://docs.tigera.io/calico/latest/about/>

Context and comparison against the other CNIs: [../README.md](../README.md)

---

## The problem it solves

Pod networking with a **choice of dataplane and routing model**, which is what makes it fit
into environments that already have opinions.

- **native routing via BGP**, peering with an existing network fabric — no encapsulation, full MTU
- or **overlay** (VXLAN / IP-in-IP) where BGP is not an option
- a policy engine that goes past the Kubernetes API: `GlobalNetworkPolicy` applies cluster-wide, plus ordered rules and explicit deny
- an eBPF dataplane option, if you want it without moving to Cilium

## When to use it

- you need **BGP** to integrate with a datacentre fabric
- policy requirements exceed what stock `NetworkPolicy` expresses — cluster-scoped rules, ordering, explicit deny
- you want a long, boring operational track record more than the newest dataplane

## When not to use it

- eBPF-first observability is the goal — [Cilium](../cilium/README.md) goes considerably further, with Hubble
- a local throwaway cluster, where [kindnet](../kindnet/README.md) is enough

---

[← CNI](../README.md)
