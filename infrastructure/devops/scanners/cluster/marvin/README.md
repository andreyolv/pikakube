[← Cluster scanners](../README.md)

# Marvin

<https://github.com/undistro/marvin>

---

## The problem it solves

Cluster scanners usually ship a fixed set of checks written in Go, so extending them means forking
them. Marvin's answer is to make the checks **data**: each check is a YAML document containing one
or more [CEL](https://github.com/google/cel-spec) expressions evaluated against the resources it
selects.

```
# a check declares: which kinds to look at, and a CEL expression that must hold
```

That has two consequences worth caring about:

| Consequence | Why it matters |
|---|---|
| Writing a new check is writing a YAML file | no Go, no fork, no build |
| The check set is versionable and reviewable | it lives in a repository like everything else |

Marvin ships a built-in set covering Kubernetes misconfigurations, workload best practices, and
checks derived from known Kubernetes CVEs — the last being unusual: most scanners check *your*
configuration, and few check whether the cluster is exposed to a specific published vulnerability.

It runs as a CLI against a live cluster and produces a report grouped by severity.

## When to use it

- **custom organisational checks** are the requirement, and maintaining them as YAML rather than as
  a fork is the difference between doing it and not
- as a scheduled or CI-run audit against a cluster, producing a report
- when checking exposure to known Kubernetes CVEs matters, alongside ordinary best-practice checks
- alongside rather than instead of [Polaris](../polaris/README.md) — the check sets overlap but do
  not coincide

## When not to use it

- **as an admission controller.** Marvin reports; it does not block. If the requirement is
  "unsafe workloads must not be admitted", that is a policy engine — Kyverno or Gatekeeper, under
  `security/2-cluster/policies/` — and a scanner is the wrong shape of tool
- if a dashboard and a long-running service are wanted; Polaris covers that and Marvin does not
- for CIS benchmark compliance specifically. That is `kube-bench`, under
  `security/2-cluster/posture/`, and it answers a different question
- if nobody will read the report. This applies to every tool in this folder and it is the actual
  failure mode

## Notes

The only recorded reference is the repository: <https://github.com/undistro/marvin>.

Marvin comes from Undistro, alongside their other Kubernetes tooling. Nothing is deployed for it
here — it is mapped as a CLI, which is the natural way to run it.

The reason it is worth having in the folder next to [Polaris](../polaris/README.md) and
[Popeye](../popeye/README.md): the three answer overlapping questions with different biases.
Polaris is opinionated about **workload configuration**, Popeye is good at **unused and dangling
resources**, and Marvin is the **extensible** one, plus the only one that looks at cluster
vulnerability exposure. The comparison is drawn out in [`../README.md`](../README.md).

CEL is worth knowing independently of Marvin. It is the same expression language used by Kubernetes
validating admission policies and by Kyverno's newer CEL rules, so checks written here translate
conceptually to enforcement later — which is the natural progression from *scanning* to *blocking*
described in [`../../README.md`](../../README.md).

---

[← Cluster scanners](../README.md)
