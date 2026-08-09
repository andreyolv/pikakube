[← Trivy](../README.md)

# Trivy polr-adapter

<https://github.com/fjogeleit/trivy-operator-polr-adapter>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

Trivy Operator writes its findings as its own CRDs — `VulnerabilityReport`,
`ConfigAuditReport`, `ExposedSecretReport`, `RbacAssessmentReport`, `ClusterComplianceReport`.
Kyverno writes its findings as `PolicyReport` and `ClusterPolicyReport`, the resource types
defined by the Kubernetes **Policy WG report API**. Anything built to consume `PolicyReport`
resources — Policy Reporter's UI, its metrics, its notification routing to Slack or Teams —
therefore sees Kyverno's results and is blind to Trivy's.

The adapter closes that gap. It watches Trivy Operator's CRDs and emits equivalent
`PolicyReport` resources, with the source labelled so you can still tell where a result came
from.

The consequence is the one that matters operationally:

> **Vulnerability findings and policy violations appear in the same list, with the same
> severities, the same filters and the same alert routing.**

Without it, the platform has two answers to "what is wrong in this cluster" and people check at
most one of them.

## When to use it

- **You already run Policy Reporter** (which this repository does, alongside Kyverno) and you
  run Trivy Operator. That is the whole case, and it is a strong one
- **You want a single notification pipeline.** Policy Reporter's targets — Slack, Teams,
  webhooks, S3, Elasticsearch — then carry vulnerability findings too, without wiring a second
  integration
- **You want `PolicyReport`-shaped metrics.** Policy Reporter exports Prometheus metrics from
  `PolicyReport` resources; the adapter makes vulnerability counts available through the same
  path
- **Multiple report sources, one consumer.** The adapter also supports other scanners' CRDs, so
  it stays useful if the mix of tools changes

## When not to use it

- **You do not run Policy Reporter.** The adapter produces `PolicyReport` resources for
  something else to read; on its own it just doubles the number of CRs in the cluster
- **You read Trivy's CRDs directly.** If your tooling already consumes `VulnerabilityReport`,
  the translation adds a component and an eventual-consistency lag for no gain
- **Large clusters where object count is a concern.** Every finding becomes a second Kubernetes
  object; on a big cluster with vulnerability reports enabled for everything, that is real
  pressure on etcd. Scope which report types you translate rather than enabling all of them
- **You want aggregation across tools outside the cluster.** That is a different job —
  deduplication and triage across CI, DAST, SAST and container scanning belongs in
  [`../../../../4-code/aspm/defectdojo/README.md`](../../../../4-code/aspm/defectdojo/README.md)

## Notes

- The adapter is a **community project by Frank Jogeleit**, the author of Policy Reporter
  itself — <https://github.com/fjogeleit/trivy-operator-polr-adapter>. It is not maintained by
  Aqua Security, so its compatibility with new Trivy Operator CRD versions can lag; check the
  chart's supported versions when upgrading the operator.

- The chart values reference kept in the HelmRelease:
  <https://github.com/fjogeleit/trivy-operator-polr-adapter/blob/main/charts/trivy-operator-polr-adapter/values.yaml>
  — the authoritative list of which report types can be enabled or disabled.

- Related component in this repository: Policy Reporter lives under Kyverno in
  `security/2-cluster/policies/kyverno/policy-reporter/`, which is the consumer this adapter
  feeds.

---

[← Trivy](../README.md)
