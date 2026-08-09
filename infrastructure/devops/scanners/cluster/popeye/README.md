[← Cluster scanners](../README.md)

# Popeye

<https://github.com/derailed/popeye>

---

## The problem it solves

A cluster that has been running for a year contains a great deal that nobody meant to leave there,
and none of it produces an error:

- ConfigMaps and Secrets that no workload references
- Services with no matching endpoints, pointing at Deployments that were renamed
- ServiceAccounts, Roles and RoleBindings left over from something removed
- PersistentVolumeClaims bound to nothing
- containers requesting far more CPU and memory than they ever use, and containers requesting far
  less than they need

Popeye is a **read-only cluster sanitiser**. It scans the live cluster, applies a set of checks, and
reports findings by severity and by resource. It requires no installation into the cluster — it is
a CLI using your kubeconfig — and it changes nothing.

Its distinctive strength is the **dangling-reference and utilisation** category. Other scanners
mostly ask "is this workload configured well?"; Popeye also asks "does this thing point at anything,
and is anyone using it?", which is the question that finds accumulated debt.

It comes from the author of `k9s`, and the sensibility shows: a fast CLI producing a readable report,
with output formats (including HTML and JSON) for when it needs to feed something else.

## When to use it

- **a periodic cluster audit** — quarterly, or on inheriting a cluster nobody can explain
- finding unused resources and dangling references before they cause confusion during an incident
- a quick sanity check after a large migration or a batch of deletions, to see what was orphaned
- reviewing resource requests against actual utilisation, as an input to right-sizing

## When not to use it

- **as a gate.** It is a diagnostic. Wiring it into CI as a pass/fail check produces noise, because
  a well-run cluster still has findings that are deliberate
- as a substitute for workload best-practice checking in CI — [Polaris](../polaris/README.md) and
  [kube-score](../../manifest/kube-score/README.md) are aimed at that and run against manifests
  before anything is applied
- for security posture or CIS benchmarks — that is the security discipline
- if nobody has agreed what to do with the output. A long report read once and ignored is the
  standard outcome for this category of tool

## Notes

The only recorded reference is the repository: <https://github.com/derailed/popeye>.

Nothing is deployed for it; it is a CLI, and running it as a CLI is the point.

The way to use it well is to run it, triage the findings once into "fix" and "expected", and then
compare future runs against that baseline. Read cold, the first report on any real cluster is long
enough to be dismissed — which is how the tool ends up remembered as noisy rather than useful.

Where it sits relative to the other two in [`../`](../README.md): [Polaris](../polaris/README.md)
is about **workload configuration quality**, [Marvin](../marvin/README.md) is about **extensible
checks and CVE exposure**, and Popeye is about **cruft and dangling references**. They overlap, but
Popeye is the only one of the three that reliably answers "what is in here that shouldn't be", which
is the direct link between this folder and [`cleanup/`](../../../cleanup/README.md) — Popeye finds
the accumulation, and cleanup tooling prevents it.

---

[← Cluster scanners](../README.md)
