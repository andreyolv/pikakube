[← Image scanning](../README.md)

# KubeClarity

<https://github.com/openclarity/kubeclarity>
<https://github.com/openclarity/openclarity>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

Most scanning happens at build time, against images someone is about to publish. That leaves a
question unanswered: **what is actually running in the cluster right now, and what is it made
of?**

KubeClarity answers it from the inside. It discovers the workloads in the cluster, generates an
**SBOM for each running image**, scans those SBOMs for vulnerabilities, and presents the result
through a UI with the relationships intact — which image contains which package, and which
running application depends on it.

The features that distinguish it from a CI scanner:

| Capability | Why it matters |
|---|---|
| **Runtime SBOM generation** | you get an inventory of what is deployed, not of what was built — including images pulled from elsewhere and images nobody rebuilds |
| **Multiple scanner and SBOM-generator backends** | it orchestrates syft, Trivy, Grype and others rather than implementing its own matching, so results can be merged |
| **Package-centric view** | "which running workloads contain log4j 2.14" is one query, which is exactly the question asked on the day a headline CVE lands |
| **CIS Docker Benchmark on running images** | posture in addition to vulnerabilities |
| **UI-first** | it is meant to be browsed, not just alerted on |

That "which workloads contain package X" query is the practical reason to run something like
this. Reconstructing the answer from CI logs during an incident is exactly when you do not want
to be reconstructing anything.

## When to use it

- **You want an inventory of what is deployed**, browsable, with dependency relationships —
  rather than a stream of per-image findings
- **Incident response on a named package.** "Where is this library running" answered in seconds
- **You do not control every image.** Vendor images, marketplace charts and third-party
  operators never pass through your CI; runtime discovery is the only way they get inventoried
- **You want to combine several scanner backends** and see where they disagree, without wiring
  that yourself

## When not to use it

- **As a CI gate.** It is a cluster component with a UI; use Trivy or Grype in the pipeline
- **You already run Trivy Operator and are happy with CRDs.** The overlap is substantial: both
  scan running workloads continuously. Trivy Operator's output is Kubernetes-native
  (`VulnerabilityReport` CRDs, feeding
  [Policy Reporter](../trivy/polr-adapter/README.md)); KubeClarity's is a UI and an API. Running
  both means paying twice for the same scans
- **Small clusters.** The deployment is a multi-component application with a database, a UI and
  scanner jobs — heavy relative to what it returns on a handful of workloads
- **Without checking the project's current state first.** See the note below

## Notes

Original notes recorded for this tool, and what the pairing means:

- <https://github.com/openclarity/kubeclarity> — the original project. KubeClarity is the
  Kubernetes-focused tool: discover workloads, generate SBOMs, scan, present.
- <https://github.com/openclarity/openclarity> — **the successor**. The OpenClarity project
  consolidated its previously separate tools (KubeClarity, VMClarity, APIClarity) into a single
  platform that scans containers, VMs and APIs through one architecture.

That is why both links are recorded, and it is the thing to check before adopting: **new
development happens in `openclarity`, and `kubeclarity` is the earlier, Kubernetes-only
codebase.** Anyone starting today should be looking at OpenClarity and confirming the current
maintenance status of the standalone KubeClarity repository and its Helm chart, rather than
assuming the chart deployed here is the actively developed path.

The chart values reference recorded in the HelmRelease:
<https://github.com/openclarity/kubeclarity/blob/main/charts/kubeclarity/values.yaml>.

APIClarity, the API-focused sibling now folded into OpenClarity, is adjacent to the tools in
[`../../../4-code/api/README.md`](../../../4-code/api/README.md) — different layer, related
lineage.

---

[← Image scanning](../README.md)
