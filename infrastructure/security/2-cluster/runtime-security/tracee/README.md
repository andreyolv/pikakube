[← Runtime security](../README.md)

# Tracee

<https://github.com/aquasecurity/tracee>

Aqua Security's eBPF runtime detection tool. Deep event capture with behavioural signatures, and a
tracing tool good enough to use as a debugger.

---

## The problem it solves

Tracee is two things that happen to ship together, and understanding the split explains where it
fits.

**A tracing engine.** It captures a wide range of kernel events — syscalls, network activity, file
operations, and kernel-internal events other tools do not expose — with rich argument capture and
container context. Used on its own it is a general-purpose "what is this process actually doing"
tool, which is genuinely useful outside security: debugging a container that fails for no visible
reason, or working out which files a black-box image touches.

**A detection engine.** On top of that stream it runs **signatures**, each describing an attacker
technique mapped to MITRE ATT&CK: container escape attempts, dynamic code loading, anti-debugging,
LD_PRELOAD injection, kernel module loading, `/proc` manipulation.

The signature model is the difference from [Falco](../falco/README.md). A Falco rule is a filter
expression over a single event — powerful, readable, and stateless. A Tracee signature can be
written in Go or Rego and can carry **state across events**, which is what a multi-step technique
requires: "a process wrote a file, then made it executable, then executed it" is three events and one
detection.

Two capabilities that follow from the depth of capture:

- **Argument and file capture.** Tracee can capture the contents of a written file or a memory
  region, which matters for forensics — the alert can include what was dropped, not just that
  something was.
- **Detection of techniques that hide from syscalls.** Things like kernel module loading and some
  process-injection methods are visible because it hooks below the syscall layer.

The cost of that depth is volume and overhead. Capturing more events with more arguments is more
work per event, and the untuned output is very large.

## When to use it

- **You want ATT&CK-mapped detections out of the box.** Signatures are written as techniques, so the
  output answers "which attack step is this" rather than "which rule fired". That is the same framing
  [kubescape](../../posture/kubescape/README.md) brings to posture.
- **Multi-step techniques matter.** Stateful signatures catch sequences that a stateless rule engine
  structurally cannot.
- **You are already using Aqua tooling.** Trivy for images, Tracee for runtime — one vendor, one
  support relationship, findings that line up.
- **As a debugging and investigation tool.** This is an underrated use. Running Tracee against one
  workload to see exactly which files and syscalls it uses is the fastest way to understand a
  container you did not build — and it is the practical way to build an allow-list for
  [KubeArmor](../kubearmor/README.md).
- **You need forensic detail in the alert.** Argument and file capture put the evidence in the event.
- **For a one-off investigation.** It runs as a standalone binary against a host, not only as a
  DaemonSet. Deploying nothing permanently and running it during an incident is a legitimate mode.

## When not to use it

- **You want enforcement.** Tracee detects. It does not block, and there is no response engine in its
  ecosystem — no equivalent of [falco-talon](../falco/falco-talon/README.md). Prevention is
  [Tetragon](../tetragon/README.md) or [KubeArmor](../kubearmor/README.md).
- **You need a mature output and routing layer.** Falco's falcosidekick fans out to dozens of
  destinations with no work. Tracee emits events and getting them to a SIEM, Slack or a dashboard is
  yours to build.
- **Overhead is tight.** Deeper capture costs more. On high-syscall workloads — Spark, Airflow,
  anything process-heavy — the default event set is expensive, and narrowing what is captured is the
  first tuning step rather than the last.
- **You want the widest community rule set.** Falco's is larger and more actively contributed to;
  writing a Tracee signature means writing Go or Rego, not editing YAML.
- **Another kernel agent is deployed.** One DaemonSet hooking the kernel per cluster.
- **The kernel is old.** It requires a recent kernel with BTF for CO-RE, or a matching prebuilt
  object. This is the same constraint that produced the driver problem recorded in the
  [Falco notes](../falco/README.md).

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of the deployment and how it compares.

### How it is deployed here

`helm/helmrelease.yaml`, chart `tracee` 0.20.0 from the `aqua` HelmRepository into the `tracee`
namespace, with **no values** — only the two documentation comments pointing at the chart's
`values.yaml` and the ArtifactHub page.

One detail worth noticing: the ArtifactHub link in the comment is
`packages/helm/trivy-operator/tracee`. The chart is published under Aqua's repository alongside
Trivy Operator, which is a reminder that Tracee is one component of a larger Aqua stack rather than a
standalone product — and part of the argument for it is adopting more of that stack.

With default values this installs the agent DaemonSet with the default signature set and default
event capture. No signatures are customised, no events are narrowed, and nothing consumes the output
— there is no `ServiceMonitor` and no sink configured. Events go to the agent's log.

That is the same shape as [Tetragon](../tetragon/README.md) next door: installed, running, and not
integrated with anything.

### Where it sits against the others

| | Tracee | [Falco](../falco/README.md) | [Tetragon](../tetragon/README.md) | [KubeArmor](../kubearmor/README.md) |
|---|---|---|---|---|
| Owner | Aqua Security | CNCF, graduated | Cilium / Isovalent | Accuknox |
| Mechanism | eBPF | eBPF or kernel module | eBPF | LSM |
| Detection model | signatures, **stateful**, ATT&CK-mapped | rules, stateless, per-event | `TracingPolicy` over kernel hooks | per-workload allow-lists |
| Enforces | no | no | yes (`sigkill`) | yes (LSM denies) |
| Written in | Go or Rego | a filter expression language | kernel-level YAML | Kubernetes YAML |
| Output ecosystem | thin | the largest here | metrics and JSON export | relay |
| Also useful as | a debugger | — | process ancestry viewer | — |

Tracee and Falco are the closest pair, and the honest summary is: Falco wins on ecosystem and rule
accessibility, Tracee wins on depth of capture and stateful signatures. For a platform that needs
detections routed to humans and acted on, ecosystem is usually the deciding factor — which is why
Falco is the one built out in this repository.

### The use that does not require choosing

Even if Falco stays the deployed agent, Tracee is worth keeping as an **investigation tool**. Running
it against a single workload to enumerate exactly which syscalls, files and network endpoints that
workload uses is the practical way to produce the allow-list a KubeArmor policy needs — and it is a
job Falco's rule-based model does not do.

That is a better justification for this folder than "a fourth runtime agent".

---

[← Runtime security](../README.md)
