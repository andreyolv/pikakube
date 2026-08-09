[← Kyverno](../README.md)

# Kyverno examples

A worked catalogue: policies plus the resources that pass and fail them. Reference material, not
cluster configuration.

Subfolder with its own notes: [`test/`](test/README.md) — testing policies with the Kyverno CLI

## Contents

1. [How the folder is organised](#1-how-the-folder-is-organised)
2. [validate — refuse](#2-validate--refuse)
3. [mutate — rewrite](#3-mutate--rewrite)
4. [mutate existing — reach out and change other things](#4-mutate-existing--reach-out-and-change-other-things)
5. [cleanup — delete on a schedule](#5-cleanup--delete-on-a-schedule)
6. [The anchors, in one place](#6-the-anchors-in-one-place)
7. [Anti-patterns](#7-anti-patterns)
8. [How this applies to pikakube](#8-how-this-applies-to-pikakube)

---

## 1. How the folder is organised

Two conventions are mixed here, which is worth knowing before reading:

- **Subfolders** contain a `clusterpolicy.yaml` plus one or more resources to test it against
  (`pod.yaml`, `deployment.yaml`, `example.yaml`). Apply the policy, apply the resource, observe.
- **Loose `.yaml` files** at the top level are policies on their own, mostly taken from the
  [Kyverno policy library](https://kyverno.io/policies/).

Two files are not policies at all: `namespace.yaml` creates a namespace called `foobar` for
testing, and `namespace-airflow-helmrelease.yaml` is a Flux `HelmRelease`.

Nothing in this folder is referenced by the Kyverno `kustomization.yaml`, so none of it is applied
by Flux. That is the correct arrangement for a catalogue — the policies intended for the cluster
live in [`../policies/`](../policies/README.md).

## 2. validate — refuse

| File | What it enforces | Mode |
|---|---|---|
| `disallow-latest-tag/clusterpolicy.yaml` | an image tag is present, and it is not `latest` | `Enforce` |
| `require-labels/clusterpolicy.yaml` | `app.kubernetes.io/name` is set | `Audit` |
| `require-requests-limits/clusterpolicy.yaml` | CPU and memory requests, and a memory limit | `Enforce` |
| `disallow-default-namespace.yaml` | Pods and controllers are not in `default` | `Audit` |
| `block-large-images.yaml` | container images under 2 GiB | `Audit` |
| `namespace-delete-protection.yaml` | namespaces cannot be updated or deleted | `enforce` |

Four of these are worth reading closely.

**`disallow-latest-tag`** has two rules, not one: `require-image-tag` (the image must have a tag at
all) and `validate-image-tag` (that tag must not be `latest`). Untagged is the same as `latest` to
the runtime, and a policy that only checks the literal string misses the more common mistake. This
is the same pair the Gatekeeper `disallow-tags` template implements next door.

**`require-requests-limits`** requires a *memory* limit but not a CPU limit. That is deliberate and
correct: CPU is compressible, so a container over its request is throttled; memory is not, so a
container over its limit is OOM-killed. A CPU limit mostly causes throttling nobody asked for.
Compare with the Gatekeeper `container-ratios` policy, which enforces the ratio between them.

**`block-large-images.yaml`** is the most interesting policy in the folder, because it does
something no other engine here can do without an external provider: it calls out to the **registry**
during admission. The `context` block uses `imageRegistry` to fetch the image manifest and sums
`manifest.layers[*].size`. That means admission now depends on registry reachability and adds a
network round-trip to every Pod creation — powerful, and a real availability consideration.

Its `preconditions` block skips `DELETE` operations, and the `{{request.operation || 'BACKGROUND'}}`
idiom is worth internalising: during a background scan there is no request, so the expression
defaults. Any policy using `request.operation` needs it.

**`namespace-delete-protection.yaml`** blocks `UPDATE` and `DELETE` on namespaces outright. Its
description was clearly adapted from a Service-based policy and still says "Service resource that
contains the label `protected=true`" — the rule as written protects *every* namespace and checks no
label. As a demonstration of expressing "deny this verb" that is fine; as something to apply, it
would prevent labelling a namespace, which breaks a great deal, including
[`label-existing-namespaces`](#4-mutate-existing--reach-out-and-change-other-things) in this same
folder.

It is also the clearest illustration of what Kyverno adds over RBAC: RBAC grants verbs on kinds and
names, and cannot express "unless the object carries this label". This can.

## 3. mutate — rewrite

| File | What it changes |
|---|---|
| `add-labels/clusterpolicy.yaml` | adds `foo=bar` to Pods, Services, ConfigMaps and Secrets |
| `set-image-pull-policy/clusterpolicy.yaml` | sets `imagePullPolicy: IfNotPresent` on images ending in `:latest` |
| `replace-image-registry/clusterpolicy.yaml` and `replace-image-registry.yaml` | rewrites `docker.io/*` to a Harbor mirror |
| `add-ttl-jobs/clusterpolicy.yaml` | adds `ttlSecondsAfterFinished` to Jobs with no owner |

`replace-image-registry` is the one with real platform value and it is present twice — a bare rule
in the subfolder, and a fuller `replace-image-registry-with-harbor` version at the top level.

The mechanism is worth reading:

```
image: "{{ regex_replace_all('^docker.io/(.*)$', image_normalize('{{element.image}}'), 'harbor.corp.org/$1' )}}"
```

`image_normalize` is what makes it work. A user writes `nginx`; the actual reference is
`docker.io/library/nginx:latest`. Normalising first means the regex sees a consistent string
regardless of how lazily the image was written. A hand-rolled string replace on the raw value misses
every unqualified image, which is most of them.

This solves Docker Hub rate limiting and gives a single choke point for image provenance — and it is
the mutating counterpart to the Gatekeeper `allowed-repositories` constraint. One rewrites, one
rejects. Rewriting is friendlier and hides the change; rejecting is visible and annoying. See
[`../../README.md`](../../README.md#2-validating-vs-mutating) on why that trade matters.

`add-ttl-jobs` is a small policy with a large effect: Jobs with no `ownerReference` (created by
humans, not by CronJobs) never get cleaned up, and on a data platform they accumulate for months.
Setting `ttlSecondsAfterFinished` hands the problem to the built-in TTL controller.

`set-image-pull-policy` is the one that looks harmless and is not: setting `IfNotPresent` on a
`:latest` image means the node keeps whatever it already cached, so `:latest` stops meaning latest.
That may be what you want, and it must be a deliberate choice.

## 4. mutate existing — reach out and change other things

Three policies here mutate objects *other than* the one being admitted. This is Kyverno's
`mutate.targets` capability and it is the mechanism behind the whole "reload on secret change"
problem.

| File | Trigger | Target |
|---|---|---|
| `refresh-env-var-in-pods.yaml` | a `Secret` labelled `kyverno.io/watch: "true"` is updated | writes a random annotation into every `Deployment` consuming it via `secretKeyRef`, forcing a rollout |
| `refresh-volumes-in-pods.yaml` | a `ConfigMap` labelled `kyverno.io/watch: "true"` is updated | annotates the Pods mounting it, so the kubelet refreshes the volume immediately instead of after 60–90 seconds |
| `restart-deployment-on-secret-change.yaml` | a Secret changes | restarts the named Deployment |
| `label-existing-namespaces/clusterpolicy.yaml` | any AdmissionReview on a Namespace | labels **all** namespaces, including pre-existing ones |

The first two matter directly to [`../../../secrets/`](../../../secrets/README.md): rotating a
secret does nothing if the consumer never re-reads it. Environment variables from `secretKeyRef` are
set at container start and **never change** — the only fix is a new Pod. `refresh-env-var-in-pods`
produces one by writing `corp.org/random: "{{ random('[0-9a-z]{8}') }}"` into the Deployment's Pod
template, which is a change to the template, which triggers a rollout. That trick — mutate an
annotation you do not care about in order to cause a rollout — is the standard mechanism, and it is
what Reloader-style controllers do too.

The opt-in label `kyverno.io/watch: "true"` is the important design detail: without it, every Secret
update in the cluster would roll every Deployment that references it.

`label-existing-namespaces` demonstrates the counterpart of the `generateExisting` problem described
in [`../policies/sync-secret/`](../policies/sync-secret/README.md): admission-triggered rules only
see new objects, and reaching backwards requires an explicit mechanism.

All of these need extra RBAC — Kyverno's background controller must be allowed to update
Deployments and Pods, which it is not by default.

## 5. cleanup — delete on a schedule

`cleanup-label/pod.yaml` contains no policy at all, just a Pod with:

```yaml
labels:
  cleanup.kyverno.io/ttl: 2m
```

That label is understood natively by Kyverno's cleanup controller: the object is deleted two minutes
after creation, with no policy required. It accepts a duration (`2m`, `8h`) or an absolute
timestamp.

Deletion-by-label is convenient and worth treating carefully — anyone who can label a resource can
schedule its deletion.

`add-ttl-jobs` solves a similar problem through the Kubernetes TTL controller instead, which is
preferable when the built-in mechanism exists.

## 6. The anchors, in one place

Kyverno's pattern syntax is where most of the learning curve is. Every form appears somewhere in
this folder:

| Anchor | Meaning | Seen in |
|---|---|---|
| `"*"` | any value, but the field must exist | `disallow-latest-tag` (`image: "*:*"`) |
| `"!default"` | must not equal | `disallow-default-namespace` |
| `"?*"` | any non-empty value | `require-labels` |
| `(field)` | **conditional** — only apply the rest if this matches | `set-image-pull-policy` (`(image): "*:latest"`) |
| `+(field)` | **add if absent** — do not overwrite what the user set | the `safe-to-evict` policy described in [`../README.md`](../README.md) |
| `<(field)` | **global anchor** — the rule applies only where this matches | `refresh-env-var-in-pods` (`<(name)`) |
| `X(field)` | negation anchor — apply where this does *not* match | — |

`+()` is the one to internalise for any defaulting policy. Without it, a mutate rule overwrites a
value the user set deliberately, and the user has no way to opt out.

## 7. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Applying these examples as-is | several are demonstrations with placeholder values (`foo=bar`, `harbor.corp.org`) | copy into [`../policies/`](../policies/README.md), adapt, review |
| Trusting a policy's description | `namespace-delete-protection.yaml` describes a label check its rule does not do | read the `spec`, not the annotation |
| Mutate without `+()` | overwrites values the user set on purpose, silently | add-if-absent anchors for defaults |
| Registry-calling policies without thinking about availability | admission now depends on the registry being up and adds latency to every Pod create | narrow the match, and know the failure mode |
| `mutate.targets` policies without the extra RBAC | the rule fails silently in the controller log | grant the specific update permission |
| Refresh policies without the opt-in label | every Secret update rolls every Deployment that reads it | keep `kyverno.io/watch: "true"` as the gate |
| `set-image-pull-policy` on `:latest` in production | the node keeps a cached image and `latest` stops meaning latest | decide deliberately; better still, ban `:latest` |
| Leaving a catalogue and live policy in one folder | nobody can tell what is enforced | this folder is examples; `../policies/` is the cluster |

## 8. How this applies to pikakube

This is the most useful reference folder in the whole `policies/` subtree, and three of the policies
here are directly relevant to problems this platform has:

**`replace-image-registry`** — Docker Hub rate limits are a real cause of failed deployments, and
this is the mutating fix. It pairs with the registry inventory work recorded in the
[Gatekeeper notes](../../gatekeeper/README.md), which produces exactly the list of registries in use
that this policy would need.

**`refresh-env-var-in-pods` and `restart-deployment-on-secret-change`** — the missing half of the
secrets story. [`../../../secrets/`](../../../secrets/README.md) has external-secrets syncing values
from Vault, and nothing that makes a running workload notice a rotated credential. These policies
are that mechanism.

**`add-ttl-jobs`** — a data platform creates Jobs constantly, and the ones without an owner never go
away.

The catalogue also duplicates three Gatekeeper constraints from
[`../../gatekeeper/policies/`](../../gatekeeper/policies/README.md) — disallow `:latest`, require
resources, restrict registries — which makes the pair of folders a genuine side-by-side comparison
of YAML against Rego on identical problems. That comparison is worth more than either folder alone.

---

[← Kyverno](../README.md)
