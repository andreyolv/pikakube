[← Cluster scanners](../README.md)

# Polaris

<https://github.com/FairwindsOps/polaris>
<https://github.com/FairwindsOps/charts>

---

## The problem it solves

Most workloads running in a cluster are wrong in the same small number of ways, and nobody notices
until one of them causes an incident:

| Finding | What it causes later |
|---|---|
| No resource requests | the scheduler cannot place it sensibly; it starves or it starves others |
| No limits | one workload takes a node down |
| No liveness or readiness probe | traffic routed to a Pod that is not ready, and hung Pods never restarted |
| `image: latest` | nobody can say what is running |
| `runAsRoot`, writable root filesystem, privilege escalation allowed | a container escape becomes a node compromise |
| No `PodDisruptionBudget` | a node drain takes the service down |

Polaris checks all of it against a configurable set of best-practice rules and scores the result. It
is the most opinionated of the three cluster scanners here, and the opinions are mostly right.

**Three modes, and choosing between them is the real decision:**

| Mode | What it is | Use for |
|---|---|---|
| **Dashboard** | a long-running service with a web UI scoring the live cluster | visibility; a number people can watch move |
| **CLI audit** | `polaris audit` against manifests or a cluster, with an exit code | CI — this is where it actually changes behaviour |
| **Admission controller** | a validating webhook that rejects non-conforming workloads | enforcement |

## When to use it

- **in CI, against manifests, failing the build** — the mode with the highest return. A finding
  produced before merge is fixed; a finding on a dashboard is admired
- as a dashboard to establish a baseline and show whether things are getting better, particularly
  when arguing for time to fix them
- to make workload standards concrete: "requests and limits on everything, probes on everything" is
  a policy nobody can measure until Polaris counts the exceptions

## When not to use it

- **the admission-controller mode, if a policy engine is already deployed.** Kyverno or Gatekeeper
  (`security/2-cluster/policies/`) do enforcement with one mechanism for all policies. Running
  Polaris as a second admission webhook adds another thing in the path of every workload creation
  for a subset of the same job
- as a security tool. Polaris covers the security-adjacent workload settings, but posture scanning
  and CIS benchmarks live in the security discipline and go much further
- the dashboard alone. A score nobody is accountable for changes nothing, and the dashboard is the
  easiest of the three modes to deploy and forget

## Notes

Two recorded references: the project, <https://github.com/FairwindsOps/polaris>, and the chart
repository, <https://github.com/FairwindsOps/charts> — Fairwinds keeps charts for their whole
tooling range in one repository, so the `HelmRepository` is shared rather than per-tool.

**Deployed here**, via a Flux `HelmRelease` against the `fairwinds-stable` Helm repository, chart
version `5.17.1`, with `dashboard.replicas: 1`.

That configuration says something worth naming: **only the dashboard is deployed.** The webhook and
the CI audit are not in use. Per the section above, the dashboard is the mode that produces
visibility and the CI audit is the mode that produces change — so what exists today is a way to see
how many workloads are misconfigured, and no mechanism that prevents the number from growing.
Running `polaris audit` in the pipeline is the cheap next step and does not require anything new to
be installed.

Polaris is also the only tool in [`../`](../README.md) that is deployed rather than mapped, which
makes it the de facto cluster scanner here; [Marvin](../marvin/README.md) and
[Popeye](../popeye/README.md) are documented as CLIs.

---

[← Cluster scanners](../README.md)
