[← Admission policies](../README.md)

# Gatekeeper

<https://github.com/open-policy-agent/gatekeeper>
<https://github.com/open-policy-agent/opa>
<https://github.com/open-policy-agent/gatekeeper-library>
<https://open-policy-agent.github.io/gatekeeper-library/website/>
<https://github.com/sigstore/cosign-gatekeeper-provider>

OPA's admission controller for Kubernetes. Policies are Rego, split into a reusable
`ConstraintTemplate` and a parameterised `Constraint`.

Policies in this repo: [`policies/`](policies/README.md)

---

## The problem it solves

Kubernetes RBAC answers *who may create a Pod*. It has no way to say *and not a privileged one, and
not from Docker Hub, and only with resource limits*. Gatekeeper is a validating (and optionally
mutating) admission webhook that answers the second question, using OPA as its policy engine.

Its specific contribution over "just run OPA" is the two-object split:

| Object | Contains | Written by |
|---|---|---|
| `ConstraintTemplate` | the Rego, plus an OpenAPI schema for its parameters. Creates a CRD. | whoever knows Rego |
| `Constraint` | an instance of that CRD: which resources it matches, which parameters, which enforcement action | whoever knows the cluster |

That separation is the reason a platform team can maintain five templates and let others tune
dozens of constraints without touching Rego. `allowed-repositories/constraint-template.yaml` in this
repo defines `K8sAllowedRepos` with a `repos` array parameter; `constraint.yaml` then instantiates
it with `repos: ["openpolicyagent/"]` and `enforcementAction: dryrun`. Same logic, different
policy, no Rego edited.

Two more things Gatekeeper adds on top of raw OPA:

- **Audit.** A background loop re-evaluates existing objects against the constraints and records
  violations in the constraint's `status`. Admission only sees new writes; audit is how you find out
  what was already wrong.
- **Replication (`syncSet`/`config`).** Rego can only reason about data it has. Gatekeeper can
  mirror selected cluster resources into OPA's cache so a policy can say "no two Ingresses may claim
  the same host" — a rule that requires knowing about objects other than the one being admitted.

## When to use it

- **The team already uses OPA.** Rego written for an API gateway, for Kafka authorisation, or for
  Terraform review transfers directly. The linked post on
  <https://opencredo.com/blogs/controlling-kafka-data-flows-using-open-policy-agent/> is that case
  outside Kubernetes: OPA deciding which Kafka topics a client may touch. If OPA is already the
  policy language of the platform, having a second one for Kubernetes is the odd choice.
- **The policy is genuinely complex.** Set operations, cross-resource comparisons, and conditional
  logic are what Rego is for. The equivalent in Kyverno's JMESPath gets hard to read well before
  Rego does.
- **You want the community library.** The gatekeeper-library is a large, maintained catalogue of
  templates — the five in [`policies/`](policies/README.md) are drawn from it — and it also carries
  the Pod Security Standards as constraint templates.
- **Supply-chain verification via an external provider.** `cosign-gatekeeper-provider` lets a
  constraint call out to verify an image signature at admission. External data providers are the
  mechanism for any check that needs an answer Gatekeeper does not hold.
- **You need the two-tier split.** Where policy authorship and policy configuration are done by
  different people, the template/constraint split is a real organisational fit.

## When not to use it

- **Nobody on the team wants to learn Rego.** This is the decisive factor and it is not a soft one.
  Rego is a declarative logic language; `violation[{"msg": msg}] { ... }` is a rule that holds for
  every binding that satisfies its body. It is unlike anything most platform engineers write, and a
  policy nobody can modify becomes a policy nobody can fix under pressure.
- **You need to generate resources.** Gatekeeper validates and mutates. It cannot create a
  NetworkPolicy or copy a Secret into a new namespace — that is Kyverno's `generate`, and it is
  often the more valuable capability. See [`../kyverno/`](../kyverno/README.md).
- **You want readable violation reporting out of the box.** Violations live in each constraint's
  `status`, capped by `constraintViolationsLimit` — set to 100 in this repo's HelmRelease, and
  20 by default. The Notes below record the workaround, and it is not pleasant.
- **Kyverno would do the job.** For "require a label", "block `:latest`", "require limits", the
  Kyverno version is shorter, readable by anyone, and equally effective. Reach for Rego when the
  policy earns it.
- **You already run another admission engine.** Two webhooks in the API server write path is twice
  the latency and twice the outage surface. Pick one.

## Notes

Every original note from `doc.md`, translated and explained.

### Tag policy exemptions

> Tag policy exceptions: Flux, spot — automatic tag updates.

The `disallow-tags` constraint blocks mutable tags such as `:latest`. Two things in this platform
legitimately change image tags without a human: **Flux** (its image-automation controllers rewrite
tags in Git as new images appear) and **spot**-instance related components, which update
automatically. Both must be exempted or they fight the policy.

The right way to write these exemptions is narrowly — `disallow-tags/constraint.yaml` uses
`exemptImages: ["openpolicyagent/opa-exp:latest"]`, which exempts a specific image rather than a
whole namespace. A namespace-wide exemption would also exempt everything else that happens to run
there.

### Reading violations from the CRD, and why it does not scale

> We can try to get non-compliant images from the CRD, but it is limited to 20 records.

```bash
kubectl get K8sAllowedRepos -o json | jq -r '["NAMESPACE", "NAME", "MESSAGE"], (.items[].status.violations[] | [.namespace, .name, .message]) | @tsv' | column -t -s $'\t' | tr '\t' '|' > images-dev.yaml
```

Gatekeeper's audit loop writes violations into `status.violations` on each constraint, and truncates
that list — 20 entries by default, raised to 100 by `constraintViolationsLimit` in this repo's
HelmRelease. On a cluster where hundreds of Pods violate a newly-added policy, the status shows an
arbitrary 20 (or 100) of them, so it cannot be used to build the exemption list. This is the single
biggest practical friction in adopting Gatekeeper on an existing cluster.

### Reading violations from the logs instead

> The best option is to take the list from the Gatekeeper pod logs, for each cluster.

```bash
kubectl logs -l gatekeeper.sh/system=yes -n gatekeeper-system --tail 2000 | jq -c -R -r 'fromjson? | select(.resource_namespace != null and .resource_name != null and .msg != null) | "\(.resource_namespace)\t\(.resource_name)\t\(.msg)"' | grep "has an invalid image repo" | sort | uniq | column -t -s $'\t' | tr '\t' '|' > images-dev.yaml

kubectl logs -l gatekeeper.sh/system=yes -n gatekeeper-system --tail 2000 | jq -c -R -r 'fromjson? | select(.resource_namespace != null and .resource_name != null and .msg != null) | "\(.resource_namespace)\t\(.resource_name)\t\(.msg)"' | grep "didn't specify an image tag" | sort | uniq | column -t -s $'\t' | tr '\t' '|' > images-dev.yaml
```

Gatekeeper logs JSON, one object per line. `fromjson?` parses each line and silently drops anything
that is not JSON; the `select` keeps only lines carrying a resource and a message; the rest is
formatting.

The two `grep` strings are the violation messages produced by the constraint templates in this
folder — `has an invalid image repo` comes from the `sprintf` in
`allowed-repositories/constraint-template.yaml`, and `didn't specify an image tag` from
`disallow-tags`. That coupling is worth noting: the extraction depends on the exact wording of the
message in the Rego, so changing a message breaks the tooling built on it.

Both commands redirect to the same filename, so they are alternatives, run one at a time. The
`--tail 2000` is the real limitation — this reads a log buffer, so violations older than the buffer
are gone. Shipping Gatekeeper's logs to a log store makes this query reliable instead of
best-effort.

### Merging results across clusters

> Now merge the files from each cluster into one, without duplicates.

```bash
awk '{$1=$2=""; print $0}' images-*.yaml | sort | uniq | awk -F '<|>' '{print $4}' > all-images.txt
```

The first `awk` blanks the namespace and name columns, leaving the message. The second splits on
`<` and `>` — the constraint template wraps values in angle brackets
(`container <%v> has an invalid image repo <%v>`), so field 4 is the image reference. The result is
a deduplicated inventory of every image that violates the policy across every cluster, which is the
input to building the allowed-repositories list.

### Splitting the images by registry

> Commands to separate registries by origin.

```bash
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*quay\.io.*$' > quay-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*gcr\.io.*$' > gcr-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*ghcr\.io.*$' > ghcr-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*registry\.k8s\.io.*$' > registry-k8s-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep -vE '^(quay\.io|gcr\.io|ghcr\.io|registry\.k8s\.io)' > dockerhub.txt
```

The same extraction, bucketed per registry. The last line inverts the match, so anything not
prefixed with a known registry lands in `dockerhub.txt` — Docker Hub is the implicit default when an
image reference carries no registry, which is exactly why it is the interesting bucket. Images with
no explicit registry are the ones that will break first when a pull-through mirror or an allowed-repos
policy is introduced.

This whole sequence is the audit-before-enforce workflow made concrete: collect violations, group
them, decide which registries are legitimate, write the allow-list, then flip the constraint from
`dryrun` to `deny`.

---

[← Admission policies](../README.md)
