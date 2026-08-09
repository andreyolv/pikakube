[← Kubernetes cost visibility](../README.md)

# OpenCost

<https://github.com/opencost/opencost>
<https://github.com/opencost/opencost-helm-chart>
<https://github.com/opencost/opencost-parquet-exporter>

---

## The problem it solves

A node costs €0.42/hour and runs forty pods from eight teams. The cloud bill has one line for it.
There is no line for a pod, because the provider does not know pods exist.

OpenCost computes the split: node price × the share each pod reserved × the time it existed, plus
persistent volumes, load balancers and — with a cloud integration — the actual invoiced rate rather
than list price. The result is available as an API, as a small UI, and as **Prometheus metrics**.

It is the CNCF project that defines the model, and Apache-2.0. [Kubecost](../kubecost/README.md) is
the commercial product built on it. Where other tools disagree about what a pod costs, this is the
implementation they are disagreeing with.

## When to use it

- **as the default**: the open specification, no licence question, and the model everything else is
  measured against
- when cost should be a **Prometheus series** living beside every other platform metric, graphed in
  the Grafana you already have
- feeding cost into your own reporting, or into a data warehouse — see the parquet exporter below
- multi-cluster, where you are willing to aggregate the metrics yourself

## When not to use it

- when the audience is outside the platform team and needs a product to open — that is
  [Kubecost](../kubecost/README.md), which is built on this
- when long retention is required and Prometheus retention is short: OpenCost's history is your
  metrics store's history
- expecting alerting and budgets out of the box; see the notes — that has been a persistent gap
- without a cloud billing integration on a discounted account, where list prices make the numbers
  wrong rather than approximate
- as an optimisation tool. It attributes; it changes nothing —
  [`optimization/`](../../../optimization/README.md)

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/opencost/opencost>** — the project. CNCF incubating, Apache-2.0, and the
reference implementation of the allocation model described in [`kubernetes/`](../README.md)
section 2.

**<https://github.com/opencost/opencost-helm-chart>** — the official chart, and the one used here.

**<https://github.com/opencost/opencost-parquet-exporter>** — exports OpenCost's allocation data as
**Parquet files** to object storage. The point of this is easy to miss and it is genuinely useful:
OpenCost's own history is bounded by Prometheus retention, but a FinOps programme wants year-on-year
comparisons. Dumping allocation data to Parquet in S3 or Blob Storage makes cost a dataset the
platform's own query engines can read — see
[`data-engineering/`](../../../../data-engineering/README.md) — with the retention decided by storage
policy rather than by a monitoring system. It also makes cost joinable to business data, which is
where per-customer or per-feature cost analysis becomes possible.

### The recorded issues

Five, and together they are a fair picture of what OpenCost is good at and what it is not.

**<https://github.com/opencost/opencost/issues/2442>** — *"No cloud costs appear in the UI"* (January
2024, closed). The classic cloud-integration failure: OpenCost runs, in-cluster allocation looks
right, and the cloud cost view is empty. The cause is almost always the integration rather than the
tool — malformed integration secret, missing permissions on the billing export, or the provider's
export not yet populated. **This is the issue to read first when `cloudCost` is enabled and shows
nothing**, and it is directly relevant here, since this deployment enables `cloudCost` and mounts an
Azure service key.

**<https://github.com/opencost/opencost/issues/1726>** — *"WRN CostModel: custom pricing has illegal
GPU cost"* (March 2023, closed). A warning emitted when custom pricing is configured without a valid
GPU price. Harmless in itself, and worth recognising for two reasons: it is noisy enough to look like
a real failure during setup, and it is a reminder that **GPU nodes need their price configured
explicitly** — otherwise the most expensive capacity in the cluster is allocated wrongly, or not at
all.

**<https://github.com/opencost/opencost/issues/737>** — *"Feature Request — Cost threshold
notifications and alerts for labels"* (March 2021, closed) and
**<https://github.com/opencost/opencost/issues/781>** — *"Teams Notification"* (April 2021, closed).
Both are the same underlying request: **notify me when cost crosses a threshold.** Their age and
their outcome are the finding — alerting is not what OpenCost does. It computes and exports; it does
not decide that a number is bad.

That is not a defect if you have a monitoring platform. OpenCost exports Prometheus metrics, so the
correct route is a Prometheus alerting rule on those series, delivered through the platform's
existing [`alerting/`](../../../../observability/alerting/README.md) path — the same channel as every
other alert, instead of a second notification system that only talks about cost.

**<https://github.com/opencost/opencost/issues/2884>** — *"Filter cost by label"* (August 2024,
**still open**). The most consequential of the five. Aggregation by namespace is straightforward;
filtering and aggregating by arbitrary labels — team, product, cost centre, environment — is the
capability a real chargeback or showback model needs, and it is uneven. Worth verifying against the
current version before promising a report that depends on label filtering, because this is precisely
where [Kubecost](../kubecost/README.md) sells its product tier.

### On the deployment here

Flux, chart **1.28.0**, into an `opencost` namespace, pointed at the existing Prometheus
(`prometheus-server.monitoring`, port 80) with `cloudCost` enabled, `defaultClusterId: AKS_DEV` and a
`cloud-integration-secret`. The important choices:

**A custom image**: `gcr.io/kubecost1/opencost:cloudcost`, for both the exporter and the UI, instead
of an upstream release tag. That is a pinned workaround from when cloud cost support was not in a
stable release. It should be revisited — running an unversioned tag from a vendor registry means no
reproducible version and no upgrade path, and cloud cost has since become a normal feature.

**Resources**: `requests` 10m CPU / 4Gi memory, `limits` 999m CPU / 4Gi. Memory request equals limit,
which is correct for an incompressible resource (see
[`rightsizing/`](../../../optimization/rightsizing/README.md) section 2), and 4Gi is not a guess —
OpenCost holds allocation state in memory and its footprint grows with cluster size and query window.
The CPU request of 10m against a 999m limit is a very wide burst range, which is defensible for a
component that is idle between queries.

**Probes with `initialDelaySeconds: 180`** on both liveness and readiness, on both containers. Three
minutes before the first check — OpenCost builds its initial view by querying Prometheus over the
whole window, and a shorter delay produces a restart loop that looks like a crash and is actually
just a slow start.

**A commented-out post-renderer:**

```yaml
# postRenderers:
# - kustomize:
#     patches: ... add envFrom: secretRef: opencost-spn
```

This is the pattern to recognise: the chart has no values field for injecting arbitrary environment
variables from a Secret, so a Flux Kustomize post-renderer patches `envFrom` onto the Deployment
after templating. `opencost-spn` is an Azure **service principal** — the credentials for reading the
billing export. It is the right technique when a chart is missing a field, and it is worth keeping
visible as a general escape hatch rather than forking the chart.

**Other commented-out options**, each recording something that was tried:

- `EMIT_KSM_V1_METRICS` / `EMIT_KSM_V1_METRICS_ONLY` — OpenCost can emit kube-state-metrics v1-shaped
  series itself. These flags control the overlap when the cluster already runs kube-state-metrics;
  getting them wrong produces either duplicate series or missing ones.
- `EXPORT_CSV_FILE` pointing at Azure Blob Storage — a simpler predecessor of the parquet exporter
  above, and the same instinct: get the data out to somewhere with real retention.
- `persistence` — for keeping state across restarts.
- `CLUSTER_INFO_FILE_ENABLED`, and log level.

**An Azure service key mounted at `/var/secrets`** via `extraVolumes` and `extraVolumeMounts` — the
other half of the cloud integration.

---

[← Kubernetes cost visibility](../README.md)
