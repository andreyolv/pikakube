[← Cluster interconnection](../README.md)

# KubeSlice

<https://github.com/kubeslice/kubeslice>
<https://kubeslice.io/>

Context and comparison against the alternatives: [../README.md](../README.md)

---

## The problem it solves

Raw cluster-to-cluster connectivity is all-or-nothing: once the clusters are joined,
everything can reach everything.

KubeSlice introduces the **slice** — an application-level overlay network spanning multiple
clusters, scoped to a set of namespaces, with its own isolation and QoS. Two workloads on
the same slice talk to each other across clusters; workloads outside it do not.

The one-line difference from the neighbouring tool:

> **Submariner connects clusters. KubeSlice connects applications across clusters.**

Submariner's unit is the cluster; KubeSlice's is the slice.

## When to use it

- multiple tenants or applications share the same set of clusters and must stay **isolated from each other**
- you want the boundary to follow the **application**, not the cluster
- per-slice QoS or bandwidth control matters

## When not to use it

- you just need two clusters to talk — this is a heavier model for that
- there is only one tenant and one application spanning the clusters
- an existing service mesh already provides the isolation and identity you are after

---

[← Cluster interconnection](../README.md)
