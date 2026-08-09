[← Admission policies](../README.md)

# Kyverno

<https://github.com/kyverno/kyverno>
<https://github.com/kyverno/policies>
<https://kyverno.io/docs/writing-policies/validate/>
<https://kyverno.io/docs/writing-policies/mutate/>

Policy engine for Kubernetes where policies are Kubernetes resources written in YAML. Validates,
mutates, generates and cleans up — the only engine in this folder that does the last two.

Subfolders: [`policies/`](policies/README.md) — policies intended for this cluster ·
[`examples/`](examples/README.md) — a worked catalogue ·
[`policy-reporter/`](policy-reporter/README.md) — where violations become readable

---

## The problem it solves

A cluster accumulates resources nobody would have approved: images from unknown registries, `latest`
tags, Pods with no limits, namespaces with no owner label. RBAC cannot express any of that, and CI
checks only cover the manifests that went through CI.

Kyverno is a mutating and validating admission webhook that can. Its distinguishing choice is the
language: policies are `ClusterPolicy`/`Policy` custom resources with `match`, `validate`, `mutate`,
`generate` and `cleanup` blocks. Anyone who can read a Deployment can read a policy, which is the
entire reason it has overtaken Gatekeeper in adoption — see [`../README.md`](../README.md#5-the-language-question)
for the comparison against Rego and WebAssembly.

Four capabilities, and most people only use the first:

| Capability | What it does | Example here |
|---|---|---|
| `validate` | accept or reject | `examples/disallow-latest-tag/clusterpolicy.yaml` |
| `mutate` | rewrite the object before it is stored | `examples/replace-image-registry.yaml` rewrites `docker.io/*` to a Harbor mirror |
| `generate` | **create** resources in response to an event | `policies/sync-secret/sync-tls-secret.yaml` clones a TLS secret into every namespace |
| `cleanup` | delete resources on a schedule | `examples/cleanup-label/` |

`generate` is the underrated one. A validating policy that requires every namespace to have a
NetworkPolicy produces a rejection and an annoyed engineer; a generating policy that creates the
NetworkPolicy produces a secure namespace. Policy doing work rather than refusing.

The controllers are split, which is why the HelmRelease has four replica counts:

| Controller | Job |
|---|---|
| admission | the webhook — validate and mutate on the write path |
| background | re-applies `generate` and `mutate` rules to existing resources |
| reports | produces `PolicyReport` resources |
| cleanup | runs `CleanupPolicy` on a schedule |

Only the admission controller is in the API server's critical path. That separation is a real
operational advantage over a monolith: the background controller can be slow or down without
blocking writes.

## When to use it

- **YAML is the shared language of the team.** This is the decisive factor. A policy that only one
  person can modify is a policy that does not get fixed during an incident.
- **You need `generate`.** Nothing else in [`../`](../README.md) does it. Per-namespace defaults —
  a NetworkPolicy, an image-pull Secret, a TLS Secret, a ResourceQuota — are the highest-value
  policies a platform can have, and they are creation, not validation.
- **You want the policy library.** <https://kyverno.io/policies/> is large and mostly
  copy-paste-and-tune. Several linked from the original notes are directly relevant:
  - <https://kyverno.io/policies/other/allowed-image-repos/allowed-image-repos/> — the allowed
    repositories rule, the Kyverno equivalent of the Gatekeeper constraint next door.
  - <https://kyverno.io/policies/other/allowed-base-images/allowed-base-images/> and
    <https://kyverno.io/policies/other/require-base-image/require-base-image/> — restrict what an
    image may be *built from*, which requires the base image to be recorded in the image annotations
    at build time. Supply-chain policy, not just deployment policy.
  - <https://kyverno.io/policies/best-practices/add-safe-to-evict/add-safe-to-evict/> — see the
    Notes below.
- **You want policies testable in CI.** `kyverno test` runs policies against fixtures without a
  cluster. [`examples/test/`](examples/test/README.md) is a worked example.
- **You want reports without extra work.** Kyverno emits `PolicyReport` resources natively;
  [Policy Reporter](policy-reporter/README.md) turns them into a UI and metrics.

## When not to use it

- **The policy logic is genuinely complex.** Deeply conditional rules become JMESPath expressions
  embedded in YAML, and they get unreadable faster than the Rego equivalent would. When a policy
  needs set arithmetic or cross-resource joins, [Gatekeeper](../gatekeeper/README.md) is the better
  tool.
- **OPA is already the platform's policy language.** If Rego is in use for the API gateway, for
  Kafka, or for CI, a second policy language is a cost.
- **You cannot accept a webhook in the write path.** Kyverno is a webhook like any other, with the
  same `failurePolicy` dilemma described in [`../README.md`](../README.md#3-the-failure-mode-decision).
  With `Fail` it is a cluster-wide single point of failure; with `Ignore` it is advisory.
- **You already run another admission engine.** Two webhooks means twice the latency and twice the
  failure surface.
- **You expect it to see runtime behaviour.** It sees the object once, at write time. Drift and
  in-cluster behaviour are [`../../runtime-security/`](../../runtime-security/README.md).

## Notes

Every original note from `doc.md`, translated and explained, plus the state of the folder.

### Dead configuration: the commented-out HelmRelease at the root

There are **two** HelmRelease files for Kyverno in this folder:

| File | State |
|---|---|
| `helmrelease.yaml` (folder root) | **entirely commented out.** The old `HelmRepository`-based version, chart 3.3.7, referencing `sourceRef: {kind: HelmRepository, name: kyverno}` |
| `helm/helmrelease.yaml` | the live one. Uses `chartRef: {kind: OCIRepository, name: kyverno}`, chart 3.8.1 pinned by digest |

`kustomization.yaml` lists `namespace.yaml`, `helm/ocirepository.yaml`, `helm/helmrelease.yaml` and
`rbac.yaml` — the root `helmrelease.yaml` is not referenced, so it is inert. It should be deleted.
Commented-out configuration that is not in the kustomization is worse than no configuration: it
looks authoritative, it is stale by two minor versions, and the next person to read it has to work
out which of the two is real.

`helm/helmrepository.yaml` is in the same position — the live source is the `OCIRepository`, and the
`HelmRepository` is left over from the migration.

The migration itself was worth doing: `OCIRepository` pins both a tag and a `digest`
(`sha256:61d8cd...`), so the chart that gets installed is byte-identical every time. A
`HelmRepository` plus a version constraint is not that guarantee.

### Suspending Kyverno on specific namespaces

From the live values, `configs/configmap.yaml` sets `resourceFilters` to skip `kyverno` itself,
`kube-system`, `kube-public`, `kube-node-lease`, `Node`, and `Event`. This is not tidiness — it is
the escape hatch that lets the cluster repair itself when the webhook is broken. See
[`../README.md`](../README.md#how-to-survive-either-choice).

Skipping `Event` is separately important: events are high-volume and evaluating policy on every one
of them is pure overhead.

### Spot instances and safe-to-evict

> spot, same as before
> `+(cluster-autoscaler.kubernetes.io/safe-to-evict): true`

The `+()` syntax is a Kyverno **add-if-absent anchor** in a mutate rule: set this annotation if it
is not already set, and leave it alone if the user specified something. That distinction is what
makes a defaulting policy safe — without it, the policy overwrites a deliberate `false`.

`cluster-autoscaler.kubernetes.io/safe-to-evict: true` tells the cluster autoscaler it may evict the
Pod in order to drain and remove a node. On spot instances, where nodes disappear anyway, marking
workloads evictable is what lets the autoscaler consolidate. Without it, a single Pod with a local
`emptyDir` volume can pin an entire node indefinitely.

The reference policy is
<https://kyverno.io/policies/best-practices/add-safe-to-evict/add-safe-to-evict/>. The note "spot,
same as before" links this to the [Gatekeeper](../gatekeeper/README.md) notes, where spot instances
are listed as an exemption to the tag policy for the same underlying reason: automation, not humans,
is changing these workloads.

### Global anchors

> <https://kyverno.io/docs/writing-policies/validate/#global-anchor>

A global anchor `<()` makes a validation rule *conditional*: the rest of the rule is only checked
when the anchored field matches. "If the container mounts a hostPath, then it must be read-only" —
the policy does not fire at all for containers that mount nothing.

This is the mechanism that keeps a validating policy from producing false rejections on workloads it
was never meant to cover, and it is the thing most often missing from a hand-written first draft.

### The three policies to write

> allowed repositories
> disallow tags
> https only

A shortlist of the intended policies for this platform. The first two are the same rules the
[Gatekeeper library](../gatekeeper/policies/README.md) next door implements, and Kyverno equivalents
already exist in [`examples/`](examples/README.md). "https only" — requiring TLS on Ingress and
rejecting plain-HTTP backends — is the one with no implementation anywhere in this folder yet.

### Recorded issue

> <https://github.com/kyverno/kyverno/discussions/14373>

An upstream discussion kept as a reference. Worth re-checking against the deployed chart version
(3.8.1) before assuming it still applies.

### HelmRelease shape

The live release is configured for a real cluster rather than a demo: three admission-controller
replicas with a `topologySpreadConstraint` across hostnames, two replicas each for the background,
cleanup and reports controllers, a `ServiceMonitor` for Prometheus, and node selectors plus
tolerations pinning everything to a `system` node pool.

Three spread replicas is the correct answer to the `failurePolicy: Fail` problem — it is what makes
`Fail` survivable. Pinning to the system pool is the same reasoning: keep the webhook off the nodes
that scale in and out.

`rbac.yaml` at the folder root grants the aggregated ClusterRoles Kyverno needs to read and manage
Secrets. That is a direct consequence of the `generate` rule in
[`policies/sync-secret/`](policies/sync-secret/README.md) — Kyverno cannot clone a Secret it is not
allowed to read, and the default install deliberately does not grant Secret access.

---

[← Admission policies](../README.md)
