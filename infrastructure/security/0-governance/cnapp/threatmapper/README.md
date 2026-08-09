[← CNAPP](../README.md)

# ThreatMapper

<https://github.com/deepfence/ThreatMapper>

---

## The problem it solves

Scanners produce more findings than anyone can act on, ranked by CVSS — a score that knows
nothing about your environment. A critical CVE in a library that is never loaded, in a pod with
no network exposure, outranks a medium in an internet-facing service. Sorting by severity is
sorting by the wrong key.

ThreatMapper, from Deepfence, is built around fixing that ranking. It scans the usual things —
container images, hosts, registries, and Kubernetes — for vulnerabilities, secrets and
malware, and then places every finding on a **topology graph** of the running environment:
which workloads exist, how they connect, what is exposed to the internet, and what an attacker
could reach from where.

The output is an **attack path** rather than a list. "This internet-facing pod has an
exploitable vulnerability, and from it these three internal services are reachable" is
actionable in a way that a CVSS-sorted table is not.

| Capability | Note |
|---|---|
| Vulnerability scanning | images, hosts, registries |
| Secret scanning | credentials left in images and filesystems |
| Malware scanning | uses YARA rules |
| **Runtime topology** | the live map of workloads and connections — the differentiating feature |
| **Attack-path analysis** | exploitability and reachability, not just severity |
| Compliance | posture checks against common benchmarks |

## When to use it

- **prioritisation is the problem** — you have findings and no way to decide which matter, which
  is the normal state after any scanner is turned on
- exposure and reachability are the questions: what is internet-facing, and what can be reached
  from it
- a **mixed estate** — cloud VMs, Kubernetes and bare metal — where the topology spans more than
  one platform
- you want an open-source option in the attack-path space, which is otherwise almost entirely
  commercial
- alongside an enforcement tool rather than instead of one; it tells you where to act

## When not to use it

- **as an enforcement point.** ThreatMapper observes and prioritises; it is not an admission
  controller and it does not block deployments. If the gap is "nothing stops bad workloads
  running", that is `3-container/admission/` or `2-cluster/policies/`, not this
- a small estate. The graph pays off when the topology is too large to reason about
  unaided — see [`../README.md`](../README.md#8-how-this-applies-to-pikakube)
- when a scanner is what is actually wanted. Trivy or Grype in the pipeline is faster, simpler
  and better at the scanning part; ThreatMapper's value is what it does with the results
- **alongside another CNAPP**. Running it with [StackRox](../stackrox/README.md) duplicates
  scanning and produces two answers to the same question
- when there is no capacity to act on prioritised findings. Better ranking of a list nobody
  reads is still a list nobody reads

## Notes

Original reference recorded for this tool:

> <https://github.com/deepfence/ThreatMapper>

Two things worth recording from the staged configuration in this repository, because both would
block a deployment.

**The staged `HelmRelease` is incomplete.** It has no `metadata.name`, no `metadata.namespace`
and no chart version — only the chart name `deepfence-console` and the `deepfence`
`HelmRepository` pointing at `https://deepfence-helm-charts.s3.amazonaws.com/threatmapper`.
As written it would not reconcile. It is a placeholder, and it is more clearly a placeholder
than the other charts staged nearby.

**The console is only half of it.** `deepfence-console` is the central UI, database and scanning
backend. Getting any data requires the **agent/sensor** chart deployed onto the clusters and
hosts being observed — and the runtime topology, which is the whole reason to choose this tool,
comes entirely from those agents. A console with no sensors shows an empty map.

**On the project's position generally.** Deepfence's open-source offering is one of the few
places attack-path analysis is available without a commercial contract, which is why it is
recorded here. It is also a smaller project than StackRox with a smaller community, and the
version referenced in the staged configuration comments (`release-2.2`) is worth checking
against current releases before any deployment — the chart and the product version have moved.

---

[← CNAPP](../README.md)
