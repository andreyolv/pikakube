[← SDN](../README.md)

# Kilo

<https://github.com/squat/kilo>
<https://kilo.squat.ai/>

Context and comparison: [../README.md](../README.md)

---

> **Not a CNI.** Kilo meshes *nodes*; it does not provide pod networking. It runs alongside a
> CNI, not instead of one.

## The problem it solves

Kubernetes assumes nodes can reach each other directly. That assumption breaks the moment
nodes stop sharing a network — a cluster spanning two clouds, a region plus an edge site, or
a laptop joining a remote cluster.

Kilo creates a **WireGuard mesh** between nodes, so a cluster can span locations over
untrusted networks with encrypted node-to-node traffic. It understands topology: nodes in
the same location talk directly, and only cross-location traffic goes through the mesh.

## When to use it

- **one cluster spanning multiple clouds, regions or sites**, with no private link between them
- edge or on-prem nodes joining a central cluster over the public internet
- node-to-node traffic must be encrypted and the CNI does not do it

## When not to use it

- every node sits on one trusted network — the mesh and encryption cost buys nothing
- you want **separate clusters** to talk, not one cluster spanning locations. That is a different capability entirely: see [`cluster-interconnection/`](../../cluster-interconnection/README.md)

## The distinction that matters

| Goal | Tool |
|---|---|
| **One cluster**, nodes in different places | **kilo** |
| **Several clusters**, in different places, that need to talk | [Submariner](../../cluster-interconnection/submariner/README.md) or a service mesh |

Mixing these up is the common mistake. Kilo makes distant machines behave like one cluster;
cluster-interconnection keeps clusters separate and connects them.

---

[← SDN](../README.md)
