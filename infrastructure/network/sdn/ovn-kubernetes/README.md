[← SDN](../README.md)

# ovn-kubernetes

<https://github.com/ovn-kubernetes/ovn-kubernetes>

Context and comparison: [../README.md](../README.md)

---

## The problem it solves

The same substrate as [Kube-OVN](../kube-ovn/README.md) — pod networking implemented on **OVN/OVS**
rather than iptables or eBPF — but as the upstream project that large distributions build
on. It is the CNI behind OpenShift.

You get the OVN model: logical switches and routers, ACLs, and a network programmed through
a control plane rather than assembled from per-node rules.

## When to use it

- you are **aligned with the OpenShift or Red Hat ecosystem**, and want the same networking upstream
- you want the OVN substrate with the opinions and hardening of a large distribution behind it
- your team already operates OVN elsewhere

## When not to use it

- you want OVN features with a friendlier, more Kubernetes-native API — [Kube-OVN](../kube-ovn/README.md) is the more approachable of the two
- you are not committed to the OVN ecosystem at all; the operational cost only pays off if the model is genuinely needed

## Choosing between the two OVN options

| | ovn-kubernetes | Kube-OVN |
|---|---|---|
| Positioning | upstream, distribution-driven | product-driven, richer CRD surface |
| Best fit | OpenShift alignment | VPC/subnet/QoS features on a self-managed cluster |
| API style | closer to raw OVN concepts | more Kubernetes-native abstractions |

Both carry the same underlying cost — an OVN control plane to operate.

---

[← SDN](../README.md)
