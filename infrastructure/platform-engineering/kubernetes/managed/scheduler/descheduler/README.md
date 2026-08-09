[← Scheduler](../README.md)

# Descheduler

<https://github.com/kubernetes-sigs/descheduler>

---

## The problem it solves

The scheduler places a pod once and never reconsiders. The cluster then changes — nodes are added,
utilisation becomes lopsided, affinity rules would now be better satisfied elsewhere, pods sit in a
broken state — and nothing corrects it.

The descheduler runs periodically and **evicts** pods that violate its policies. Eviction is all it
does: the scheduler then places them again, and because the cluster has changed, usually somewhere
better. It respects PodDisruptionBudgets, so eviction is cooperative rather than forced.

## When to use it

- Rebalancing after adding nodes, when everything stays on the old ones
- Clearing pods stuck in `ImagePullBackOff` or similar states beyond a time limit
- Enforcing affinity or topology rules that have been violated since placement
- Removing duplicate pods of the same workload from a single node

## When not to use it

- **To fix `Pending` pods that cannot be scheduled** — the central limitation; see below
- Where evicting a pod is expensive: long-running jobs, stateful workloads mid-operation
- Without PodDisruptionBudgets, where it can evict more than a service can survive
- As a substitute for fixing whatever put pods in the wrong place

## Notes

### The finding that matters

Translated from the original note:

> The descheduler does not work for pods in `Pending` status when the pod is **unschedulable** — it
> only works for pods in `Pending` allocated to a node. So it will not work around the Gatekeeper
> problem where a pod tries to schedule onto a VM that does not exist.

- <https://github.com/kubernetes-sigs/descheduler/issues/1183#issuecomment-1622026879>

This is the most important sentence in the folder, because it contradicts the intuition that brings
most people here. The descheduler's only action is **eviction**, and eviction operates on a pod bound
to a node. A pod that no node can accept is not bound to anything, so there is nothing to evict and
the descheduler cannot see it as a problem.

The concrete case it failed to solve — a workload repeatedly trying to schedule onto a node that no
longer existed — is exactly the shape of problem people expect it to fix. The fix for that class of
issue is upstream of scheduling: correct the node selector, the affinity, or whatever names the
missing node.

### Other recorded issues

- <https://github.com/kubernetes-sigs/descheduler/issues/1046>
- <https://github.com/kubernetes-sigs/descheduler/issues/651>
- **No OCI repository support** — <https://github.com/kubernetes-sigs/descheduler/issues/1470>

The last one is a GitOps constraint rather than a scheduling one, and it is the reason this tool is
installed from a Helm repository while several of its neighbours use `OCIRepository`. Worth recording,
because "why is this one wired differently" is otherwise an unanswerable question six months later.

### The committed policy

`example/deschedulerpolicy.yaml` uses the `PodLifeTime` plugin, and it is a very specific piece of
operational engineering:

```yaml
- name: "PodLifeTime"
  args:
    maxPodLifeTimeSeconds: 1800
    namespaces:
      exclude: ["default", "kube-system", "kube-public", "kube-node-lease", "flux-system"]
    labelSelector:
      matchExpressions:
      - { key: dag_id, operator: Exists }
    states:
      - "Pending"
      - "PodInitializing"
      - "ContainerCreating"
      - "ImagePullBackOff"
      - "ErrImagePull"
      - "InvalidImageName"
```

What it is actually doing: evict any pod carrying a `dag_id` label — an Airflow task pod — that has
been stuck in a **non-running state** for more than 30 minutes. Not old pods; *stuck* pods. The
`states` list is the discriminator, and it is entirely image-pull failures plus early startup states.

The reasoning is sound. An Airflow task pod that cannot pull its image will sit there indefinitely,
holding its scheduled slot and its resource requests. Evicting it after 30 minutes lets Airflow's own
retry logic take over, which is the mechanism that actually knows what to do.

Note the excluded namespaces: system namespaces and **`flux-system`**. Evicting the GitOps controller
because it happened to be restarting would be an unpleasant way to learn to write that exclusion.

Read alongside the finding above, the policy is consistent with the limitation: every state in that
list is a state a **bound** pod can be in. Nothing here attempts to address unschedulable pods,
because nothing could.

---

[← Scheduler](../README.md)
