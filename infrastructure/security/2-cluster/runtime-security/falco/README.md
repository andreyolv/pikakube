[← Runtime security](../README.md)

# Falco

<https://github.com/falcosecurity/falco>
<https://github.com/falcosecurity/charts>
<https://github.com/falcosecurity/plugins>
<https://github.com/falcosecurity/falcosidekick>
<https://github.com/falcosecurity/falcosidekick-ui>
<https://github.com/falcosecurity/falco-talon>

The reference runtime security tool for Kubernetes. eBPF syscall monitoring, a rules language, and
the only ecosystem in this folder large enough to turn detections into action. CNCF graduated.

Companions in this folder: [`event-generator/`](event-generator/README.md) — prove the rules fire ·
[`falco-exporter/`](falco-exporter/README.md) — Prometheus metrics ·
[`falco-talon/`](falco-talon/README.md) — automated response

A second way to deploy the same thing: [`../falco-operator/`](../falco-operator/README.md) — rules,
plugins and configuration as CRDs instead of Helm values. **The two are alternatives, not layers**,
and as checked in they collide — see that page.

---

## The problem it solves

Everything else in `2-cluster/` inspects intent. Admission control sees the Pod spec, posture tools
see configuration, image scanners see the image. A Pod can satisfy all of them and still be running a
reverse shell, because the exploit arrives through the application at runtime, not through the
manifest.

Falco watches what processes actually do. It attaches to the kernel — modern eBPF by default — and
evaluates every syscall against a rule set:

```
a shell was spawned inside a container
a process wrote to /etc/shadow
a container tried to read a Kubernetes service account token
an outbound connection went to a non-allowed port
a package manager ran in a running container
```

Each of those is a rule over syscalls plus container and Kubernetes metadata, and the rules are
readable YAML: a `condition` in Falco's filter language, an `output` string, and a `priority`. That
readability is why the rule set is the largest of any tool here, and why tuning one is a task a
platform engineer can do rather than a kernel engineer.

Two things separate Falco from the rest of the folder:

**Plugins.** The engine is not limited to syscalls. Plugins feed it other event streams — Kubernetes
audit logs, AWS CloudTrail, Okta, GitHub — evaluated by the same rules engine. That makes it a
detection engine for the platform, not only for the nodes.

**An output ecosystem.** Falco emits events and does nothing with them. `falcosidekick` fans them out
to dozens of destinations (Slack, Loki, Elasticsearch, PagerDuty, webhooks); `falco-exporter` turns
them into Prometheus metrics; `falco-talon` acts on them. Nothing else in this folder has that.

What Falco does **not** do: block. It observes and reports. Enforcement is
[Tetragon](../tetragon/README.md) or [KubeArmor](../kubearmor/README.md), or Falco plus
[falco-talon](falco-talon/README.md) reacting after the fact. That distinction is deliberate on the
project's part and it is the honest boundary of what it offers.

## When to use it

- **You want the widest rule coverage available.** The default rule set encodes years of accumulated
  detection knowledge, and it is maintained by a graduated CNCF project.
- **You need to route detections somewhere.** falcosidekick is the reason to pick Falco over a
  technically similar tool: the integration work is already done.
- **You want detections from more than syscalls.** The plugin framework brings cloud audit logs into
  the same rules engine and the same alert pipeline.
- **Detection is the goal, not enforcement.** Observing first is the correct order anyway — see
  [`../README.md`](../README.md#3-detection-vs-enforcement).
- **You want to prove the control works.** [`event-generator/`](event-generator/README.md) generates
  the suspicious activity on demand. Very few security tools ship a way to demonstrate they are
  actually working.
- **Compliance requires runtime monitoring.** PCI DSS, SOC 2 and similar frameworks ask for file
  integrity monitoring and detection of unauthorised activity; Falco is the standard answer on
  Kubernetes.

## When not to use it

- **You want the action blocked, not reported.** Falco tells you after the syscall happened. If the
  requirement is prevention, use an LSM-based tool.
- **Nobody has time to tune it.** This is the real reason Falco deployments fail. The default rules
  fire constantly on a normal cluster — `kubectl exec` produces "terminal shell in container" every
  single time, package managers in init containers look identical to tampering, and data workloads
  spawn processes by design. Tuning is a quarter of work, not an afternoon, and
  [`../README.md`](../README.md#4-the-alert-volume-problem) describes the loop.
- **Node overhead is tight.** A DaemonSet processing every syscall on every node is not free,
  especially on high-syscall workloads — which is exactly what Spark and Airflow are. Watch the
  event drop counters.
- **The kernel cannot support it.** See the Notes: the kernel-module driver has real version limits,
  and eBPF needs a recent enough kernel with the right options built in.
- **Another agent is already deployed.** Two DaemonSets hooking the kernel means duplicate alerts and
  double the overhead.

## Notes

Every original note from `doc.md`, translated and explained.

### Checking the driver loaded

```bash
kubectl logs daemonset/falco -n falco -c falco-driver-loader
```

Falco's DaemonSet has an init container whose only job is to obtain the kernel driver — build it,
download a prebuilt one, or set up eBPF. When Falco is running but seeing nothing, this container's
log is the first place to look, and it is where the failure in the note below shows up.

With `driver.kind: modern-bpf` — which is what this repo sets — no driver is loaded at all: modern
eBPF is compiled into the Falco binary using CO-RE and attaches directly, so there is nothing to
build and nothing to match against the running kernel. The driver-loader container becomes a no-op,
which is exactly the point of choosing it.

### The Falco UI credentials

> login and password in the UI:
> admin
> admin

The falcosidekick web UI's default credentials, unchanged. That is fine for a local cluster and must
not survive contact with anything else — the UI shows every security detection in the cluster, which
is a map of where the weaknesses are.

The UI is enabled in `helm/helmrelease.yaml` (`falcosidekick.webui.enabled: true`) with one replica.
The chart takes credentials through its values; leaving them at the default is a decision, not an
oversight, and it should be recorded as one.

### The kernel module problem

> DONE
> - With the kernel module, versions above 5.x.x do not work. It went badly trying to test with Kind.
>   Try with the eBPF module.
>
> <https://github.com/falcosecurity/falco/issues/2540>
> <https://github.com/falcosecurity/plugins/issues/123>

Marked DONE, so this is a resolved finding rather than an open problem — and it is the most
practically useful note in the folder.

What happened: the legacy kernel-module driver failed on kernels above 5.x, and testing inside
**Kind** made it worse. Kind runs Kubernetes nodes as containers on the host, so the "node" shares
the host's kernel. A tool that needs to load a kernel module has to load it into the *host* kernel
from inside a container, which requires privileges the host may not grant and produces confusing
errors when it does not.

The resolution was to switch to eBPF, and that is visible in the deployed configuration:
`driver.kind: modern-bpf`. Modern eBPF needs no compilation, no kernel headers, and no module
loading — it uses CO-RE to attach to a range of kernels with one binary. It requires a reasonably
recent kernel (roughly 5.8+) with BTF available, which is the trade.

The two linked issues are upstream reports kept as the evidence trail: one against Falco itself, one
against the plugins repository. Both are worth re-checking against the deployed chart version
(4.21.3) before assuming any of it still applies — this ecosystem moved quickly in that period.

The general lesson generalises past Falco: **kernel modules are the legacy path**, and choosing them
is choosing a class of problem that appears on the next kernel upgrade rather than today.

### How it is deployed here

`helm/helmrelease.yaml`, chart `falco` 4.21.3:

| Setting | Meaning |
|---|---|
| `driver.kind: modern-bpf` | CO-RE eBPF; no module, no compilation — the resolution of the note above |
| `falcosidekick.enabled: true` | the output router is deployed |
| `falcosidekick.webui.enabled: true` | plus the web UI, one replica |
| `falco.grpc.enabled` and `falco.grpc_output.enabled` | the gRPC API is on |

The gRPC settings are not cosmetic: they are what
[`falco-exporter/`](falco-exporter/README.md) and [`falco-talon/`](falco-talon/README.md) consume.
Without them, both companions have nothing to subscribe to.

No output target is configured on falcosidekick — no Slack, no Loki, no webhook — so detections reach
the web UI and stop there. That is the gap between "we can look this up" and "we find out", and it is
the same gap noted in [Policy Reporter](../../policies/kyverno/policy-reporter/README.md) on the
admission side.

Nothing in this folder customises the rule set. The default rules on an untuned cluster are noisy by
design, and the work described in [`../README.md`](../README.md#tuning-is-the-job) has not started
here.

There is also a second, incompatible deployment of Falco in the repository:
[`../falco-operator/`](../falco-operator/README.md) declares a `HelmRelease` with the **same name in
the same namespace**, installing the operator chart instead of this one. Neither is wired into
`clusters/dev/`, so nothing is broken today — but the choice between the chart here and the operator
there has been deferred rather than made.

---

[← Runtime security](../README.md)
