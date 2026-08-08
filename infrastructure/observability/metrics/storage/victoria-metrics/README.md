[← Metrics storage](../README.md)

# VictoriaMetrics

<https://github.com/VictoriaMetrics/VictoriaMetrics>
<https://github.com/VictoriaMetrics/operator>
<https://github.com/VictoriaMetrics/helm-charts>

---

## The problem it solves

A PromQL-compatible time-series database built around the two things that hurt most in a
Prometheus deployment: **memory at high cardinality**, and **long retention needing a second
system**.

It handles both. Memory use is substantially lower for the same series count, and long-term
storage is built in rather than requiring [Thanos](../../long-term-storage/thanos/) or
[Mimir](../../long-term-storage/mimir/) alongside it.

It also runs as a drop-in scrape target replacement — `vmagent` scrapes, `vmalert` evaluates
rules, and the operator provides `VMServiceScrape` mirroring `ServiceMonitor`.

## When to use it

- **cardinality is already a problem** and Prometheus memory is the constraint
- you want one system for recent and historical data instead of two
- cost matters at scale — the resource difference is large enough to show up on a bill

## When not to use it

- nothing currently hurts. Prometheus is the ecosystem default, and every dashboard, alert rule and example assumes it
- you depend on behaviour at the edges of PromQL; MetricsQL is compatible but not identical, and the differences surface in unusual queries
- the team's knowledge is Prometheus-shaped and there is no pressure to change

## The honest comparison

Technically the stronger system on resources and operational simplicity. Prometheus retains
the ecosystem, and that is what makes it the default rather than inertia — community
dashboards, alert rules and exporters all assume it.

**Switch when cardinality or cost is already hurting.** Before that, the compatibility of the
default is worth more than the efficiency gain.

## Related

Subfolders: [`victoria-metrics-k8s-stack/`](victoria-metrics-k8s-stack/) — the equivalent of
kube-prometheus-stack — and [`victoria-metrics-operator/`](victoria-metrics-operator/).

The k8s-stack is the fair comparison against kube-prometheus-stack, since both bundle
collection, storage, rules and dashboards rather than just the database.

---

[← Metrics storage](../README.md)
