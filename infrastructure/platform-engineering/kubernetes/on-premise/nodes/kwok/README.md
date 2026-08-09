[← Nodes](../README.md)

# kwok

<https://github.com/kubernetes-sigs/kwok>

---

## The problem it solves

Kubernetes WithOut Kubelet. kwok creates **fake nodes** in a real cluster — nodes with names,
capacity, labels, taints and conditions you choose — and simulates pod lifecycle on them. Pods
scheduled there transition to `Running` and report status, and nothing is executed.

The consequence is that a cluster with thousands of nodes and tens of thousands of pods can be
simulated on a laptop. Scheduler behaviour, autoscaler behaviour, controller performance and
scale-related bugs become testable without hardware.

## When to use it

- Testing scheduling and autoscaling behaviour at a scale you cannot build
- Developing a controller and needing to know how it behaves against 5,000 nodes
- Reproducing scale-dependent problems locally
- Simulating node conditions and failures deterministically — a node that goes `NotReady` on demand

## When not to use it

- Anything that must actually run; no containers are started
- Testing real resource pressure, throttling or eviction under genuine load
- Networking or storage behaviour, which is not simulated
- As a development cluster; it looks like a cluster and runs nothing

## Notes

Recorded as a link only.

**This is the direct answer to a limitation recorded elsewhere in this repository.**
[kind cannot set node names or node capacity](../../../local/distributions/README.md) — two upstream
issues are filed against it — which rules out local testing of anything that depends on node shape.
kwok sets exactly those properties, which is the whole point of it.

That makes it the missing piece for experiments this repository would otherwise be unable to run:

- the [bin-packing scheduler configuration](../../../managed/scheduler/custom-scheduler/README.md),
  whose behaviour depends entirely on node capacity
- [cluster autoscaler](../../../managed/autoscaler/cluster-auto-scaler/README.md) priority expander
  rules, which select between node groups
- [descheduler](../../../managed/scheduler/descheduler/README.md) policies, which depend on
  utilisation across nodes

None of those can be exercised on kind. All of them can be exercised on kwok.

**Two modes worth distinguishing:**

- **`kwok`** — the controller, added to an existing cluster, which manages fake nodes alongside real
  ones. Useful for mixing real workloads with simulated capacity.
- **`kwokctl`** — creates an entire fake cluster, control plane included, in seconds. Useful for a
  clean simulation environment.

**The limits, stated so nobody is surprised:** pods do not run. There is no container, no process, no
CPU consumed, no memory used, no network traffic. Anything downstream of a container actually
existing — application behaviour, real resource pressure, eviction driven by genuine memory use — is
outside what kwok can tell you. It simulates the **control plane's view** of a large cluster, and
that view is exactly what scheduling and autoscaling operate on.

`kubernetes-sigs`, from the scheduling and testing side of the project — the same community as
[kube-scheduler-simulator](../../../managed/scheduler/kube-scheduler-simulator/README.md), which
answers the complementary question of *why* a single pod was placed where it was.

---

[← Nodes](../README.md)
