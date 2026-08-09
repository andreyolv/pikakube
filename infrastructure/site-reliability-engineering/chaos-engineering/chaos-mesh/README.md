[← Chaos engineering](../README.md)

# Chaos Mesh

<https://github.com/chaos-mesh/chaos-mesh>
<https://chaos-mesh.org/>

---

## The problem it solves

The broadest **fault vocabulary** of anything in this folder. Most chaos tools kill pods; Chaos
Mesh injects failures at layers that are otherwise almost impossible to reproduce deliberately:

| Fault | What it exposes |
|---|---|
| `PodChaos` | replicas, probes, PDBs |
| `NetworkChaos` | latency, loss, duplication, corruption, **partition** |
| `IOChaos` | filesystem latency and errors — the failure nobody has ever seen |
| `TimeChaos` | clock skew, which breaks certificates, tokens and leader election |
| `StressChaos` | CPU and memory pressure |
| `KernelChaos` | kernel-level faults |
| `DNSChaos` | resolution failures and wrong answers |

`TimeChaos` and `DNSChaos` deserve attention. Clock skew and DNS failure cause outages that are
notoriously hard to diagnose, and almost nobody tests for them — which is precisely why they
are worth injecting on purpose.

## When to use it

- faults **beyond pod termination** are the point
- network partition and IO failure behaviour need testing, which no simple tool covers
- CRD-driven experiments fitting a GitOps workflow

## When not to use it

- a random pod killer is all you want — [chaoskube](../chaoskube/README.md)
- you want a catalogue, workflows and tracked results — [LitmusChaos](../litmus/README.md) is more of a platform
- faults are needed **outside** Kubernetes too — [ChaosBlade](../chaosblade/README.md)

## A caution

`KernelChaos` and `IOChaos` operate at a level where mistakes affect the node, not just the
pod. Blast radius here is not a formality — start with `PodChaos` and `NetworkChaos`, and reach
the lower layers only on a cluster you are prepared to lose.

---

[← Chaos engineering](../README.md)
