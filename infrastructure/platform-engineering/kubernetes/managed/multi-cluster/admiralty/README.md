[← Multi-cluster](../README.md)

# Admiralty

<https://github.com/admiraltyio/admiralty>

---

## The problem it solves

Admiralty makes other clusters appear as **virtual nodes** in the local one. A pod annotated for
multi-cluster scheduling is intercepted, a proxy pod is placed on a virtual node, and the real pod is
created in the target cluster. To everything local it looks like a pod running on a node.

The consequence is that no new scheduling concepts are introduced. Deployments, Jobs, affinities,
taints and tolerations all keep working — the scheduler simply has more nodes to choose from, and
some of them happen to be entire clusters.

## When to use it

- Bursting capacity from one cluster to another when the first is full
- Batch and CI workloads that can run anywhere and do not hold state
- You want the existing scheduler to make the decision rather than a new policy language
- Incremental adoption — it is opt-in per pod, via annotation

## When not to use it

- Stateful workloads; the volume stays in the cluster it was created in
- Where pods need to reach each other across clusters — Admiralty does not solve networking
- Complex placement policy; [Karmada](../karmada/README.md) has an actual policy model
- When observability is not already centralised, because the pod you are debugging is somewhere else

## Notes

**Installed from an `OCIRepository`.** Recorded as a link only, with no commands or evaluation.

The mechanism is worth understanding because it explains both the appeal and the limits. Admiralty is
built on the [virtual-kubelet](../../../on-premise/nodes/virtual-kubelet/README.md) pattern: register
something that speaks the kubelet API and is not a machine. Here the thing behind the fake node is
another cluster's API server.

What that buys: the local scheduler's entire vocabulary works unchanged.

What it hides, and this is the part to be deliberate about:

- **The pod is not where the API says it is.** `kubectl logs` and `kubectl exec` are proxied; when
  the proxy or the link fails, the symptoms are unlike any single-cluster failure.
- **Network locality is invisible to the scheduler.** A pod placed remotely still expects to reach
  the services it always reached, and those are in the other cluster.
- **Volumes do not travel.** Anything with a PersistentVolumeClaim is effectively pinned.

The natural comparison is [Liqo](../liqo/README.md), which uses the same virtual-node idea but also
brings cross-cluster networking and storage. Admiralty is the smaller, more focused tool: scheduling
only, and you supply the rest.

---

[← Multi-cluster](../README.md)
