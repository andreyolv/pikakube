[← Manifest scan](../README.md)

# kube-linter

<https://github.com/stackrox/kube-linter>

Context and comparison against the other tools: [../README.md](../README.md)

---

## The problem it solves

kube-linter checks Kubernetes YAML (and Helm charts) against a set of **production-readiness
and security** rules, before the manifests ever reach a cluster. Where kubesec is a single
security score on the pod spec, kube-linter is a broad checklist across the things that make
a workload behave — or misbehave — in production.

The default checks cover the mistakes that cause real incidents:

| Category | Example checks |
|---|---|
| Reliability | no liveness/readiness probe, no resource requests/limits, a Deployment with one replica, no `PodDisruptionBudget` |
| Security | running as root, writable root filesystem, dangerous capabilities, privileged containers, host mounts |
| Correctness | a Service selector matching no pods, a dangling ConfigMap/Secret reference, mismatched labels |
| Hygiene | `latest` image tag, missing `imagePullPolicy`, deprecated API versions |

The framing that matters: kube-linter is not only a security tool. Half of what it catches
is *reliability* — the missing probe and the absent resource limit are what page you at 3am,
not what an attacker exploits. It is a "will this survive contact with a real cluster" check
as much as a "is this safe" check.

Checks are configurable — you enable, disable, or tune them per repository with a config
file — which lets a team encode its own house rules rather than argue about them in review.

## When to use it

- A **CI gate on every manifest and Helm chart** in the repo, catching the cheap and obvious mistakes before merge
- Enforcing team conventions (probes required, limits required, no `latest`) as code rather than as review comments
- Linting Helm charts by rendering them first — it understands templated output
- The reliability net that kubesec and checkov do not fully provide — the probe/limit/replica checks are its home turf

## When not to use it

- **As admission control.** It runs in CI on files. Anything applied to the cluster outside that pipeline — `kubectl apply` by hand, an operator generating resources, a Helm install from a laptop — is never seen by it. Enforcement belongs to `policies/`, and the parent README explains why this gap is the whole reason admission control exists
- As a deep pod-security score. kubesec is more focused and more opinionated on `securityContext`; kube-linter's security checks are broader but shallower
- As broad IaC coverage. It is Kubernetes-only. Terraform, Dockerfiles and CloudFormation are [checkov](../checkov/README.md)'s territory
- Expecting runtime findings. It reads static YAML. What a pod *does* once running is `runtime-security/`

## Notes

The original note in this folder was the project link and nothing else:

- <https://github.com/stackrox/kube-linter> — the upstream repository, from StackRox
  (now part of Red Hat).

Points worth recording alongside it:

- **Reliability, not just security.** It is easy to file kube-linter under "security scanner"
  and miss half its value. The probe, resource-limit, replica-count and PDB checks are
  operational-readiness checks. On a platform, those catch more real outages than the
  security rules catch breaches.
- **Configurable check set.** The default checks are a reasonable starting point, but the
  intended use is to curate a per-repo config: turn off what does not apply, turn on the
  stricter checks, and commit that file so the ruleset is reviewable like any other code.
- **It renders Helm.** Point it at a chart and it templates first, so it lints the manifests
  that would actually be applied — not the raw templates. This matters in a repo where most
  workloads arrive as charts.
- **Same CI-only ceiling as the whole folder.** A green kube-linter run proves the files in
  the repo are clean. It proves nothing about what is running in the cluster. That is the
  standing caveat for every tool here.

---

[← Manifest scan](../README.md)
