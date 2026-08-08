[← Prometheus](../README.md)

# kube-prometheus-stack

<https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack>
<https://github.com/prometheus-operator/kube-prometheus>

**This is what pikakube actually deploys.**

---

## What it bundles

Not a single component — an opinionated stack that gets a cluster from nothing to working
monitoring in one release:

| Component | Role |
|---|---|
| **Prometheus Operator** | manages Prometheus, Alertmanager and rules through CRDs |
| **Prometheus** | scraping, storage, rule evaluation |
| **Alertmanager** | [routing, grouping, inhibition](../../../../alerting/alertmanager/) |
| **[kube-state-metrics](../../../collector/kube-state-metrics/)** | Kubernetes object state |
| **node-exporter** | per-node OS metrics |
| **[Grafana](../../../../dashboards/grafana/)** | dashboards, pre-provisioned |
| **Default rules and dashboards** | a working baseline for cluster health |

The default alert rules matter more than they look. They encode a decade of accumulated
knowledge about what actually goes wrong in a Kubernetes cluster, and reproducing them by hand
is a long project.

## The CRDs are the real product

The operator turns configuration into resources, which is what makes the whole stack fit
GitOps:

| CRD | Declares |
|---|---|
| `ServiceMonitor` | scrape this Service |
| `PodMonitor` | scrape these Pods directly |
| `PrometheusRule` | alerting and recording rules |
| `Probe` | blackbox probing targets |

A team adds a `ServiceMonitor` next to their Deployment and their metrics are scraped —
without editing a central Prometheus configuration. That delegation is why the operator
pattern won.

## What to change from the defaults

The chart is designed to work immediately, not to be right for your cluster:

| Setting | Why |
|---|---|
| **Retention** | the default local window is short; decide it deliberately and pair with [long-term storage](../../../long-term-storage/README.md) |
| **Persistent volumes** | disabled by default in some paths — a restart then discards everything |
| **Resource limits** | Prometheus memory tracks [cardinality](../../../README.md#3-cardinality-is-the-whole-game), and the defaults assume a small cluster |
| **`serviceMonitorSelector`** | by default it may only select its own release's monitors, which is the usual reason a new `ServiceMonitor` is silently ignored |

That last row is the single most common confusion with this chart: the `ServiceMonitor` exists,
looks correct, and is never scraped because the selector does not match it.

---

[← Prometheus](../README.md)
