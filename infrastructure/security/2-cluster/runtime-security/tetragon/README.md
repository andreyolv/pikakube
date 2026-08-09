[← Runtime security](../README.md)

# Tetragon

<https://github.com/cilium/tetragon>

Cilium's eBPF security observability and runtime enforcement tool. It can kill a process from inside
the kernel, without a round-trip to userspace.

---

## The problem it solves

Most runtime tools in this folder observe: the syscall happens, an event is emitted, something in
userspace reads it and decides what to do. That gap between event and reaction is where an attacker
operates, and it is measured in milliseconds at best and hours at worst — see
[`../README.md`](../README.md#5-detection-without-response-is-a-dashboard).

Tetragon's distinguishing capability is **in-kernel enforcement**. A `TracingPolicy` can carry a
`sigkill` action, applied by the eBPF program at the hook itself. The process is terminated
synchronously, before the syscall returns, with no userspace agent in the path. That closes the gap
entirely rather than shortening it.

The rest of what it offers:

| Capability | Detail |
|---|---|
| Process lifecycle tracking | full ancestry — which process spawned which, with the container and pod it belongs to |
| Arbitrary kernel hooks | `TracingPolicy` attaches to kprobes, tracepoints and LSM hooks, not just a fixed syscall list |
| In-kernel filtering | the filter runs in eBPF, so uninteresting events never reach userspace at all |
| File and network observability | opens, writes, connects, with the process that did them |
| Cilium integration | identity and network context from the CNI, when Cilium is the CNI |

The in-kernel filtering is the underrated part. Falco and Tracee push events to userspace and filter
there; Tetragon can discard them at the hook. On a high-syscall workload — which is what a data
platform is — that difference shows up directly as lower overhead and fewer dropped events.

The cost of that flexibility: a `TracingPolicy` is written against **kernel functions and
arguments**, not against a friendly rule language. Writing one means knowing which kprobe to attach
to and how to interpret its arguments. There is a library of them, and it is not the copy-paste
experience Falco's rules are.

## When to use it

- **Cilium is already the CNI.** This is the strongest argument. The eBPF infrastructure, the
  identity model and the operational familiarity are already there, and the network and runtime
  pictures join up.
- **You want enforcement without an LSM dependency.** [KubeArmor](../kubearmor/README.md) needs the
  node's kernel to have a usable LSM enabled. Tetragon's `sigkill` works wherever its eBPF programs
  load. On managed node pools where you do not control the host image, that is a real difference.
- **Process ancestry matters to the investigation.** "A shell was spawned" is much less useful than
  "nginx spawned bash, which spawned curl, which connected here". Tetragon's process tree is its
  strongest observability feature.
- **Event volume is a problem.** In-kernel filtering means you can attach broadly and still keep the
  output tractable.
- **You need a hook nothing else exposes.** Arbitrary kprobes cover cases a fixed syscall rule set
  does not.

## When not to use it

- **You want a large ready-made rule set.** [Falco](../falco/README.md) has the ecosystem: hundreds
  of maintained rules and an output layer that already integrates with everything. Tetragon's policy
  library is smaller and lower-level.
- **Nobody wants to write kernel-level policy.** A `TracingPolicy` referencing kprobe arguments is a
  different skill from a Falco rule. If nobody on the team can review one, nobody can fix one during
  an incident.
- **`sigkill` before understanding the workload.** In-kernel termination is the fastest possible
  enforcement and therefore the fastest possible way to kill a production process for a false
  positive. The application sees a signal, not an explanation. Observe first.
- **Cilium is not in play.** Tetragon runs standalone perfectly well, but a large part of the reason
  to prefer it over Falco is the integration you would not be getting.
- **You need the output routed somewhere.** Tetragon exports JSON events and Prometheus metrics; it
  has nothing equivalent to falcosidekick's fan-out. Getting events to Slack, a SIEM or a response
  engine is work you do yourself.
- **Another kernel agent is already deployed.** One DaemonSet hooking the kernel per cluster.

## Notes

The original `doc.md` contained only the repository link, which is at the top of this file. What
follows is the state of the deployment and how it compares.

### How it is deployed here

`helm/helmrelease.yaml`, chart `tetragon` 1.4.0 from the `cilium` HelmRepository into the `tetragon`
namespace, with **no values** — only the two documentation comments pointing at the chart's
`values.yaml` and the ArtifactHub page.

Defaults mean: the agent DaemonSet and the operator are installed, process execution tracking is on,
and **no `TracingPolicy` exists**. So Tetragon here observes process lifecycle events and enforces
nothing, which is the correct order and also means there is no policy in this repository to read as
an example.

There is no `ServiceMonitor` configured and nothing consumes the event export, so events go to the
agent's log and stop.

### Where it sits against the others

| | Tetragon | [Falco](../falco/README.md) | [KubeArmor](../kubearmor/README.md) | [Tracee](../tracee/README.md) |
|---|---|---|---|---|
| Mechanism | eBPF (kprobes, tracepoints, LSM) | eBPF or kernel module | LSM (AppArmor / SELinux / BPF-LSM) | eBPF |
| Enforces | yes — in-kernel `sigkill` | no | yes — LSM denies the action | no |
| When enforcement happens | at the hook, synchronously | n/a | before the action, the kernel refuses | n/a |
| Policy language | `TracingPolicy` — kernel-level | rules over syscalls, readable | per-workload allow-lists | signatures |
| Filtering | in-kernel | userspace | in-kernel | userspace |
| Rule ecosystem | small | large | per-workload library | moderate |

The distinction between Tetragon's and KubeArmor's enforcement is worth being precise about:
KubeArmor's LSM hooks **deny** the action, so it never happens; Tetragon's `sigkill` lets the syscall
proceed and kills the process. Both are prevention in practice, and only the first is prevention in
the strict sense.

### What it would take to adopt

1. Decide whether Cilium is the CNI on this platform — if not, most of the argument for Tetragon over
   Falco disappears.
2. Deploy in observation only, which is what the current values already do.
3. Enable the metrics `ServiceMonitor` and route the JSON event export somewhere, since neither is
   configured.
4. Write or adopt `TracingPolicy` resources, starting with observation and adding `sigkill` only for
   actions with no benign explanation.
5. Decide explicitly against [Falco](../falco/README.md), which is the agent actually built out in
   this repository with three companions and real configuration. Both installed is duplicate
   overhead and duplicate alerts.

---

[← Runtime security](../README.md)
