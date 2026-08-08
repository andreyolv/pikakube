[← SDN](../README.md)

# Kube-OVN

<https://github.com/kubeovn/kube-ovn>
<https://kubeovn.github.io/docs/stable/en/>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

A plain CNI gives you one flat pod CIDR. That satisfies Kubernetes and expresses nothing
else — no tenant address spaces, no subnets, no bandwidth control.

Kube-OVN builds on **OVN/OVS** to bring cloud-VPC semantics inside the cluster:

- **VPCs and subnets** — real isolated address spaces, with per-tenant CIDRs that may overlap between VPCs
- **ACLs** beyond `NetworkPolicy` — stateful, ordered, with explicit deny
- **QoS** — bandwidth limits per pod or subnet
- **static and predictable IPs** — for workloads addressed by IP from legacy systems or firewalls
- **underlay mode** — pods addressable directly on a physical VLAN, no overlay

## When to use it

- **hard multi-tenancy** on a self-managed cluster, where tenants need genuinely separate address spaces
- an existing network expects pods to appear on real VLANs with predictable addresses
- telco, NFV or on-prem environments that already speak OVS

## When not to use it

- a general-purpose cluster — you inherit an entire control plane for constructs you will not use
- the team has no OVN/OVS experience; debugging moves from `iptables` and `tcpdump` to OVS tooling nobody knows yet
- policy, dataplane performance and observability are the real goals — [Cilium](../../cni/cilium/) fits better

## The cost, stated plainly

OVN brings its own control plane and its own databases, which become components you have to
operate, back up and troubleshoot. That is the trade: a much richer network model in exchange
for a much larger operational surface.

---

[← SDN](../README.md)
