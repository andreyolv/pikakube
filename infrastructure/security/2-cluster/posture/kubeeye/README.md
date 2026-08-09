[← Posture assessment](../README.md)

# KubeEye

<https://github.com/kubesphere/kubeeye>

KubeSphere's cluster inspection tool. Checks configuration, resource definitions and node health, and
writes the findings into `ClusterInsight` custom resources.

---

## The problem it solves

The other two tools in this folder answer a security question against a published standard.
KubeEye answers a broader and vaguer one: **is anything about this cluster wrong?**

What it looks at:

| Area | Examples |
|---|---|
| Workload configuration | missing resource limits, no liveness or readiness probe, `latest` tags, single-replica Deployments with no PDB |
| Node health | kernel-level problems surfaced by node-problem-detector, disk pressure, unready nodes |
| Cluster resources | deprecated API versions, orphaned objects, misconfigured RBAC |
| Rules you write | its own rule CRDs, so a check specific to your environment becomes part of the inspection |

The last row is what distinguishes it. kube-bench runs a fixed benchmark and kubescape runs fixed
frameworks; KubeEye lets you add inspection rules — including rules that run a Prometheus query or
evaluate an arbitrary expression against a resource — so organisation-specific expectations get
checked by the same mechanism.

Results land as `ClusterInsight` resources in the cluster, which means they are queryable with
`kubectl` and consumable by anything that reads the API. There is no external service.

The honest framing: **this is an operational health checker with a security-adjacent surface, not a
security benchmark tool.** Half its findings are reliability problems — no probes, no limits, a
deprecated API that will break at the next upgrade. Those are real and worth finding. They are not
what an auditor means by posture.

## When to use it

- **You want reliability findings alongside configuration findings.** Missing probes and absent
  resource limits cause more outages than a wrong API server flag causes breaches, and no other tool
  in this folder reports them prominently.
- **You need custom inspection rules.** If there are conventions specific to this platform — every
  namespace must carry an owner label, every StatefulSet must have a PDB — KubeEye can check them
  without writing a controller.
- **Deprecated API detection before an upgrade.** Finding out which manifests will stop working at
  the next Kubernetes version is genuinely valuable and is not what kube-bench or kubescape are for.
- **You already run KubeSphere.** It is part of that ecosystem and integrates with its console.
- **You want findings to stay in the cluster.** `ClusterInsight` resources, no SaaS, no external
  reporting path — a real contrast with [kubescape](../kubescape/README.md).

## When not to use it

- **You need CIS Benchmark evidence.** That is [kube-bench](../kube-bench/README.md). KubeEye's
  overlap with CIS is incidental.
- **You need framework coverage or attack-path analysis.** [kubescape](../kubescape/README.md) does
  NSA, MITRE ATT&CK and RBAC escalation paths; KubeEye does not.
- **Something else already reports the same findings.** Missing limits and `:latest` are already
  covered by the admission policies in [`../../policies/`](../../policies/README.md) — and covered
  better, because a policy prevents them rather than listing them. A finding you can enforce is not
  a finding worth scanning for repeatedly.
- **Project activity matters to you.** It is the least widely adopted of the three tools here and
  moves more slowly. Check the repository's recent history before committing to it.
- **You want three overlapping scanners.** Three tools producing three lists that partly agree is a
  triage problem, not a coverage win.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of this folder.

### How it is deployed here

This is the only tool in `2-cluster/` installed from a **`GitRepository`** source rather than a
Helm registry:

| File | Content |
|---|---|
| `helm/gitrepository.yaml` | Flux `GitRepository` in `flux-system`, cloning `https://github.com/kubesphere/kubeeye.git` at tag `v1.0.1`, refreshed every 24h |
| `helm/helmrelease.yaml` | HelmRelease using `chart: chart/kubeeye` from that GitRepository, with no values |
| `namespace.yaml` | the namespace |

That shape is what you do when a project does not publish its chart to a registry: Flux clones the
source repository and installs the chart from a path inside it. It works, and it has two costs worth
naming — the chart is not versioned independently of the source tree, and the install now depends on
GitHub being reachable at reconcile time rather than on a registry.

The tag `v1.0.1` is pinned, which is the important part. An unpinned branch reference here would mean
the chart could change under you at any reconcile.

No values are set, so this is the chart's defaults. There is no `kustomization.yaml` in this folder,
so like most of `2-cluster/`, whether Flux actually delivers it depends on how the parent
Kustomization is assembled.

### What to look at after installing it

The inspection produces `ClusterInsight` objects. `kubectl get clusterinsight -o yaml` is the whole
interface — there is no UI in this deployment, and there is no `ServiceMonitor`, so nothing reaches
Prometheus either.

That is the practical weakness of this folder as configured: findings exist as YAML in the cluster
and nothing surfaces them. Compare with [kubescape](../kubescape/README.md), which has a
`ServiceMonitor` enabled, and with
[Policy Reporter](../../policies/kyverno/policy-reporter/README.md), which exists precisely because
findings nobody reads are findings that do not count.

### Where it fits

Of the three tools here, KubeEye is the one whose value overlaps least with the others and whose
findings overlap most with things this platform can already enforce. The reliability half —
deprecated APIs, missing probes — is the part worth keeping it for; the configuration half is better
handled by [Kyverno](../../policies/kyverno/README.md), where a rule prevents the problem instead of
reporting it every week.

---

[← Posture assessment](../README.md)
