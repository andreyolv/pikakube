[← Test](../README.md)

# Sonobuoy

<https://github.com/vmware-tanzu/sonobuoy>

---

## The problem it solves

Sonobuoy runs the **upstream Kubernetes conformance suite** against a cluster and gives you the
result as a tarball you can inspect or submit. It is the tool behind the CNCF's Certified Kubernetes
programme — the same tests every distribution must pass to use the name.

Practically: it deploys itself into the cluster, runs the end-to-end tests as pods, collects the
results and cleans up. It also gathers cluster state — resource dumps, logs, node information — which
makes the output useful for diagnosis and not only for a pass or fail.

## When to use it

- After building a cluster by hand, with Kubespray, or with Cluster API, before deploying anything real
- After every minor-version upgrade — the run most often skipped
- After changing the CNI, the CSI driver or the container runtime
- Producing evidence that a cluster is conformant, for an audit or a certification submission

## When not to use it

- On a busy production cluster without a maintenance window; the tests are disruptive
- As a performance, security or configuration assessment — it tests API conformance only
- On managed clusters, where the provider has already certified them
- As a substitute for testing your own workloads

## Notes

Recorded as a link only.

**Modes matter**, because the full run is long:

- **`--mode quick`** — a small subset, minutes. The routine health check.
- **`--mode certified-conformance`** — the full suite, typically an hour or more. This is the one
  required for certification and the one to run after building or upgrading.
- **Plugin mode** — Sonobuoy can run arbitrary containers as plugins and collect their output, which
  makes it a general framework for cluster-wide test execution rather than only a conformance runner.

**The results tarball is the underrated part.** It contains not only test outcomes but a dump of
cluster resources, node data and logs. For a cluster that is behaving strangely, running Sonobuoy and
reading the collected state is a reasonable diagnostic move even if the conformance result is not the
question.

**What a pass means, precisely:** the cluster implements the portable Kubernetes API behaviour the
tests cover. It says nothing about whether the cluster is fast, secure, correctly sized, or sensibly
configured. Presenting a conformance pass as a general quality statement is a misreading that this
tool invites and does not deserve.

**Maintenance status is worth checking.** Sonobuoy came from VMware/Heptio, and the surrounding
corporate changes make its ongoing maintenance worth verifying before depending on it. The tests
themselves are upstream Kubernetes and are not going anywhere; Sonobuoy is the runner, and if it
stalls, the underlying `e2e` test framework remains the thing being run.

---

[← Test](../README.md)
