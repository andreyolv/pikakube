[← Metrics collectors](../README.md)

# kube-state-metrics

<https://github.com/kubernetes/kube-state-metrics>
<https://github.com/kubernetes/kube-state-metrics/tree/main/docs>

---

## The problem it solves

Kubernetes knows the desired and actual state of every object. None of it is a metric until
something translates it.

kube-state-metrics listens to the API and exposes object state as Prometheus series: desired
versus ready replicas, pod phase and restart count, PVC status, Job success, node conditions,
CronJob schedules.

Most Kubernetes alerts are built on it — "deployment has fewer ready replicas than desired" is
a kube-state-metrics query, not a resource one.

## What it is not

**Not [metrics-server](../metrics-server/).** That reports live CPU and memory usage for
`kubectl top` and the HPA. This reports **object state** for Prometheus. Different data,
different consumers, both usually needed.

It also holds no state and does no aggregation — it is a translation layer from the API to
the metrics format, which is why it is stateless and cheap to run.

## Custom resources, too

The feature worth knowing about: it can expose **your own CRDs** as metrics, through
`customResourceState`.

That is how a Crossplane composite, a Flux `Kustomization` or any operator's CRD becomes
alertable — otherwise their status is visible only through `kubectl`.

- <https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/extend/customresourcestate-metrics.md>
- <https://github.com/crossplane/crossplane/discussions/2583>
- <https://blog.cubieserver.de/2024/creating-custom-kubernetes-metrics-with-kube-state-metrics/>

Known issue: <https://github.com/kubernetes/kube-state-metrics/issues/2449>

## Cardinality note

It produces a series per object, so cluster size drives series count directly. On large
clusters the label allow-list is worth configuring rather than accepting the defaults — see
[cardinality](../../README.md#3-cardinality-is-the-whole-game).

```bash
kubectl port-forward svc/kube-prometheus-stack-kube-state-metrics 8080
```

---

[← Metrics collectors](../README.md)
