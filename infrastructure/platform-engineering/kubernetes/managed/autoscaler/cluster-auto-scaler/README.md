[← Autoscaler](../README.md)

# Cluster Autoscaler

<https://github.com/kubernetes/autoscaler>

---

## The problem it solves

Pods go `Pending` because no node has room. Someone has to add a node. Cluster Autoscaler is the
controller that watches for unschedulable pods, works out which node group would fit them, calls the
cloud provider to grow it, and later removes nodes whose pods could run elsewhere.

It is the reference implementation and the one every managed provider integrates with. Its scope is
narrow and worth stating: it scales **node groups**, driven by **pod resource requests**, in
reaction to **scheduling failures**.

## When to use it

- Any cluster whose workload volume varies and whose nodes are billed by the hour
- Batch and CI workloads, where the alternative is a permanently oversized cluster
- Multiple node groups where you want a defined preference order between instance types
- Managed clusters — it is the mechanism EKS, AKS and GKE expect

## When not to use it

- Fixed on-premise hardware; there is no cloud API to call, and nothing to save
- As a response to traffic spikes — minutes of latency; use [overprovisioning](../cluster-overprovisioner/README.md)
- Alongside a cloud-native node autoscaler managing the same node groups; they will fight
- Before resource requests have been audited — it will scale correctly to satisfy nonsense

## Notes

**Chart** `cluster-autoscaler` version `9.58.0`, from `https://kubernetes.github.io/autoscaler`.
Values are left empty in the `HelmRelease`, with the upstream references kept as comments:

- `https://artifacthub.io/packages/helm/cluster-autoscaler/cluster-autoscaler/`
- `https://github.com/kubernetes/autoscaler/blob/master/charts/cluster-autoscaler/values.yaml`

**The priority expander.** The `configmap.yaml` beside this file is the interesting artifact —
`cluster-autoscaler-priority-expander` in `kube-system`:

```yaml
priorities: |-
  10:
    - .*t2\.large.*
    - .*t3\.large.*
  50:
    - .*m4\.4xlarge.*
```

What it does: when more than one node group could satisfy a pending pod, the **priority** expander
picks the group whose name matches a regex at the highest number. Here `m4.4xlarge` at 50 beats the
`t2`/`t3.large` groups at 10 — large instances are preferred, and the burstable small ones are the
fallback for what does not fit or when the large group cannot scale.

This matters more than it looks. The default expander is `random`, which will happily pick a node
group that technically fits and is the wrong shape or price. The priority expander is how you say
"prefer these, in this order" without writing a scheduler.

Two references were recorded with it:

- <https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/expander/priority/readme.md>
  — the expander's own documentation, which is the only complete description of the format.
- <https://itnext.io/kubernetes-resources-and-autoscaling-from-basics-to-greatness-7cae17fbf27b>

Note the ConfigMap is AWS-specific by construction: those regexes match AWS Auto Scaling Group
names. On another provider the same mechanism works, but every pattern has to be rewritten.

**Recorded upstream issues**, kept as filed:

- <https://github.com/kubernetes/autoscaler/issues/7086>
- <https://github.com/kubernetes/autoscaler/issues/8879>

They are preserved without a summary because the notes carried none — the point of recording them is
that the autoscaler's behaviour was checked against open upstream problems rather than assumed
correct. Read them before spending a day on unexpected scale-down behaviour.

---

[← Autoscaler](../README.md)
