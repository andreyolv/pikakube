[← CNI](../README.md)

# kindnet

<https://github.com/aojea/kindnet>

Context and comparison against the other CNIs: [../README.md](../README.md)

---

## The problem it solves

The default CNI that [Kind](https://kind.sigs.k8s.io/) ships with. It exists so a local
cluster comes up with working pod networking and **zero decisions required**.

It satisfies the Kubernetes network model and deliberately stops there.

## When to use it

- local Kind clusters where networking is not the thing being tested
- you want the cluster up now, and the CNI is not the point

## When not to use it

- any shared, staging or production cluster
- when you are testing networking behaviour itself — policy enforcement, routing modes, observability. Install [Cilium](../cilium/README.md) or [Calico](../calico/README.md) on the Kind cluster instead

## In pikakube

This is what comes up by default from
[`clusters/kind-configs/`](../../../../clusters/kind-configs/), and it is the right choice
for a laptop cluster. Cilium is the one documented in depth for when networking *is* the
subject.

---

[← CNI](../README.md)
