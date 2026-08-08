[← Troubleshooting](../README.md)

# Inspektor Gadget

<https://github.com/inspektor-gadget/inspektor-gadget>

---

## The problem it solves

Some problems are invisible from `kubectl`. A pod is running and healthy, and something is
still wrong: it is opening files it should not, resolving a hostname that fails intermittently,
making syscalls that get denied, or generating traffic nobody can account for.

Inspektor Gadget is a collection of **eBPF gadgets** that observe that layer live, per pod:
syscalls, file access, network connections, DNS queries, TCP retransmits, signals sent to
processes.

Crucially, it maps kernel-level activity back to **Kubernetes identity** — pod, namespace,
container — instead of leaving you with a PID.

## When to use it

- the problem is below the application and no log explains it
- intermittent DNS or connection failures that nothing reports
- understanding what a workload actually does — which files, which hosts, which syscalls
- investigating an image whose behaviour is not documented

## When not to use it

- ordinary application debugging — logs, events and a scan are faster
- as a continuous signal. It is an investigation tool, not a monitoring pipeline; for standing network visibility see [`observability/network/`](../../network/README.md)

## Related

Overlaps with [`security/2-cluster/runtime-security/`](../../../security/2-cluster/runtime-security/) —
Falco, Tetragon and Tracee observe the same layer. The difference is intent: those detect and
alert on policy violations continuously, this one is used to answer a question now.

---

[← Troubleshooting](../README.md)
