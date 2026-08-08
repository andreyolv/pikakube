[← eBPF platforms](../README.md)

# DeepFlow

<https://github.com/deepflowio/deepflow>
<https://github.com/deepflowio/deepflow-charts>

---

## The problem it solves

Most eBPF platforms reconstruct an application-level picture. DeepFlow goes further **down**,
correlating application behaviour with the network path underneath it — including the
infrastructure layers that usually stay invisible.

That makes it strong on a specific and genuinely hard question: **is this latency the
application, the pod network, the node, or the underlay?** Normally answering that means
correlating three tools by timestamp.

## When to use it

- latency problems that cross the application and network boundary and nobody can attribute them
- complex networking — service mesh, overlays, multi-cluster — where the path itself is a suspect
- you want full-stack correlation from application call down to network flow

## When not to use it

- the question is "which services talk to each other and how are they doing" — [Coroot](../coroot/) answers that with less
- small or simple environments, where the depth is unused complexity
- you already have [Cilium](../../../../network/cni/cilium/) with Hubble, plus an application-level tool

## Related

Overlaps with [`observability/network/`](../../../network/README.md), which covers flow-level
visibility as its own capability. DeepFlow is filed here because it presents itself as a full
platform rather than a network add-on.

---

[← eBPF platforms](../README.md)
