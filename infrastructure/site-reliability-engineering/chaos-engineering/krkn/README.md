[← Chaos engineering](../README.md)

# krkn

<https://github.com/krkn-chaos/krkn>

---

## What it is

Chaos testing oriented to **cluster and telco workloads**, originating from Red Hat's
OpenShift performance and scale work. CNF-focused, scenario-driven, and run as a set of
scripted scenarios rather than as CRDs.

Its emphasis is different from the other tools here: less "inject a fault into an application",
more **"stress the cluster itself and measure whether it stays within bounds"** — node
failures, API server pressure, etcd disruption, resource exhaustion at cluster scale.

## When to use it

- validating a **cluster**, not a workload — how the control plane behaves under disruption
- CNF and telco environments, where it was designed and is used
- scenario-driven testing fits better than a CRD per experiment

## When not to use it

- application-level chaos in a normal Kubernetes platform — [Chaos Mesh](../chaos-mesh/README.md) or [LitmusChaos](../litmus/README.md) are more idiomatic
- you want CRDs, a UI and tracked results
- OpenShift is not the context, which is where most of its material assumes you are

## Why it is mapped here

Because it tests something the others largely do not: **the control plane**. Most chaos tooling
assumes Kubernetes keeps working and disrupts what runs on it. krkn is willing to disrupt
Kubernetes.

That is worth knowing about for on-premise clusters, where the control plane is yours to lose —
see [`platform-engineering/kubernetes/on-premise/`](../../../platform-engineering/kubernetes/on-premise/).

---

[← Chaos engineering](../README.md)
