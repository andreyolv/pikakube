[← Renovate Operator](../README.md)

# Renovate Operator — Helm deployment

The Flux resources that install the community Renovate operator.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `ocirepository.yaml` | `OCIRepository` (`flux-system`) | tracks the OCI-published chart `oci://ghcr.io/mogenius/helm-charts/renovate-operator` at tag `4.14.1`, polled every 24h |
| `helmrelease.yaml` | `HelmRelease` (`renovate` namespace) | installs it via `chartRef`, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `renovate` namespace |

## Two details worth noticing

**`OCIRepository` + `chartRef` instead of `HelmRepository` + `chart.spec`.** This is the Flux
pattern for charts published as OCI artefacts rather than to an HTTP chart repository. Every other
release in this tree uses the older form, so this one looks different for a reason. Practical
consequences: the chart is pulled from a registry (so registry authentication and any pull-through
cache apply to it), and it is referenced by tag — which, like an image tag, is mutable unless a
digest is used.

**`upgrade.crds: CreateReplace`.** Helm does not upgrade CRDs on `helm upgrade`; without this, an
operator can end up running against the CRD schema installed on day one. Setting it is correct for
an operator chart. It is also the more destructive of the available behaviours, so it is a
deliberate decision rather than a default worth copying blindly.

## What is missing to make it work

| Required | Why |
|---|---|
| **Renovate custom resources** | the operator reconciles CRs into jobs. With none, it runs and does nothing |
| **Platform credentials in a Secret** | a GitHub App private key or token; the operator has write access to every repository it manages, which makes this the sensitive part |
| **A Renovate configuration** | grouping, scheduling, automerge, concurrency limits — [`../../../README.md`](../../../README.md) section 2 |

The two values that *are* set — `metrics.enabled` and `metrics.serviceMonitor.enabled` — mean the
operator's metrics reach the platform's Prometheus as soon as it has work to report.

## Notes

- The chart values references kept in the file:
  <https://artifacthub.io/packages/helm/mogenius/renovate-operator> and
  <https://github.com/mogenius/renovate-operator/blob/main/charts/renovate-operator/values.yaml>.

- Three deployment shapes are staged in this tree: this operator, the
  [CE server](../../renovate-ce/README.md), and the GitHub Actions workflow described in
  [`../../README.md`](../../README.md). Only one should run against a given set of repositories,
  or you get duplicate pull requests.

---

[← Renovate Operator](../README.md)
