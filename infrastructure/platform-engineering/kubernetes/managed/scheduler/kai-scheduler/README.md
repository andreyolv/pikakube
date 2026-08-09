[← Scheduler](../README.md)

# KAI Scheduler

<https://github.com/kai-scheduler/KAI-Scheduler>

---

## The problem it solves

A scheduler built specifically for **AI and GPU workloads**, open-sourced from NVIDIA's Run:ai
platform. The problems it targets are the ones that appear once a cluster's expensive resource is
GPUs rather than CPU:

- **GPU sharing** — several workloads on one physical GPU, rather than the one-pod-one-GPU allocation
  Kubernetes gives you by default
- **Gang scheduling** for distributed training
- **Hierarchical queues** with fair share and reclaim between research teams
- **Preemption** aware of which jobs are checkpointable and which are not

The distinguishing item is the first. Kubernetes treats a GPU as an indivisible integer resource, so a
notebook using 5% of an A100 holds all of it. On a cluster where GPUs are the entire budget, that is
the dominant inefficiency.

## When to use it

- GPU clusters where utilisation, not availability, is the problem
- Many researchers sharing a small number of expensive accelerators
- Interactive notebooks alongside training jobs, competing for the same hardware
- NVIDIA GPUs, which is what it is built around

## When not to use it

- CPU-only clusters; nothing here applies
- General batch — [Volcano](../volcano/README.md) and [YuniKorn](../yunikorn/README.md) are more
  established and more general
- Where the GPU operator and device plugin story is not already working
- As a general-purpose replacement scheduler

## Notes

Recorded as a link only, with no chart and no manifests.

**Why it is worth keeping in the list** despite being unevaluated: the GPU sharing problem is real
and has no good default answer. Kubernetes' device plugin model allocates whole devices. The
alternatives — MIG partitioning, time-slicing through the NVIDIA device plugin — are configured at the
node level and are coarse. A scheduler that understands fractional GPU allocation is a genuinely
different capability, not a repackaging of one.

**The provenance is the strongest signal here.** It is the scheduler from Run:ai, which NVIDIA
acquired and then open-sourced. That means it has run real multi-tenant GPU clusters in anger, which
very little in this space has. It also means the project is young **as an open-source project** even
though the code is not, and community conventions, documentation and release practices are still
settling.

**The neighbouring pieces**, if this is ever pursued: GPU scheduling only works when the device
plugin, drivers and node labelling are correct first —
[`on-premise/nodes/node-feature-discovery/`](../../../on-premise/nodes/node-feature-discovery/README.md)
is the piece that labels nodes by hardware capability, and it is a prerequisite for anything
GPU-aware making sensible placement decisions.

---

[← Scheduler](../README.md)
