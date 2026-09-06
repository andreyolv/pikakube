[← SDN](../README.md)

# FRRouting (FRR)

<https://github.com/frrouting/frr>
<https://frrouting.org/>

Context and comparison: [../README.md](../README.md)

---

## What it is

A full **routing protocol suite for Linux** — BGP, OSPFv2/v3, IS-IS, RIP, EIGRP, Babel, PIM,
LDP, BFD, VRRP, PBR and BGP EVPN — descended from Quagga and hosted by the Linux Foundation.
GPL-2.0.

The architecture is the part worth knowing, because it explains how it behaves in a container:

| Component | Role |
|---|---|
| `zebra` | the RIB manager — collects routes from every protocol daemon and programs the kernel FIB |
| `bgpd`, `ospfd`, `isisd`, … | one daemon per protocol, each speaking to peers and feeding zebra |
| `vtysh` | an integrated Cisco-style CLI over all of them |

So FRR does not forward packets. The kernel does. FRR decides **what the kernel's routing table
should say**, by talking to the routers around it.

## Why it belongs in this folder

It is the second exception here, alongside [kilo](../kilo/README.md): **not a CNI**, and not
something a cluster picks instead of one. Everything else in `sdn/` builds a programmable network
*inside* Kubernetes. FRR is how a node participates in the routed network *outside* it.

That makes it the layer underneath several tools that are documented elsewhere in this repository:

| Where it shows up | What FRR is doing |
|---|---|
| [MetalLB](../../load-balancer/metallb/README.md) in FRR mode (`frr-k8s`) | advertising Service IPs to the top-of-rack switches over BGP, with BFD for fast failure detection |
| [kube-router](../kube-router/README.md) | the same job, with GoBGP rather than FRR — the alternative implementation of the same idea |
| Cumulus Linux, SONiC, VyOS, DENT | FRR **is** the routing stack of those network operating systems |
| Pure-L3 / "BGP to the host" clusters | every node is a BGP speaker peering with the fabric; no overlay, no encapsulation |

The last row is the design argument. An overlay exists because the underlay does not know how to
reach pod CIDRs. Tell the underlay — via BGP — and the overlay is unnecessary: no VXLAN header,
no MTU arithmetic, and traceroute works again.

## When to use it

- **on-premise, with a real network team.** BGP peering with the top-of-rack switch is the normal
  way to get Service and pod addresses routable, and FRR is the standard speaker
- MetalLB in BGP mode is already the plan — FRR mode is where the features are (BFD, IPv6,
  multiple sessions, `FRRConfiguration` CRDs)
- EVPN/VXLAN underlay, or any design where nodes must exchange routes with the fabric
- you want the routing stack to be the same one the switches run

## When not to use it

- **managed Kubernetes.** EKS, AKS and GKE hand you a routed VPC and a cloud load balancer; there
  is no BGP session for you to own, and nothing here applies
- Kind, k3d, or any laptop cluster — there is no fabric to peer with
- BGP is not available, or nobody owns the network side of the conversation. A BGP session is an
  agreement with the network team, not a configuration file; adopting it unilaterally is how you
  get an ASN conflict and a very awkward incident review

## The operational warning

FRR is a router. Misconfiguring it does not fail closed the way a broken Deployment does — it
advertises the wrong prefixes, and the blast radius is the physical network rather than the
cluster.

Two specifics that matter in Kubernetes:

- **filter what you advertise, both ways.** A node that accepts a full table, or announces more
  than its Service prefixes, affects traffic that has nothing to do with Kubernetes
- **BFD changes failure timing.** It is the reason to run FRR mode in MetalLB — sub-second
  detection instead of BGP hold timers — but it also means a flapping link now moves traffic
  quickly and repeatedly

## How this applies to pikakube

Nothing to deploy, and the reason is the same one recorded across this folder: the cluster is
Kind, and every question FRR answers is a question about a physical network that does not exist
here.

It is worth having filed for the on-premise case, where it is not optional in the way most tools
here are. The [on-premise](../../../platform-engineering/kubernetes/on-premise/README.md) path
reaches it quickly: a self-managed cluster needs `LoadBalancer` Services to get real addresses,
that means [MetalLB](../../load-balancer/metallb/README.md), and MetalLB in BGP mode means FRR.

The point to carry over from this folder's [anti-patterns](../README.md#5-anti-patterns): the
choice is not FRR versus an overlay in the abstract. It is whether the underlay is something you
are allowed to talk to. Where it is, routed beats encapsulated on every axis. Where it is not,
none of this is available at any price.

---

[← SDN](../README.md)
