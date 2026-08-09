[← Gatekeeper](../README.md)

# Gatekeeper policy library

Five worked `ConstraintTemplate` + `Constraint` pairs, drawn from the
[gatekeeper-library](https://open-policy-agent.github.io/gatekeeper-library/website/). Together they
are the clearest available explanation of how Gatekeeper's two-object model works.

## Contents

1. [The two-object model, concretely](#1-the-two-object-model-concretely)
2. [The policies in this folder](#2-the-policies-in-this-folder)
   - [allowed-repositories](#allowed-repositories)
   - [disallow-tags](#disallow-tags)
   - [container-ratios](#container-ratios)
   - [required-labels](#required-labels)
   - [required-resources](#required-resources)
3. [Reading Rego without learning Rego](#3-reading-rego-without-learning-rego)
4. [Exemptions](#4-exemptions)
5. [Anti-patterns](#5-anti-patterns)
6. [How this applies to pikakube](#6-how-this-applies-to-pikakube)

---

## 1. The two-object model, concretely

Every folder here contains the same pair:

| File | What it is |
|---|---|
| `constraint-template.yaml` | a `ConstraintTemplate`: the Rego logic, plus an OpenAPI schema for its parameters. Applying it **creates a CRD**. |
| `constraint.yaml` | an instance of that CRD: which resource kinds it matches, what the parameters are, and which `enforcementAction` to take |

So applying `allowed-repositories/constraint-template.yaml` creates a new cluster resource type
called `K8sAllowedRepos`, and `constraint.yaml` is one object of that type. You can create ten more
`K8sAllowedRepos` objects with different allow-lists and different match rules without touching the
Rego once.

The `enforcementAction` field on the constraint is where audit-vs-enforce lives:

| Value | Effect |
|---|---|
| `dryrun` | violations recorded in the constraint's `status`, nothing blocked |
| `warn` | the request succeeds, the user gets a warning on their terminal |
| `deny` | the request is rejected |

`allowed-repositories/constraint.yaml` carries the comment `#dryrun warn deny` on that line, which
is a useful habit — the three values are not otherwise obvious.

## 2. The policies in this folder

| Folder | Template kind | Enforcement here | Matches |
|---|---|---|---|
| `allowed-repositories/` | `K8sAllowedRepos` | `dryrun` | Pods |
| `disallow-tags/` | `K8sDisallowedTags` | `warn` | Pods |
| `container-ratios/` | `K8sContainerRatios` | `deny` | Pods, excluding `kube-system` |
| `required-labels/` | `K8sRequiredLabels` | default (`deny`) | Namespaces |
| `required-resources/` | — | — | empty, only a `.gitkeep` |

Three different enforcement actions across three policies is not an accident — it is what a real
rollout looks like mid-flight. One policy is trusted enough to block, one is warning while people
adjust, one is still collecting data.

### allowed-repositories

Requires every container image to start with one of a list of prefixes. The Rego has three nearly
identical rules, one each for `containers`, `initContainers` and `ephemeralContainers` — a recurring
theme, and a common source of holes when someone writes only the first.

The constraint here allows only `openpolicyagent/`, which makes the two test files self-explanatory:
`test1.yaml` runs `openpolicyagent/opa:0.9.2` and passes, `test2.yaml` runs `nginx` and violates.
`example.yaml` and `example2.yaml` are Deployments (Ubuntu and a Flask app) rather than bare Pods —
useful because the constraint matches `Pod`, so what gets evaluated is the Pod the Deployment
creates, not the Deployment itself.

That last point matters more than it looks: a constraint matching only `Pod` rejects the *Pod*, so
the user sees a healthy Deployment with a ReplicaSet that cannot create anything, and the error is
buried in the ReplicaSet's events. Matching the workload kinds as well gives a better error, at the
cost of writing the rule against several shapes.

The violation message this template produces —
`container <%v> has an invalid image repo <%v>, allowed repos are %v` — is the string the log
extraction commands in [`../README.md`](../README.md) grep for.

### disallow-tags

Blocks a list of image tags, `latest` here. It has three example files rather than two, and the
third is the interesting one:

| File | Case |
|---|---|
| `example-allowed.yaml` | a pinned tag — passes |
| `example-disallowed.yaml` | `:latest` — blocked |
| `example-disallowed-notag.yaml` | **no tag at all** — also blocked |

No tag is the same as `:latest`, because that is what the container runtime resolves it to. A policy
that only checks the literal string `latest` misses the more common case, which is people omitting
the tag entirely. This template checks both, and the second message —
`didn't specify an image tag` — is the other string the log extraction greps for.

It is on `warn` here: the request succeeds and the user gets a warning, which is a reasonable middle
step for a rule that would break a lot of existing manifests.

### container-ratios

The most interesting of the five, and by some distance the longest. It enforces a maximum ratio of
`limits` to `requests` — configured here as `ratio: "1"` for memory and `cpuRatio: "10"` for CPU,
excluding `kube-system`.

What that encodes: **memory limit must equal memory request** (ratio 1, i.e. a Guaranteed-class
container for memory), while **CPU limit may be up to 10× the request**. That asymmetry is correct
and worth understanding — CPU is compressible, so a container exceeding its request gets throttled;
memory is not, so a container exceeding its request gets OOM-killed. Overcommitting CPU is a
scheduling decision, overcommitting memory is a reliability decision.

As a side effect it also rejects containers with no limits or no requests at all, which is why
`required-resources/` is empty: this template already covers it.

Most of the Rego is unit parsing. `canonify_cpu` normalises `100m`, `0.1` and `1` to a common
number; `canonify_mem` handles the whole `Ki`/`Mi`/`Gi`/`k`/`M`/`G` suffix table, including the
millibyte case Kubernetes accepts and probably should not — the template links
<https://github.com/kubernetes/kubernetes/issues/28741> in a comment about it. This is a good
argument both for and against Rego: the logic is genuinely intricate, and you did not have to write
it.

It is also the only one of the five that uses a `libs:` block — a shared `lib.exempt_container`
package implementing `is_exempt`, with prefix matching on `*`. Reusable helper libraries across
templates is a real Gatekeeper capability and one of the things Rego buys you.

### required-labels

Requires named labels to exist, optionally matching a regex. The constraint here targets
**Namespaces** rather than Pods and requires a `cks` key with no value constraint.

Namespace-level constraints are the cheapest high-value policy in Kubernetes: a required
`owner`/`team`/`cost-centre` label on every namespace turns chargeback and incident routing from
archaeology into a query. The blast radius is small, because namespaces are created rarely and by
people who can fix the error.

The template also supports a custom `message` parameter, which is the difference between a user
seeing a generic denial and seeing "namespaces must carry an owner label, see <runbook>".

### required-resources

Empty — just a `.gitkeep`. Its intent is covered by `container-ratios`, which already rejects
missing limits and requests. Worth either deleting or filling in; an empty policy folder reads as
unfinished work rather than a deliberate no-op.

## 3. Reading Rego without learning Rego

Enough to review a template:

```rego
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not strings.any_prefix_match(container.image, input.parameters.repos)
  msg := sprintf("container <%v> has an invalid image repo <%v>, ...", [container.name, container.image])
}
```

| Element | Meaning |
|---|---|
| `violation[...]` | a **set** rule. Gatekeeper reads this set; an empty set means no violation. |
| `{ ... }` body | every line must hold. Lines are ANDed, there is no `and` keyword. |
| `[_]` | iterate over every element. The rule is evaluated once per container. |
| `input.review.object` | the Kubernetes object being admitted |
| `input.parameters` | the `parameters` block from the `Constraint` |
| `not` | negation — the rule fires when the prefix does *not* match |
| several rules with the same head | ORed. Any one holding produces a violation. |

That last one is the mental model people miss: three separate `violation` rules for containers,
initContainers and ephemeralContainers are not three functions — they are three ways for the same
set to be non-empty.

## 4. Exemptions

Two mechanisms are visible here, and the difference matters:

| Mechanism | Example | Scope |
|---|---|---|
| `exemptImages` parameter | `disallow-tags/constraint.yaml`: `exemptImages: ["openpolicyagent/opa-exp:latest"]` | one image |
| `excludedNamespaces` in `match` | `container-ratios/constraint.yaml`: `- kube-system` | everything in a namespace, forever |

Prefer the first. A namespace exclusion exempts everything that will ever run there, including
things that do not exist yet. `kube-system` is the legitimate case, because you do not control what
the control plane schedules there and blocking it can prevent the cluster from repairing itself.

The `exemptImages` schema in these templates warns about this directly: use the fully-qualified
image name starting with a registry domain, otherwise `my-image-*` also exempts
`untrusted-registry.example.com/my-image-evil`.

## 5. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Editing the `ConstraintTemplate` to change a value | the Rego is the reusable part; you have forked a library template | change `parameters` on the `Constraint` |
| A rule that checks only `containers` | `initContainers` and `ephemeralContainers` bypass it entirely | one rule per container type, as all five templates do |
| Matching only `Pod` and expecting a good error | the Deployment succeeds and the failure hides in ReplicaSet events | match the workload kinds too, or accept the trade and document it |
| `deny` on day one | the first deployment fails and policy gets blamed | `dryrun` → collect → `warn` → `deny`, which is the spread visible in this folder |
| `excludedNamespaces` as the default exemption | exempts everything that will ever run there | `exemptImages`, scoped to one fully-qualified image |
| Unqualified prefixes in `exemptImages` | `my-image-*` matches any registry | start the pattern with a domain |
| Changing a violation message casually | the log-extraction tooling greps for the exact string | treat messages as an interface |
| Empty policy folders left in place | reads as unfinished, and nobody knows if it is intentional | delete it or fill it in |

## 6. How this applies to pikakube

This library is the most valuable part of the Gatekeeper folder even though Gatekeeper is not the
engine in the delivery path here — [Kyverno](../../kyverno/README.md) is. Five templates with
matching examples, three different enforcement actions, and a real exemption strategy are a better
tutorial on admission control than any single document.

Three of these five have direct Kyverno equivalents already present in
[`../../kyverno/examples/`](../../kyverno/examples/README.md) — allowed repositories, disallow
`:latest`, and require requests and limits — which makes this folder a useful side-by-side
comparison of the two languages on identical problems.

The one with no Kyverno equivalent here is `container-ratios`, and it is the one with the most
platform value: for a data platform where Spark executors and Airflow workers are sized by people
who are not thinking about QoS classes, "memory limit must equal memory request, CPU may burst 10×"
is a genuinely good default and a hard rule to express without the unit-parsing that this template
already contains.

---

[← Gatekeeper](../README.md)
