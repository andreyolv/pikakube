[← Metrics collectors](../README.md)

# metrics-server

<https://github.com/kubernetes-sigs/metrics-server>

---

## The problem it solves

`kubectl top` and the Horizontal Pod Autoscaler need live CPU and memory usage. Kubernetes
does not provide that out of the box — the Metrics API has no implementation until something
serves it.

metrics-server collects usage from each kubelet and serves the **Metrics API**
(`metrics.k8s.io`). It keeps only the most recent values, in memory, with no history.

Without it, `kubectl top` returns an error and CPU-based autoscaling does not work.

## What it is not

**Not a monitoring system.** It stores nothing, has no query language, and cannot answer any
question about the past. That is deliberate — it exists to serve the autoscaler, not people.

**Not [kube-state-metrics](../kube-state-metrics/README.md).** That exposes object state to Prometheus.
This exposes live resource usage to the Kubernetes API. Both are usually installed, and they
do not overlap.

## When to use it

- effectively always — `kubectl top` and HPA are baseline expectations
- CPU or memory based autoscaling

## When not to use it

- as a source of monitoring data. Prometheus scraping cAdvisor covers that, with history
- if autoscaling needs **custom** metrics — that is [prometheus-adapter](../prometheus-adapter/README.md) or [KEDA](../../../../devops/event-driven/keda/)

## Kind note

On Kind and some managed clusters, metrics-server fails to start because it cannot verify
kubelet certificates. The usual fix is `--kubelet-insecure-tls`, which is acceptable in a local
cluster and should not be carried into a real one.

---

[← Metrics collectors](../README.md)
