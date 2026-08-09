[← Trivy](../README.md)

# Trivy — Helm deployment

The Flux resources that install `trivy-operator` into the cluster.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://aquasecurity.github.io/helm-charts` as a chart source |
| `helmrelease.yaml` | `HelmRelease` (`trivy`) | installs chart `trivy-operator` version `0.31.0`, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `trivy` namespace, labelled `agentpool: spot` |

## The values that encode decisions

Four settings in `helmrelease.yaml` are choices rather than defaults, and each corresponds to an
argument made in [`../../README.md`](../../README.md):

| Value | Effect | Why |
|---|---|---|
| `targetNamespaces: airbyte` | the operator only scans workloads in the `airbyte` namespace | a scoped first rollout. Cluster-wide on day one produces thousands of findings at once and the project dies under its own output |
| `operator.builtInTrivyServer: true` | runs Trivy in client/server mode with a shared server inside the cluster | each scan Job would otherwise download the vulnerability database itself. One server means one database, far less bandwidth and much faster scans |
| `trivy.ignoreUnfixed: true` | findings with no released fix are dropped | keeps the queue actionable. The trade-off — a real vulnerability with no patch becomes invisible — is stated in [`../../README.md`](../../README.md) |
| `serviceMonitor.enabled: true` | exposes operator metrics for Prometheus | connects the scanner to the platform's existing [`observability/`](../../../../../observability/README.md) pipeline instead of a private dashboard |

## Notes

- **`serviceAccount.annotations` carries `eks.amazonaws.com/role-arn`** pointing at
  `arn:aws:iam::xxxxxxx:role/trivy-operator-eks-data-dev` (the account number is redacted in the
  file). The operator needs to pull image manifests and configuration from ECR to inventory
  them; without registry credentials every private image reports as unscannable. The IAM role
  itself is created by the Crossplane resources in
  [`../crossplane/README.md`](../crossplane/README.md).

- **The commented-out `nodeCollector.tolerations` block** lists four `agentpool` taints —
  `CriticalAddonsOnly`, `system`, `spot`, `on-demand`. The node collector runs as a Job on every
  node to gather CIS Benchmark evidence, so it needs to tolerate whatever taints the node pools
  carry. Left commented out, the collector simply does not schedule on tainted nodes and the
  compliance report is quietly incomplete. Note the taint key `agentpool` is AKS naming, which
  suggests the block was carried over from an Azure cluster — on the EKS cluster referenced by
  the ServiceAccount annotation the keys would differ.

- The chart values reference kept in the file:
  <https://artifacthub.io/packages/helm/trivy-operator/trivy-operator> and
  <https://github.com/aquasecurity/trivy-operator/blob/main/deploy/helm/values.yaml> — the second
  is the authoritative list of every value the chart accepts.

---

[← Trivy](../README.md)
