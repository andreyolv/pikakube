[← Network troubleshooting](../README.md)

# Goldpinger

<https://github.com/bloomberg/goldpinger>

The debugging **method** — which layer to check in which order:
[../README.md](../README.md)

---

## The problem it solves

A completely broken CNI is easy: nothing works, and everyone knows within a minute. The
expensive failure is the **partial** one — the cluster is mostly fine, and:

- one node cannot reach one other node, and only pods that land on both notice
- a subset of pods times out and the rest are healthy
- traffic works in one direction and not the other

The symptom surfaces in an application, so the application team investigates the application.
Hours later somebody notices the failures correlate with a node.

Goldpinger runs as a **DaemonSet** where every instance pings every other instance. N
instances produce N×N results, rendered as a live connectivity graph — a web UI plus
Prometheus metrics.

The value is not "the network is flaky". It is that a failure shows up as a specific **edge**
between two specific nodes, which turns an unbounded investigation into a bounded one.

## When to use it

- clusters large enough that a single node pair can break independently of everything else
- immediately after a CNI change, an MTU adjustment, a kernel upgrade or a security-group edit
- when intermittent timeouts are being blamed on applications and nobody can prove otherwise
- as a **standing** check wired into alerting, not a tool someone remembers during an incident
- multi-zone or multi-subnet clusters, where the failure domain follows the topology

## When not to use it

- **small or single-node clusters** — there is no matrix, and one instance pinging itself proves nothing
- **large clusters without tuning.** N×N grows quadratically: pings, metric series and UI edges all scale with the square of the node count. The ping interval and timeouts have to be tuned deliberately, or Goldpinger becomes its own noise source
- **as a general network test.** It measures pod-to-pod reachability between *its own* pods. It does not test DNS resolution, Service routing through kube-proxy, NetworkPolicy semantics, ingress, or egress to anything outside the cluster
- **as proof the network is healthy.** A fully green graph means Goldpinger pods can reach each other. It says nothing about whether your workloads can — see the caveat below
- when the question is "why does *this* connection fail, right now" — that is a shell in the right namespace, which is [netshoot](../netshoot/README.md)

## Notes

**How it works.** Each instance discovers its peers through the Kubernetes API and pings all
of them on a schedule. Every instance therefore holds an opinion about every other, and the
UI merges those opinions into one graph. Disagreement is itself informative: if A cannot
reach B but B reaches A, the fault is directional, which points at routing or policy rather
than a dead node.

**Metrics before UI.** Goldpinger exposes Prometheus metrics, and that is the way to run it.
A dashboard nobody has open during the outage detects nothing. Wire the failure counters into
[`observability/alerting/`](../../../observability/alerting/README.md) and alert on a
**specific pair failing for a sustained window** — never on individual probe failures, which
are normal and which train people to ignore the alert.

**Relationship to the CNI.** [`network/cni/`](../../cni/README.md) is what actually implements
pod-to-pod networking; Goldpinger is how you find out whether it is doing so *uniformly*
across every node. Most of what it catches — asymmetric routes, an MTU mismatch on one node's
tunnel, a node whose overlay never converged — is a CNI or infrastructure fault, not an
application one.

**Overlap with kubenurse.** [kubenurse](../../monitoring/kubenurse/README.md) under
`network/monitoring/` covers adjacent ground and probes more surfaces — API server, DNS,
ingress round trip — from every node. Goldpinger is narrower and more visual: pod-to-pod only,
with a graph. Running both is defensible; running neither is the common mistake.

Bloomberg's, Apache 2.0.

---

[← Network troubleshooting](../README.md)
