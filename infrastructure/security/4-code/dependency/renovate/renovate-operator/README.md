[← Renovate](../README.md)

# Renovate Operator

<https://github.com/mogenius/renovate-operator>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

The two other self-hosted shapes both sit slightly outside Kubernetes' model. The official Helm
chart runs Renovate as a `CronJob` — simple, but the configuration is chart values, and adding a
repository means editing them. [Renovate CE](../renovate-ce/README.md) is a long-running server
configured through environment variables and its own config file, which is a second configuration
system living next to your GitOps repository.

The operator's proposition is that **repositories to update should be Kubernetes resources**.
You declare what to renovate as custom resources; the operator reconciles them into scheduled
jobs, tracks their status, and exposes metrics.

What that buys in a GitOps platform:

| Property | Consequence |
|---|---|
| Configuration as CRs | Renovate's scope is managed by Flux, in Git, reviewed like everything else |
| Status on the resource | `kubectl get` tells you what ran and whether it succeeded |
| Prometheus metrics | job success, failure and duration land in the platform's existing pipeline |
| Jobs, not a server | no persistent service holding credentials open; work happens in short-lived pods |
| Kubernetes-native secrets | credentials come from Secrets, so External Secrets or SOPS apply normally |

For a cluster already run by Flux with everything else declared as resources, this is the shape
that is consistent with the rest of the platform.

## When to use it

- **Everything else in the platform is declarative and reconciled**, and a separately configured
  server would be the odd one out
- **You want metrics and status through Kubernetes**, rather than a dashboard in a second system —
  this deployment enables the ServiceMonitor, so the data goes to the same Prometheus as
  everything else
- **Credentials should be Kubernetes Secrets**, managed by whatever secret tooling the cluster
  already uses
- **Multiple repository groups with different schedules**, each expressed as its own resource

## When not to use it

- **It is a community project, not maintained by the Renovate team.** That is the decisive
  caveat and it should be checked before adopting: an operator that stops being updated pins an
  old Renovate version, and Renovate's value depends on it keeping up with new managers and
  datasources. Confirm release activity first
- **A handful of repositories on GitHub.** The Action in [`../README.md`](../README.md) is one
  file and nothing to operate
- **You want vendor support.** [Renovate CE](../renovate-ce/README.md) has a commercial upgrade
  path; this does not
- **Alongside another shape.** The Action, the CE server and this operator all open pull
  requests; two of them against the same repositories means duplicates

## Notes

Original note recorded for this tool — it appears in the parent Renovate note list rather than in
a file of its own:

- <https://github.com/mogenius/renovate-operator> — the community Kubernetes operator from
  mogenius. The repository documents the CRDs, the Helm chart (published as an **OCI** chart to
  `ghcr.io`), and the configuration model for repository discovery and scheduling. Read the
  release history first, for the maintenance reason above.

From the manifests committed here:

- The chart is referenced through an **`OCIRepository`** rather than a `HelmRepository` —
  `oci://ghcr.io/mogenius/helm-charts/renovate-operator`, tag `4.14.1`, polled every 24h — and
  the `HelmRelease` uses `chartRef` to point at it. This is the newer Flux pattern for
  OCI-published charts and is worth noting because it differs from every other release in this
  tree.
- `upgrade.crds: CreateReplace` is set, so CRDs are updated on chart upgrade. Helm does not
  update CRDs by default, which is a common way for an operator to end up running against a stale
  CRD schema; setting this is correct, and it is also the setting that can destructively replace a
  CRD, so it is a deliberate choice rather than a default.
- `metrics.enabled` and `metrics.serviceMonitor.enabled` are both true — the only values
  overridden — wiring it into the platform's Prometheus.
- The values reference kept in the file:
  <https://artifacthub.io/packages/helm/mogenius/renovate-operator> and
  <https://github.com/mogenius/renovate-operator/blob/main/charts/renovate-operator/values.yaml>.
- **No Renovate CRs are committed**, so the operator has nothing to reconcile — see
  [`helm/README.md`](helm/README.md).

---

[← Renovate](../README.md)
