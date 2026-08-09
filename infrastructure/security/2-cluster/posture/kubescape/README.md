[← Posture assessment](../README.md)

# Kubescape

<https://github.com/kubescape/kubescape>
<https://github.com/kubescape/helm-charts>
<https://github.com/kubescape/github-action>

CNCF security platform for Kubernetes: CIS, NSA and MITRE ATT&CK frameworks, workload configuration,
RBAC analysis and image vulnerability scanning, from one operator.

---

## The problem it solves

[kube-bench](../kube-bench/README.md) answers one question — is the cluster configured the way CIS
says — and answers it well. It says nothing about your Deployments, your RBAC bindings, or the
vulnerabilities in the images you are running.

Kubescape covers that broader surface:

| Area | What it checks |
|---|---|
| Cluster configuration | CIS Kubernetes Benchmark, including provider variants |
| Hardening guidance | NSA/CISA Kubernetes hardening |
| Attacker techniques | MITRE ATT&CK for containers |
| Workloads | privileged containers, host mounts, missing limits, dangerous capabilities |
| RBAC | who can escalate to cluster-admin, and by which path |
| Images | vulnerability scanning of what is actually running |

The ATT&CK mapping is the framing that changes the conversation. CIS tells you a flag is wrong; ATT&CK
tells you which attack step that flag enables. "Twelve controls failed" invites triage by
convenience; "these three findings enable privilege escalation from a compromised pod" invites
triage by risk. That is the one thing here that no CIS-only tool provides.

Two capabilities worth calling out because they are not obvious from the framework list:

- **Relevancy.** An eBPF component observes which code paths a container actually executes, so
  vulnerability findings can be filtered to packages that are genuinely loaded. Most CVEs in a
  container image are in code that never runs; this is the filter that makes a vulnerability list
  short enough to act on. It is `disable`d in this repo's configuration — see the Notes.
- **Runtime-informed network policies.** It can observe traffic and generate NetworkPolicy
  suggestions, which addresses the hardest part of network segmentation: knowing what talks to what.

It also runs as a CLI and as a GitHub Action, so the same checks run against manifests in CI before
they reach a cluster.

## When to use it

- **You want breadth from one deployment.** Three frameworks, workloads, RBAC and images in one
  operator is genuinely less work than assembling four tools.
- **You need prioritisation, not a checklist.** The ATT&CK mapping and the attack-path analysis are
  what turn a report into a work queue.
- **On a managed control plane.** Because so much of its value is in workloads, RBAC and images
  rather than API server flags, it degrades far less than kube-bench does when the control plane is
  not yours. See [`../README.md`](../README.md#3-the-managed-control-plane-problem).
- **You want history and trend.** A scheduled operator with stored results tells you whether posture
  is improving. A one-shot Job does not.
- **You want the same checks in CI.** The GitHub Action scans manifests before merge, which is the
  cheapest place to catch a privileged container.

## When not to use it

- **You need a pure CIS Benchmark artefact for an auditor.** kube-bench maps control by control to
  the published numbering with the official remediation text. Kubescape's CIS coverage is real, but
  kube-bench is the narrower, more direct answer to that specific request.
- **You will not accept a SaaS dependency, without doing the work to avoid it.** Kubescape runs fully
  in-cluster, but the operator's default posture — and the configuration in this repo — points at
  ARMO's backend for the UI, storage and reporting. Running it offline is supported and is a
  deliberate configuration choice, not the default here.
- **Exceptions must live in Git.** This is the recorded friction in this folder and it is a real
  objection for a GitOps platform. See the Notes.
- **Node overhead is tight.** The full capability set includes eBPF node agents and image scanning,
  which are not free. Capabilities can be disabled individually — and one already is here.
- **You only want one thing.** If the requirement is "scan images", Trivy is smaller; if it is
  "check CIS", kube-bench is smaller. Kubescape is a platform, and platforms cost more than tools.

## Notes

Every original note from `doc.md`, translated and explained.

### The SaaS backend

> <https://cloud.armosec.io> -> google

ARMO's hosted platform, where scan results are sent, stored and displayed, logged into with a Google
account. This is the piece that makes the "is this a SaaS product" question a real one.

The configuration in this repo is wired to it: `helm/helmrelease.yaml` sets `server: api.armosec.io`
and pulls `account` and `accessKey` from a Kubernetes Secret named `credentials` via `valuesFrom`
with `targetPath`. That is the right mechanism — credentials are not inline in the HelmRelease — but
it does mean scan results leave the cluster. Anyone adopting this should decide that deliberately;
the offline mode exists.

### A specific control

> <https://hub.armosec.io/docs/c-0254>

A link into ARMO's control catalogue, where each control is documented with its rationale,
remediation and framework mappings. The `c-XXXX` identifiers are how findings are referenced — worth
knowing because the report gives you the code and the explanation lives at that URL.

### Exceptions cannot be supplied through the chart

> not: Supply exceptions json in helm chart
> <https://github.com/kubescape/helm-charts/issues/393>

The important one. Every posture tool needs exceptions — for controls that do not apply, for accepted
risks, for workloads that legitimately need a host mount. Kubescape takes them as a JSON document,
and this issue records that the Helm chart offers no way to supply it.

For a GitOps-managed cluster that is not a minor gap. It means the accepted-risk list — the record of
what the organisation decided not to fix and why — lives outside Git, applied by hand or through the
SaaS UI. It is unreviewable, it is not versioned, and it disappears when the cluster is rebuilt.

This is the single strongest practical objection to Kubescape in this repository, and it is recorded
here as a "not" precisely because it was hit and not resolved.

### Other recorded chart and tool issues

> <https://github.com/kubescape/helm-charts/issues/338>
> <https://github.com/kubescape/kubescape/issues/1645>
> <https://github.com/kubescape/helm-charts/issues/566>

Three further upstream issues collected while working with the tool — two against the Helm charts,
one against Kubescape itself. Kept as a record of friction encountered rather than as a list of
resolved problems; each should be re-checked against the deployed version (chart
`kubescape-operator` 1.27.1) before assuming it still applies.

The pattern across all four links is worth naming honestly: the friction in adopting Kubescape has
been in the **packaging** rather than in the scanning. The findings are good; getting the operator to
behave in a declarative, GitOps-managed way has been the work.

### How it is deployed here

`helm/helmrelease.yaml`, chart `kubescape-operator` 1.27.1:

| Setting | Meaning |
|---|---|
| `clusterName: pikakube` | how the cluster is identified in reports |
| `server: api.armosec.io` | the SaaS backend |
| `capabilities.relevancy: disable` | the eBPF relevancy agent is off — less node overhead, and vulnerability findings are not filtered to code that actually runs |
| `kubescape.serviceMonitor.enabled: true` | Prometheus scrapes it, so findings can drive Grafana and alerts |
| `kubescapeScheduler.scanSchedule: "0 8 * * 1"` | a full scan every Monday at 08:00 |

Turning `relevancy` off is a defensible trade for a local cluster — it is the most resource-hungry
capability — and it is also the one that makes the vulnerability output tractable. Worth revisiting
if image findings ever become the reason to run this.

`registry-scan.yaml` is a Secret holding a `registriesAuth` JSON array, configured for
`quay.io/kubescape` with `auth_method: public`. That enables scanning images in a registry rather
than only the ones running in the cluster. `secret.yaml` holds the `credentials` Secret the
HelmRelease reads from.

The weekly cadence is the right shape for the workload half of the scan, which changes constantly.
The cluster-configuration half changes rarely and would be adequately covered by a run after each
upgrade — which is what [kube-bench](../kube-bench/README.md) next door does.

---

[← Posture assessment](../README.md)
