[← Runtime security](../README.md)

# Falco operator

<https://github.com/falcosecurity/falco-operator>

<https://github.com/falcosecurity/charts/pkgs/container/charts%2Ffalco-operator>

Falco's own operator: instances, rules, plugins and configuration as **Kubernetes objects** instead
of Helm values. Incubating in the Falco ecosystem, and deployed here as an OCI chart.

---

## The problem it solves

[Falco](../falco/README.md) itself is not the problem — the chart is. Under the Helm deployment,
everything that makes a Falco installation *yours* lives in `values.yaml`:

| What you actually change over time | How the chart handles it |
|---|---|
| **A detection rule** — added, tuned, or silenced after a false positive | a values change and a chart upgrade |
| A plugin — Kubernetes audit, CloudTrail, GitHub | values, plus artefact configuration |
| A configuration fragment | values |
| A second Falco with different settings — a different node pool, a different rule set | a **second release**, duplicated wholesale |

The first row is the one that hurts, because it is the row you touch constantly. Section
[§4](../README.md#4-the-alert-volume-problem) of this folder states the operational truth of runtime
security: **tuning is the job**. Rules are edited weekly at the start, and under the chart every one
of those edits is an upgrade of the release that owns the DaemonSet on every node. The unit of
change (one rule) and the unit of deployment (the whole agent) are wildly mismatched.

The operator separates them. It is two controllers:

| Component | Owns | CRDs |
|---|---|---|
| **Falco operator** | the deployment itself — DaemonSets, Deployments, companion components | `Falco`, `Component` (`instance.falcosecurity.dev/v1alpha1`) |
| **Artifact operator** | what Falco loads — rules, plugins, configuration, delivered as sidecars | `Rulesfile`, `Plugin`, `Config` (`artifact.falcosecurity.dev/v1alpha1`) |

So a rule becomes a `Rulesfile` object: written in Git, reviewed as a diff, applied on its own, and
— crucially — sourced from an **OCI artefact** in a registry as easily as from an inline string.
That is the same distribution mechanism `falcoctl` already used, promoted from a chart setting to a
first-class API.

Multiple instances follow for free. `Falco` is a CR, so a second one with different settings is a
second object, not a second Helm release with a duplicated values tree.

## When to use it

- **rules change often**, which they do on any cluster where Falco is actually being tuned rather
  than installed and ignored
- rules should be **reviewable objects in Git** with their own lifecycle, rather than a block of
  YAML inside a release's values
- you want **more than one Falco** — different rule sets or drivers per node pool, or a separate
  instance for a plugin-driven source such as Kubernetes audit logs
- rules are distributed as **OCI artefacts** across clusters, and you want the cluster to pull them
  rather than have every chart carry a copy
- the platform is already CRD-shaped and reconciled by
  [Flux](../../../../platform-engineering/gitops/flux/README.md), so one more controller costs
  little and the objects fit the existing model

## When not to use it

- **the chart already works and rules are stable.** The Helm deployment is what most Falco
  installations run, it is proven, and the operator's benefit is proportional to how often you edit
  rules. If the answer is "never", there is nothing here for you
- **it is incubating, with `v1alpha1` APIs.** New CRDs on the layer whose job is to notice a
  compromise; a broken reconcile here means detection is down, and detection being down is silent by
  nature
- **Kubernetes 1.29+ is required** for native sidecar containers. On an older cluster this is not a
  choice
- you run one Falco with the upstream rules and no local tuning — which is a defensible starting
  position, and one the operator makes no better
- **as an answer to alert noise.** This is the misreading to avoid: the operator changes where rules
  live and how they are delivered. It does not decide which rules are worth alerting on, and that is
  the actual work

## The honest boundary

**It solves distribution, not detection.** Everything this folder says about runtime security still
applies unchanged: Falco observes and does not block
([§3](../README.md#3-detection-vs-enforcement)); an untuned deployment produces noise until people
stop reading it ([§4](../README.md#4-the-alert-volume-problem)); and detection without a response
path is a dashboard ([§5](../README.md#5-detection-without-response-is-a-dashboard)) — which is what
[falcosidekick](../falco/README.md) and [falco-talon](../falco/falco-talon/README.md) are for.

The operator makes the tuning loop **cheaper and reviewable**. That is a real improvement, because
the reason most Falco installations are never tuned is friction, not disagreement about the rules.
It is not a different security posture.

## Notes

**Two deployments of Falco cannot both be applied as written.** This folder and
[`../falco/`](../falco/README.md) each contain a `HelmRelease` named **`falco`** in namespace
**`falco`**, and each contains a `Namespace` object for `falco`. One installs the Falco chart
(`4.21.3`, with falcosidekick and its UI enabled); the other installs the operator chart (`0.3.1`).
A Flux `Kustomization` including both would see duplicate resource identities, and even if it did
not, two releases would contend for the same DaemonSet.

Neither is currently wired into `clusters/dev/`, so this is latent rather than broken — but it is a
decision that has been deferred, not made. **Pick one**: the chart, which is the proven path, or the
operator, which is the declarative one. If the operator wins, `../falco/` becomes the reference page
and its manifests should go.

**The OCI pinning here is the good pattern.** `helm/ocirepository.yaml` pins the chart by tag *and*
digest:

```yaml
ref:
  tag: 0.3.1
  digest: sha256:2e5026052b24562238ee2fa0e192f1288e75d1817a32b2e156bd5ebc89b3b78f
```

A tag is mutable and a digest is not, so this is a chart that cannot change underneath the cluster.
It is the same discipline argued for actions in
[GitHub Actions §8](../../../../devops/cicd/github-actions/README.md#8-anti-patterns) and the
opposite of the tag-only pinning noted elsewhere in this repository.

**The `HelmRelease` has empty values and the sample instance has an empty spec.** `example/falco.yaml`
is a `Falco` named `falco-sample` with `spec: {}` — the default deployment, no driver choice, no
rule configuration, no outputs. That is the right way to start (install the operator, confirm it
reconciles, then configure), but it is worth being explicit that as it stands this is **an operator
with no meaningful Falco configuration behind it**, not a runtime security deployment.

**Rules pulled from a registry are code you did not review.** Sourcing a `Rulesfile` from an OCI
artefact is the operator's best feature and it moves rule content into the supply chain: the cluster
now executes detection logic fetched at reconcile time. Pin artefacts by digest, prefer registries
you control, and treat rule artefacts the way
[`security/0-governance/supply-chain/`](../../../../security/0-governance/supply-chain/README.md)
treats any other pulled artefact. A malicious or merely wrong rules file does not open a hole — it
closes an eye, which is harder to notice.

**Where this fits in pikakube.** The manifests here are the newer half of a decision this repository
has not finished: [`../falco/`](../falco/README.md) has the fuller deployment (sidekick, the UI, gRPC
output, the modern eBPF driver) and this folder has the better delivery model. Nothing is reconciled
into the cluster yet, so the cheap move is to settle it now, while the choice is a directory rather
than a migration — and if the operator is chosen, the first thing worth writing is not more rules but
a `Rulesfile` object that proves a tuned rule can be shipped without touching the DaemonSet.

---

[← Runtime security](../README.md)
