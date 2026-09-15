[← Metrics storage](../README.md)

# Prometheus

<https://github.com/prometheus/prometheus>
<https://github.com/prometheus-operator/prometheus-operator>
<https://github.com/prometheus-operator/kube-prometheus>
<https://github.com/prometheus-community/helm-charts>
<https://github.com/prometheus/node_exporter>
<https://github.com/prometheus/pushgateway>
<https://github.com/prometheus/OpenMetrics>

Subfolders: [`kube-prometheus-stack/`](kube-prometheus-stack/README.md) ·
[`prometheus/`](prometheus/) · [`promlens/`](promlens/README.md)

---

## The problem it solves

The de facto standard for metrics in Kubernetes: service discovery from the API, HTTP
scraping, a local time-series database, PromQL, and rule evaluation that feeds
[Alertmanager](../../../alerting/alertmanager/README.md).

Its gravitational pull is the real point. Effectively every component in this repository
exposes Prometheus metrics, every community dashboard assumes it, and every alerting example
is written in PromQL. Choosing something else means giving that up.

## When to use it

- effectively always, for Kubernetes metrics
- you want the ecosystem — exporters, dashboards, alert rules — without building any of it

## When not to use it

- very high cardinality workloads, where [VictoriaMetrics](../victoria-metrics/README.md) uses substantially less memory
- long retention is the primary requirement; that needs [long-term storage](../../long-term-storage/README.md) regardless of which one you pick

## The two constraints worth knowing before deploying

**Cardinality.** Memory grows with active series. One label with unbounded values can take the
instance down — see [`../../README.md`](../../README.md#3-cardinality-is-the-whole-game).

**Retention is global.** There is no per-metric retention, and it is not planned:

- <https://github.com/prometheus/prometheus/issues/15350>
- <https://github.com/prometheus/prometheus/issues/1381>

Keep the local window short and ship aggregated series to long-term storage.

---

## Notes

### Where unfamiliar metrics come from

A default install produces a large number of series nobody asked for. When trying to work out
what a prefix is and whether it can be dropped:

| Prefix | Source |
|---|---|
| `go_*`, `process_*` | <https://github.com/prometheus/client_golang> |
| `rest_client_*` | <https://github.com/kubernetes/client-go> |
| `controller_runtime_*`, `workqueue_*`, `certwatcher_*` | <https://github.com/kubernetes-sigs/controller-runtime> |
| `apiserver_*` | <https://github.com/kubernetes/apiserver> |
| `disabled_metrics_total`, `hidden_metrics_total`, `registered_metrics_total`, `cardinality_enforcement_unexpected_categorizations_total` | <https://github.com/kubernetes/component-base> |
| `aggregator_discovery_*`, `leader_election_*` | <https://github.com/kubernetes/kubernetes> |

These come from shared Go libraries rather than from the application, which is why the same
series appear on every controller in the cluster and why most of them are safe to drop with a
`metricRelabelConfig`.

### Metric catalogues

**kube-state-metrics** — <https://github.com/kubernetes/kube-state-metrics/tree/main/docs>

```bash
kubectl port-forward svc/kube-prometheus-stack-kube-state-metrics 8080
```

**cAdvisor** — <https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md>

**node-exporter** — no usable metric documentation exists; read the endpoint directly:

```bash
kubectl port-forward svc/kube-prometheus-stack-prometheus-node-exporter 9100
```

### Alert rule catalogues

**awesome-prometheus-alerts** — <https://github.com/samber/awesome-prometheus-alerts> ·
<https://samber.github.io/awesome-prometheus-alerts/>

A community catalogue of roughly 1,150 PromQL alerting rules across some 90 exporters and
services: hosts and node-exporter, the databases, Kafka and RabbitMQ, Nginx and Envoy,
Kubernetes and Etcd, Thanos and Loki, the cloud providers. The site renders each group as
YAML, so a rule reaches a `PrometheusRule` with only the wrapper added. Rules are CC BY 4.0.

What it is good for is the exporter nobody on the team has run before — it answers "what is
worth watching here" without reading the metric endpoint from scratch. It is not a rule set
to install wholesale:

- thresholds are generic defaults; firing on someone else's numbers is exactly how the noise
  problem in [`alerting/`](../../../alerting/README.md#1-the-real-problem-is-noise) starts
- a large share of the rules are cause-based — CPU, memory and disk percentages — which is
  the opposite of what the alerting folder argues for
- quality varies by contributor, and no rule carries a runbook
- for Kubernetes itself it is mostly redundant: kube-prometheus-stack already ships the
  kubernetes-mixin rules, which are maintained against the current API

Take the few rules that map to a symptom worth paging on, set the threshold from your own
history, and attach a runbook.

### Open issues worth being aware of

- <https://github.com/prometheus-operator/prometheus-operator/issues/1547>
- <https://github.com/prometheus-operator/prometheus-operator/issues/2398>
- <https://github.com/prometheus-operator/prometheus-operator/issues/5452>
- <https://github.com/prometheus-community/postgres_exporter/pull/911>
- <https://github.com/prometheus/node_exporter/issues/2607>

### Worth watching

<https://github.com/prometheus-community/parquet-common> — Parquet as a storage format for
Prometheus data, which would change the long-term storage picture considerably if it lands.

---

[← Metrics storage](../README.md)
