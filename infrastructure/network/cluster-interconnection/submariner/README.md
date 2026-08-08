[← Cluster interconnection](../README.md)

# Submariner

<https://github.com/submariner-io/submariner>
<https://github.com/submariner-io/submariner-charts>
<https://submariner.io/>

Context and comparison against the alternatives: [../README.md](../README.md)

---

## The problem it solves

Pods in two separate Kubernetes clusters cannot reach each other. There is no route between
the pod networks, and no name that resolves across the boundary.

Submariner builds **encrypted tunnels between gateway nodes** so pods can talk directly,
adds **Lighthouse** so exported services resolve under `svc.clusterset.local`, and offers
**Globalnet** for the case where both clusters use the same pod CIDR.

Its distinguishing trait is that it is **CNI-agnostic** — it works with different CNIs on
each side, which is what rules out Cilium Cluster Mesh in mixed environments.

## When to use it

- clusters sit on **networks you do not control** — different clouds, or across a boundary where you cannot get peering
- the pod **CIDRs overlap**, which is common because both clusters were built from the same defaults
- the CNIs **differ** between clusters
- as **migration scaffolding**, with a defined end date — the strongest case

## When not to use it

- a flat routed network already exists (VPC peering, BGP) — the tunnels add nothing
- **Cilium is the CNI in both clusters** — Cluster Mesh does this without another component
- a service mesh already spans the clusters — it also gives you identity and L7 policy
- only two or three services need to talk — expose them through an Ingress or API gateway instead

## Before deploying

Two operational facts worth knowing up front:

- **the broker is stateful.** Metadata exchange is not peer-to-peer; a designated namespace or cluster acts as the central point, and discovery depends on it
- **gateway nodes are a chokepoint.** They carry all cross-cluster traffic, become a bandwidth ceiling and a failure domain, and are a high-value target

And the security consequence, covered in
[../README.md §6](../README.md#6-security-what-interconnection-actually-opens): connecting
the clusters means a compromise in one can reach the pod network of the other, with
`NetworkPolicy` on the far side unable to distinguish that traffic from any other external
source.

---

[← Cluster interconnection](../README.md)
