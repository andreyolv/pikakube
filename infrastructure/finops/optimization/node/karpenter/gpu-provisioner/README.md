[← Karpenter](../README.md)

# gpu-provisioner

<https://github.com/Azure/gpu-provisioner>

---

## The problem it solves

GPU nodes are the most expensive capacity in a cluster and the least tolerable to leave idle. A GPU
agent pool sized for the largest training job costs the same when nothing is running.

`gpu-provisioner` is Microsoft's Karpenter-derived controller for **provisioning GPU nodes on AKS on
demand**. It implements the Karpenter cloud-provider interface, so it speaks the same objects —
`NodeClaim`, `NodePool`, `AKSNodeClass` — and creates a GPU VM when one is claimed, then removes it
when the claim goes away.

Its actual purpose is narrower than that description suggests: it exists to serve **KAITO**
(<https://github.com/kaito-project/kaito>), the Kubernetes AI Toolchain Operator, which provisions
GPU capacity for model inference and fine-tuning workspaces. When a KAITO `Workspace` needs a GPU
node, this is what creates it.

## When to use it

- **AKS plus KAITO**, running model workspaces that need GPU nodes created and destroyed per workload
- GPU capacity that should exist only while a job does, expressed as a Kubernetes object
- a specific GPU SKU is required and should be requested explicitly rather than pre-provisioned

## When not to use it

- **as a general node autoscaler.** It is not one, despite the shared API. General cluster capacity
  on Azure — GPU nodes included — belongs to
  [karpenter-provider-azure](../karpenter-azure/README.md), which handles GPU SKUs in an ordinary
  NodePool
- as "Karpenter for GPUs" on any cloud other than Azure
- when KAITO is not in the picture; without it the value is mostly the Karpenter API you already
  have from the standard provider
- alongside karpenter-provider-azure managing the same nodes — two controllers, one set of
  NodeClaims, conflicting decisions

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/Azure/gpu-provisioner>** — the project. Karpenter core with an Azure GPU
cloud-provider implementation, maintained by Microsoft as part of the KAITO ecosystem rather than as
a standalone autoscaler. That provenance is the thing to keep in mind: its roadmap follows KAITO's
needs, not a general cluster's.

**On the deployment here.** Installed by Flux from a `GitRepository` rather than a Helm repository —
the chart is not published anywhere, so the source is the tag `v0.3.3` of the GitHub repository with
an `ignore` rule that pulls only `/charts/gpu-provisioner`. The HelmRelease targets `kube-system`.

That shape is worth recognising because it recurs across this platform: **when a project ships a
chart in its Git tree and publishes nothing, Flux's `GitRepository` plus an ignore filter is the
clean way to consume it.** The cost is that renovation is a tag bump in the source object, and there
is no chart version to reason about.

**The `NodeClaim` example.** The interesting artefact in this folder is a hand-written `NodeClaim`
(`karpenter.sh/v1`) rather than a NodePool — which is unusual, and is how you provision one specific
GPU machine deliberately instead of letting a controller decide:

- labels `karpenter.sh/nodepool: kaito` and `kaito.sh/workspace` — the KAITO wiring
- annotation `karpenter.sh/do-not-disrupt: "true"` — **this node must not be consolidated or
  expired.** On a GPU node running a long job, that annotation is doing real work
- a taint `sku=gpu:NoSchedule`, so nothing without a matching toleration lands on the expensive
  machine
- `node.kubernetes.io/instance-type` restricted to `Standard_NC12s_v3`, with a long list of other
  NC/ND/NV sizes commented out — a record of the SKUs that were considered
- `ephemeral-storage: 120Gi` requested, which is what model weights need on disk

The accompanying `Job` is the standard MNIST TensorFlow sample from the AKS documentation, requesting
`nvidia.com/gpu: 1` and tolerating the `sku=gpu` taint. It is a smoke test: it proves a GPU node was
provisioned, the device plugin works, and the toleration matches — in a few minutes, before anything
expensive is scheduled.

Two things that combination demonstrates and that generalise to any GPU capacity:

1. **taint the GPU nodes and tolerate deliberately.** Otherwise ordinary pods drift onto the most
   expensive machines in the cluster and block them from being reclaimed.
2. **`do-not-disrupt` on GPU workloads.** Consolidation logic that is correct for stateless web
   services is destructive for a fine-tuning run that has been going for six hours.

---

[← Karpenter](../README.md)
