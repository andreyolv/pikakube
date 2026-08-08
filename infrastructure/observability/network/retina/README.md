[← Network observability](../README.md)

# Retina

<https://github.com/microsoft/retina>

---

## The problem it solves

eBPF-based network observability that is **CNI-agnostic** — flow logs, drop reasons, per-pod
traffic and DNS metrics on any CNI, not only Cilium.

That is its whole reason to exist. Hubble is more mature and more capable, and requires
Cilium. Retina is the answer when Cilium is not, and cannot be, the CNI.

## When to use it

- you want flow-level visibility and the CNI is **not** Cilium
- AKS, where it is the native option
- drop reasons and DNS metrics matter and nothing currently reports them

## When not to use it

- **Cilium is already the CNI** — use Hubble; it is better and already there
- you need something dependable today. See below

---

## Notes

> Still problematic and does not work reliably — not worth recommending in its current state.

Open issues encountered:

- <https://github.com/microsoft/retina/issues/1612>
- <https://github.com/microsoft/retina/issues/1252>
- <https://github.com/microsoft/retina/issues/915>

**Labels and ports do not match** between the metrics Service and the ServiceMonitor, so
Prometheus does not scrape it without manual correction:

- <https://github.com/microsoft/retina/blob/main/deploy/hubble/manifests/controller/helm/retina/templates/hubble/metrics-service.yaml>
- <https://github.com/microsoft/retina/blob/main/deploy/hubble/manifests/controller/helm/retina/templates/hubble/servicemonitor.yaml>

Recorded here because a broken ServiceMonitor is a silent failure: the deployment looks
healthy, and no metrics ever arrive.

---

[← Network observability](../README.md)
