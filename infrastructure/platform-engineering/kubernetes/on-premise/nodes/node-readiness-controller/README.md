[← Nodes](../README.md)

# node-readiness-controller

<https://github.com/kubernetes-sigs/node-readiness-controller>

---

## The problem it solves

A new node joins the cluster and reports `Ready` as soon as the kubelet is up. The scheduler
immediately places pods on it — before the CNI DaemonSet has started, so they have no network; before
the CSI driver is running, so volumes will not attach; before the monitoring agent exists, so the
failures are unobserved.

The pods do not wait politely. They start, fail, restart, back off, and eventually recover once the
add-ons arrive — leaving a trail of `CrashLoopBackOff` and alerts from a node that was behaving
exactly as designed.

This controller gates readiness on **conditions you declare**: a node is not made schedulable until
the DaemonSets and prerequisites it depends on are genuinely running on it.

## When to use it

- Clusters where nodes join frequently — autoscaling, spot instances, CI-created clusters
- Nodes with prerequisite DaemonSets: CNI, CSI, security agents, GPU device plugins
- Eliminating the burst of failures that follows every scale-up event
- Where the first minutes of a node's life currently generate alerts nobody acts on

## When not to use it

- Static clusters where nodes join rarely; the problem barely arises
- Managed clusters that already handle add-on readiness
- Without checking the project's maturity — see the note below
- If the real fix is workloads that tolerate their dependencies not being ready, which is worth
  building anyway

## Notes

Recorded as a link and one upstream issue:

- <https://github.com/kubernetes-sigs/node-readiness-controller/issues/26>

Recording an open issue against a young project is the right instinct, and it is worth acting on
here more than elsewhere. This is a **new `kubernetes-sigs` project**, and its function is to decide
whether nodes accept work. A bug in that logic has two failure directions and both are unpleasant:
nodes that never become ready — capacity that exists and is unused, during exactly the scale-up event
that needed it — or nodes marked ready too early, which is the problem it was installed to fix.

Read issue 26 and the surrounding tracker before deploying it.

**The mechanism it builds on** is worth understanding regardless of whether this controller is
adopted: Kubernetes has **node taints** for exactly this purpose. A node can carry a
`NoSchedule` taint until something removes it, and many CNI plugins already do this — Cilium and
Calico both taint nodes until their agent is ready. This controller generalises that pattern into a
declarative one, so the same gating works for any set of prerequisites rather than only for the ones
whose authors implemented it.

Which also means there is a manual version available today: taint nodes on join and have a small job
remove the taint once prerequisites report ready. Less elegant, no new dependency, and it makes the
mechanism visible.

---

[← Nodes](../README.md)
