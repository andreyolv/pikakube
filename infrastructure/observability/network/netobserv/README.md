[← Network observability](../README.md)

# NetObserv

<https://github.com/netobserv/netobserv-operator>

---

## The problem it solves

An operator-driven network observability pipeline: an eBPF agent collects flows, a flow
collector enriches them with Kubernetes context, and the results land in Loki or Prometheus
with a console for querying them.

Its origin is OpenShift, where it is the built-in network observability feature, and that
shows in its maturity — it is a complete pipeline rather than an agent that emits metrics.

## When to use it

- **OpenShift**, where this is the native and supported option
- you want a full flow pipeline — collection, enrichment with pod and namespace names, storage and a console — rather than assembling one
- flow-level conversation tracking matters: who talked to whom, how much, and for how long

## When not to use it

- [Cilium](../../../network/cni/cilium/) is the CNI — Hubble covers this with nothing extra
- a small cluster; the pipeline has several components and a real storage cost
- you are not on OpenShift and want the lightest option — [Retina](../retina/) is smaller, with the caveats in its README

## Storage note

Flows are high volume. Sending them to Loki means planning retention deliberately, or the
network observability bill quietly becomes the largest line in the logging store.

---

[← Network observability](../README.md)
