[← Trivy](../README.md)

# Trivy — observability

The Grafana folder and dashboard for the operator's metrics, declared as CRs for the Grafana
Operator.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `grafanafolder.yaml` | `grafana.integreatly.org/v1beta1` `GrafanaFolder` | creates a folder titled **Trivy** in Grafana |
| `17813.yaml` | `grafana.integreatly.org/v1beta1` `GrafanaDashboard` | imports community dashboard **17813** from grafana.com into that folder |

Both set `allowCrossNamespaceImport: true` and select the Grafana instance with
`instanceSelector.matchLabels.dashboards: grafana`, which is how the Grafana Operator matches a
CR in the `trivy` namespace to a Grafana running elsewhere. The dashboard references the folder
with `folderRef: trivy`.

The dashboard is pulled with `grafanaCom.id: 17813` — that is, the operator fetches it from
grafana.com rather than storing the JSON in this repository.

## Why this exists

Scanner findings that live only in a scanner's own UI get looked at once. The point of this
folder is that vulnerability data lands in the **same Grafana** as everything else the platform
watches, sourced from the same Prometheus — which is only possible because
`serviceMonitor.enabled: true` is set in the [HelmRelease](../helm/README.md).

This is the metrics half of the same idea as [`../polr-adapter/README.md`](../polr-adapter/README.md):
findings should surface where people already look, not in a dedicated dashboard that requires
someone to remember it exists.

## Notes

- The upstream reference recorded in the file:
  <https://grafana.com/grafana/dashboards/17813-trivy-operator-dashboard/> — the Trivy Operator
  dashboard on grafana.com.

- **Pulling a dashboard by ID means it is not pinned.** `grafanaCom.id` without a `revision`
  fetches the dashboard as published; the operator supports specifying a revision, and doing so
  is the difference between a dashboard that stays as reviewed and one that changes when
  upstream publishes an update. This is the same class of problem as an unpinned image tag.

- The general caution about community dashboards applies here as much as anywhere: many are
  built against metric names that have since changed, and several display numbers that do not
  answer a question anyone asks. Treat 17813 as a starting point to trim, not as the finished
  view.

---

[← Trivy](../README.md)
