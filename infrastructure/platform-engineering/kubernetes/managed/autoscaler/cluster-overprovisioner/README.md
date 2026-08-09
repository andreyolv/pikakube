[← Autoscaler](../README.md)

# Cluster Overprovisioner

<https://github.com/deliveryhero/helm-charts/tree/master/stable/cluster-overprovisioner>

---

## The problem it solves

Adding a node takes minutes — cloud API call, VM boot, node registration, image pull. If a real pod
has to wait for that, the user waiting behind it does too.

Overprovisioning buys the latency back with money. It runs **placeholder pods** that do nothing but
request CPU and memory, at a **negative PriorityClass**. They hold real capacity on real nodes. When
a genuine pod is scheduled, the scheduler preempts a placeholder instantly and the pod starts on a
node that already exists. The evicted placeholder then goes `Pending`, and *it* triggers the slow
node addition — in the background, with nobody waiting.

The result: scale-up feels instant, and the cluster is permanently one node bigger than it strictly
needs to be.

## When to use it

- Traffic spikes where minutes of scale-up latency is a visible outage
- Rolling deployments that need headroom to place new pods before old ones terminate
- Batch bursts that arrive all at once and should not queue behind VM boots
- Anywhere the cost of a spare node is clearly less than the cost of the wait

## When not to use it

- Cost is the priority — this deliberately pays for idle capacity
- Workload arrives predictably; schedule the capacity instead of holding it permanently
- Fixed-size clusters, where there is nothing to preempt into
- Before the Cluster Autoscaler itself works properly; this is a latency fix layered on top of it

## Notes

**Chart** `cluster-overprovisioner` version `0.7.11`, with values left empty and the upstream
references kept as comments:

- `https://artifacthub.io/packages/helm/deliveryhero/cluster-overprovisioner`
- `https://github.com/deliveryhero/helm-charts/blob/master/stable/cluster-overprovisioner/values.yaml`

**The `HelmRepository` URL is wrong.** The source named `deliveryhero` points at:

```
https://kubernetes.github.io/autoscaler
```

That is the **Kubernetes autoscaler** chart repository — the one
[cluster-auto-scaler](../cluster-auto-scaler/README.md) legitimately uses. It does not publish a
`cluster-overprovisioner` chart. Delivery Hero's charts are served from
`https://charts.deliveryhero.io/`.

As written, Flux will fetch the index, fail to find the chart, and the `HelmRelease` will never
become ready. It reads like a copy-paste from the neighbouring folder. Recorded here rather than
silently fixed, because a chart reference that cannot resolve is exactly the kind of thing that sits
unnoticed in a GitOps repository until someone tries to use it.

**The mechanism, in one line:** it works entirely through `PriorityClass` preemption, so it needs no
special permissions and no controller of its own — the chart is a Deployment of pause containers
plus a negative-priority class. Understanding that is enough to reimplement it in twenty lines if
the chart ever becomes a problem.

---

[← Autoscaler](../README.md)
