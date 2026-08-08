[← CNI](../README.md)

# Multus

<https://github.com/k8snetworkplumbingwg/multus-cni>

Context and comparison against the other CNIs: [../README.md](../README.md)

---

## The problem it solves

A pod gets **one** network interface. Multus lifts that restriction.

It is a **meta-plugin**: it sits in front of the real CNI, lets the primary one attach the
normal cluster interface, and then attaches **additional** interfaces from other plugins —
an SR-IOV virtual function, a macvlan onto a storage VLAN, a dedicated management network.

So it is never "Multus **or** Cilium". It is "Cilium as primary, **and** Multus for the extra
interfaces".

## When to use it

- a workload must sit on **two networks at once** — for example cluster traffic on one interface and a storage or management VLAN on another
- **SR-IOV** or other hardware-accelerated paths are needed for throughput or latency
- telco and NFV workloads, which assume separate control, management and data planes

## When not to use it

- you are choosing a primary CNI — Multus is not one, it has no dataplane of its own
- one interface per pod is enough, which covers almost every general-purpose cluster

Every extra interface is another address plan, another set of routes and another thing to
debug. It earns its place when the workload genuinely requires network separation, and adds
only cost otherwise.

---

[← CNI](../README.md)
