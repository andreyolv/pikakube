[← Runtime security](../README.md)

# KubeCop

<https://github.com/armosec/kubecop>

ARMO's behavioural runtime detection agent. Instead of matching hand-written rules, it learns what
each workload normally does and alerts on deviation.

---

## The problem it solves

Every other tool in this folder asks you to describe suspicious behaviour in advance —
[Falco](../falco/README.md) rules, [Tracee](../tracee/README.md) signatures,
[KubeArmor](../kubearmor/README.md) allow-lists, [Tetragon](../tetragon/README.md) tracing policies.
That has two failure modes and both are real:

| Failure | Consequence |
|---|---|
| The rule is too broad | it fires on normal behaviour, constantly, and the alert channel gets muted |
| The rule is too narrow | it misses the technique that was not anticipated |

The rules are also generic by necessity: they encode what is unusual on *a* cluster, not on *your*
cluster. That mismatch is the source of the alert volume described in
[`../README.md`](../README.md#4-the-alert-volume-problem).

KubeCop inverts it. During a **learning period** it uses eBPF to observe each workload — which
binaries execute, which files are opened, which network endpoints are contacted, which capabilities
are used — and builds an application profile from what it sees. After that, anything outside the
profile is an anomaly.

The consequence that makes it attractive: the baseline is *specific to your workload*. A container
that runs `python` and reads three config files has a tiny profile, and anything else it does is
genuinely notable. No rule author had to anticipate it.

Layered on top are conventional detections for the techniques that are unambiguous regardless of
baseline — a shell spawned in a container, a service account token read, `/proc` manipulation, an
attempted escape.

## When to use it

- **Nobody has time to write and tune rules.** This is the honest reason to reach for it. Rule
  maintenance is the recurring cost of every other tool here; a learned baseline moves that cost into
  a learning window instead.
- **Workloads are narrow and stable.** A microservice that does one thing produces a small, accurate
  profile. This is where behavioural detection is at its best.
- **You already use ARMO tooling.** It shares lineage with
  [Kubescape](../../posture/kubescape/README.md), which is deployed in this repo — same vendor,
  overlapping concepts.
- **To find what a rule set would miss.** Even alongside another agent, a baseline catches deviations
  nobody wrote a rule for.
- **To produce an allow-list.** The learned profile is very close to what a
  [KubeArmor](../kubearmor/README.md) policy needs. Using it to *generate* an allow-list, then
  enforcing that with an LSM, is a more useful pipeline than either tool alone.

## When not to use it

- **The workload was not verified before learning.** The critical limitation. If a workload is
  already compromised when the learning window runs, **the compromise becomes the baseline** and the
  attacker's behaviour is normal forever. Baseline only from a known-good state, ideally a freshly
  deployed one.
- **Behaviour is broad or genuinely dynamic.** Data platforms are the hard case. Airflow executes
  whatever a DAG author wrote, Spark spawns JVMs and writes to arbitrary scratch paths, and every new
  pipeline is legitimately new behaviour. The profile is either enormous and useless or constantly
  out of date and noisy.
- **Deployments are frequent.** Every new image version can be new behaviour, so the profile needs
  relearning. That is fine when it is automatic and a problem when a release produces a wall of
  anomalies.
- **You need to explain the alert.** "This deviates from the learned profile" is a much harder thing
  to act on than "this process wrote to `/etc/shadow`". Anomaly alerts require more investigation per
  alert, which partly cancels the volume advantage.
- **You need enforcement.** KubeCop detects. It does not block.
- **Project maturity matters.** This is the least established tool in the folder — check the
  repository's recent activity and its relationship to ARMO's current product line before depending
  on it. Vendor tools in this space get absorbed into larger platforms.
- **Another kernel agent is deployed.** One eBPF DaemonSet per cluster.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of the deployment and how it compares.

### How it is deployed here

`helm/helmrelease.yaml`, chart `kubecop` 0.0.40 into the `kubecop` namespace:

| Setting | Value | Meaning |
|---|---|---|
| `kubecop.alertmanager.enabled` | `false` | alerts are not sent to Alertmanager |
| `kubecop.alertmanager.endpoints` | `localhost:9093` | a placeholder, inactive while the above is false |
| `kubecop.csv.enabled` | `true` | findings written to a CSV file |
| `kubecop.prometheusExporter.enabled` | `true` | metrics exposed for Prometheus |

This is the only tool in the folder with an explicit alerting integration configured at all, even
though it is turned off — the Alertmanager endpoint is a placeholder pointing at localhost. Enabling
it and pointing it at the cluster's real Alertmanager would make this the first runtime security
component here with an actual path to a human. Everything else logs and stops.

The CSV output is a curiosity: findings written to a file inside the pod. Useful for a manual look at
a demo, not a durable sink — the file goes away with the pod.

The chart version `0.0.40` is the thing to weigh most heavily. A `0.0.x` chart for a component that
runs eBPF programs on every node is early software, and the deployment here sets nothing about the
learning window, which is the parameter that decides whether the tool works at all.

### The question this folder raises

Five runtime agents are present in [`../`](../README.md) and only [Falco](../falco/README.md) is
built out. KubeCop is the most different of the five — it is the only one that does not require
writing rules — so it is worth keeping as a documented alternative even though it will not be the
deployed agent.

Its most defensible use on a platform like this one is not as a detector at all. It is as a
**profile generator**: run it against a workload from a known-good state, take the learned profile,
and turn it into a [KubeArmor](../kubearmor/README.md) allow-list that the kernel then enforces. That
converts the hardest part of allow-list enforcement — knowing what to allow — into an observation
problem, and it is the one thing in this folder that no other tool does.

---

[← Runtime security](../README.md)
