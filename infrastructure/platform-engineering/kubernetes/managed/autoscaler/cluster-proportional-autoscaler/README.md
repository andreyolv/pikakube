[← Autoscaler](../README.md)

# Cluster Proportional Autoscaler

<https://github.com/kubernetes-sigs/cluster-proportional-autoscaler>

---

## The problem it solves

Some workloads have to grow with the **size of the cluster** rather than with their own load.
CoreDNS is the canonical case: every pod in the cluster queries it, so a cluster with 200 nodes
needs more DNS replicas than one with 5 — but CPU usage on the DNS pods is a poor and lagging
signal, which makes an HPA a bad fit.

This controller watches the number of nodes and cores in the cluster and sets a Deployment's replica
count from a ladder or a linear formula. No metrics pipeline involved; the input is cluster size.

Despite the name, **it does not scale the cluster.** It scales a workload in proportion to one.

## When to use it

- CoreDNS or kube-dns replica counts
- Cluster-wide agents whose load is proportional to node count rather than to traffic
- Ingress controllers or metrics collectors sized against fleet size
- Any case where an HPA's metric would lag behind the thing that actually drives demand

## When not to use it

- Anything whose load correlates with traffic — that is an HPA
- To add or remove nodes; that is [cluster-auto-scaler](../cluster-auto-scaler/README.md)
- On a fixed-size cluster, where the input never changes
- On managed clusters where the provider already scales CoreDNS for you — check before installing a second controller

## Notes

**Chart** `cluster-proportional-autoscaler` version `1.1.0` from
`https://kubernetes-sigs.github.io/cluster-proportional-autoscaler`, values empty, with the upstream
values file referenced as a comment:

- `https://github.com/kubernetes-sigs/cluster-proportional-autoscaler/blob/master/charts/cluster-proportional-autoscaler/values.yaml`

No notes were recorded against this tool — it is a wired-up chart, nothing more.

Two things worth knowing before it is used, since the folder does not say:

- **Two scaling modes.** *Linear* gives one replica per N cores or N nodes, with optional minimum and
  maximum. *Ladder* is a step function — explicit thresholds mapping cluster size to replica count.
  Ladder is the safer default because the steps are visible in the config rather than emergent.
- **On a managed cluster, CoreDNS may already be handled.** GKE, and to varying degrees the others,
  run their own proportional scaling for cluster DNS. Installing this to manage the same Deployment
  gives two controllers writing the same field, and the replica count will oscillate.

The name is the biggest hazard here. It sits in a folder called `autoscaler/` next to a tool that
scales the cluster, and it does something entirely different.

---

[← Autoscaler](../README.md)
