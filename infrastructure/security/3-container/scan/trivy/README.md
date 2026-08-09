[← Image scanning](../README.md)

# Trivy

<https://github.com/aquasecurity/trivy>
<https://github.com/aquasecurity/trivy-action>
<https://github.com/aquasecurity/trivy-operator>
<https://github.com/aquasecurity/trivy-checks>
<https://github.com/aquasecurity/k8s-node-collector>

Deployment and integration folders:
[`helm/`](helm/README.md) · [`crossplane/`](crossplane/README.md) ·
[`observability/`](observability/README.md) · [`polr-adapter/`](polr-adapter/README.md)

---

## The problem it solves

Most security scanning stacks are assembled from five tools that each do one thing, each with
its own output format, its own severity semantics and its own ignore file. Trivy is the
counter-proposal: **one scanner for everything**, with one configuration and one report format.

What it covers:

| Target | What it finds |
|---|---|
| Container images | OS package and language dependency vulnerabilities |
| Filesystems and Git repositories | the same, against source trees |
| **IaC** — Terraform, CloudFormation, Kubernetes manifests, Helm, Dockerfile | misconfiguration. Trivy **absorbed tfsec**, whose checks now live in `trivy-checks` |
| Kubernetes clusters | workloads, RBAC, node configuration, running images |
| Secrets | credentials committed into images or source |
| Licences | licence obligations of dependencies |
| SBOMs | generates SPDX/CycloneDX, and scans an existing SBOM as input |
| VM images and AWS accounts | disk images, and cloud posture |

Three delivery shapes, and picking the right one is most of the decision:

- **CLI** (`trivy`) — a single Go binary, no daemon, no service. Runs anywhere.
- **`trivy-action`** — the GitHub Action wrapper, for scanning at build time in CI.
- **`trivy-operator`** — a Kubernetes operator that scans continuously *inside* the cluster and
  writes results as CRDs: `VulnerabilityReport`, `ConfigAuditReport`, `ExposedSecretReport`,
  `RbacAssessmentReport`, `ClusterComplianceReport`, `InfraAssessmentReport`.

The operator is the part that changes behaviour rather than adding a report. It answers "what is
vulnerable *right now* in this cluster", including images built months ago that nobody has
rebuilt against today's vulnerability database.

Two behaviours worth knowing because they materially reduce false alarms:

- Trivy prefers **distribution severity** over NVD severity where the distribution publishes one,
  so a CVE Debian rates as low does not show up as critical.
- `--ignore-unfixed` (operator: `trivy.ignoreUnfixed`) drops findings with no released fix,
  which is usually the majority. The trade-off is discussed in [`../README.md`](../README.md).

## When to use it

- **As the default scanner**, unless there is a specific reason not to. Breadth is the argument:
  one tool, one policy, one output, one place to look
- **In CI at build time** with `trivy-action`, gating on fixable HIGH/CRITICAL
- **Continuously in the cluster** with `trivy-operator` — this is where it earns its place, and
  it is what this repository deploys
- **For IaC scanning** instead of adopting tfsec separately; tfsec is now Trivy
- **When you want results as Kubernetes resources.** CRDs mean the findings are queryable with
  `kubectl`, watchable by controllers, and convertible into `PolicyReport`s by the
  [polr-adapter](polr-adapter/README.md)
- **Air-gapped environments** — the vulnerability database can be mirrored into a private
  registry, which is well documented upstream

## When not to use it

- **When you want the scan derived from an SBOM you already publish.** syft + Grype is a cleaner
  fit for that model — see [`../grype/README.md`](../grype/README.md)
- **Registry-side scanning as a service.** Trivy is embedded in Harbor, but as a standalone
  service Clair is the shape designed for it
- **If the operator's resource cost is unacceptable in a small cluster.** Every scan is a Job;
  `builtInTrivyServer: true` (used here) reduces the repeated database downloads, but it is still
  work the cluster is doing
- **As a replacement for SAST.** Trivy inventories dependencies and configuration; it does not
  analyse your source for vulnerable patterns. That is [`../../../4-code/sast/`](../../../4-code/sast/README.md)
- **Do not expect it to see what it cannot inventory** — a binary copied in with no package
  metadata, or a statically vendored library, is largely invisible to any scanner

## Notes

Original notes recorded for this tool, with what each one is:

- <https://github.com/aquasecurity/trivy> — the scanner itself. The single Go binary, the
  documentation, and the ignore-file (`.trivyignore`) and configuration reference.
- <https://github.com/aquasecurity/trivy-action> — the official GitHub Action. This is the CI
  delivery shape: scan an image or a filesystem in a workflow and fail the job on a severity
  threshold. It also uploads SARIF to GitHub code scanning.
- <https://github.com/aquasecurity/trivy-operator> — the Kubernetes operator. Continuous
  in-cluster scanning, results as CRDs. This is what the [HelmRelease](helm/README.md) in this
  folder deploys.
- <https://github.com/aquasecurity/trivy-action/issues/389> — a recorded issue against the
  GitHub Action. It is filed here as a known problem to read before adopting the Action in a
  workflow; the note keeps the reference rather than a summary, so check the current state of
  the thread upstream before designing around it.
- <https://github.com/aquasecurity/k8s-node-collector> — the companion component that gathers
  **node-level** information (kubelet configuration, file permissions, systemd settings) so the
  operator can produce CIS Kubernetes Benchmark results for the nodes themselves. It runs as a
  Job on each node, which is why it needs tolerations for tainted node pools — the reason for
  the commented-out `nodeCollector.tolerations` block in
  [`helm/helmrelease.yaml`](helm/README.md), which lists `agentpool` taints for
  `CriticalAddonsOnly`, `system`, `spot` and `on-demand`. Without those tolerations the
  collector silently skips the tainted nodes, and the compliance report is incomplete rather
  than failing loudly.
- <https://github.com/aquasecurity/trivy-checks/> — the check definitions used for
  misconfiguration scanning, written in Rego. This is where the former **tfsec** rules ended up
  after that project was merged into Trivy, and it is the repository to read (or fork) when you
  need a custom IaC check rather than a custom vulnerability rule.

---

[← Image scanning](../README.md)
