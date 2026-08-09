[← Scheduler](../README.md)

# kube-scheduler-simulator

<https://github.com/kubernetes-sigs/kube-scheduler-simulator>

---

## The problem it solves

Scheduling decisions are opaque. A pod lands on a node and there is no ordinary way to see which
plugins filtered which nodes out, what each surviving node scored, and why the winner won. When
placement is wrong, the debugging tools are events and guesswork.

The simulator runs the **real scheduler** against a fake cluster and shows all of it: create nodes and
pods in a web UI, watch each pod be scheduled, and inspect the per-plugin filter results and scores
for every node. Scheduler configuration can be changed and the same scenario replayed.

## When to use it

- Before changing a `KubeSchedulerConfiguration` in a real cluster — test the policy first
- Understanding why a pod went where it did, in a setting you can control
- Developing or evaluating a scheduler plugin
- Teaching the scheduling framework, which is otherwise abstract

## When not to use it

- As a production component; it is a development and analysis tool
- To reproduce real capacity behaviour — the cluster is simulated, workloads do not run
- For scale testing — [kwok](../../../on-premise/nodes/kwok/README.md) fakes thousands of real-looking
  nodes in a real cluster, which is the tool for that
- Where the problem is resource requests rather than scheduling policy

## Notes

Recorded as a link only, with no chart and no manifests.

**Why it belongs in this folder despite being a toy cluster.** Everything else here changes how
scheduling works; this is the only thing that lets you *see* it. The
[bin-packing configuration](../custom-scheduler/README.md) built in this repository — `MostAllocated`
with every other scoring plugin disabled — is exactly the kind of change whose consequences are hard
to predict. Disabling all other score plugins removes image locality, pod spreading and node affinity
scoring; the simulator would show precisely what that costs, on a scenario of your choosing, before
it reaches a cluster.

**The per-plugin score view is the feature.** Scheduling looks arbitrary from outside because the
result is a single number aggregated from a dozen voters. Seeing the individual votes turns "why did
it pick that node" from a guess into a reading.

**Complementary, not competing, with [kwok](../../../on-premise/nodes/kwok/README.md):**

| | simulator | kwok |
|---|---|---|
| Cluster | simulated, in the tool | a real API server with fake nodes |
| Shows | per-plugin filter and score detail | aggregate behaviour at scale |
| Answers | *why* was this pod placed here | what happens with 5,000 nodes |

Use the simulator to understand a decision, kwok to observe behaviour at a scale you cannot afford to
build.

`kubernetes-sigs`, maintained alongside the scheduling SIG's other work.

---

[← Scheduler](../README.md)
