[← Karpenter](../README.md)

# Karpenter — Azure provider

<https://github.com/Azure/karpenter-provider-azure>

---

## The problem it solves

On AKS, capacity means agent pools: a VMSS per shape, with a fixed SKU, a fixed zone and a fixed
priority. Adding spot means another pool, adding a memory-heavy SKU means another pool, and the
cluster-autoscaler only ever removes nodes that are already empty.

This provider brings Karpenter's model to Azure: pending pods in, an appropriately sized VM out,
chosen from whole SKU families rather than one pinned type, and consolidated away again when demand
drops. Spot is a value of `karpenter.sh/capacity-type` rather than a separate pool to maintain.

It is also the engine behind **AKS Node Auto Provisioning (NAP)** — the managed version of the same
controller. Running the chart yourself gives full control of the NodePool and `AKSNodeClass` objects
and full responsibility for the identity and bootstrap plumbing; NAP hands both to AKS.

## When to use it

- **AKS, and node cost matters** — spot plus consolidation is the largest single lever available
- a workload mix where one agent pool SKU is always wrong for something
- capacity policy should be a reviewed Kubernetes object in Git rather than portal or Terraform state
- you want control over the NodePool disruption policy that the managed NAP option does not expose

## When not to use it

- when AKS Node Auto Provisioning covers the requirement — it is the same controller with the
  identity and bootstrap work already done, which is precisely the part that hurts (see the notes)
- workloads that cannot tolerate node replacement, before PDBs and SIGTERM handling exist
- alongside the cluster-autoscaler on the same pools — one owner per pool
- AWS — use [karpenter-aws](../karpenter-aws/README.md)
- provisioning GPU nodes for KAITO workspaces specifically — that is
  [gpu-provisioner](../gpu-provisioner/README.md), which is a different controller with the same API

## The hard part: identity and bootstrap

Self-hosting on AKS means wiring up three things that NAP does for you:

| Piece | What it is |
|---|---|
| **A user-assigned managed identity** with rights to create VMs in the node resource group | how Karpenter is allowed to provision at all |
| **Workload identity federation** to the controller's ServiceAccount | how the pod gets that identity |
| **The kubelet bootstrap token and cluster join configuration** | how a new VM becomes a Node |

The third is the one that produces the classic failure: the VM boots, appears in Azure, and never
joins the cluster. Everything looks correct except that no Node object appears. The commands in the
notes below exist to inspect exactly that.

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/Azure/karpenter-provider-azure>** — the Azure provider. Cloud-agnostic
scheduling lives upstream in `kubernetes-sigs/karpenter`; `AKSNodeClass`, SKU discovery, image
families and the AKS bootstrap logic are here.

**<https://github.com/Azure/karpenter-provider-azure/blob/main/hack/monitoring/grafana-values.yaml>**
— the project's own Grafana configuration, with dashboards for the controller. Worth taking rather
than building: it graphs provisioning latency, node counts by capacity type and disruption events by
reason, which is the answer to *"which node was removed, and why"*. Set this up **before** enabling
consolidation, not after somebody reports unexplained restarts.

**<https://github.com/Azure/karpenter-provider-azure/issues/696#issuecomment-2703637386>** —
*"Created node never joins the cluster"* (February 2025, closed). The canonical self-hosting
failure: the VM is created, and no Node ever registers. The linked comment is the one carrying the
resolution. Root causes cluster around bootstrap — an expired or missing kubelet bootstrap token,
a mismatched cluster endpoint or CA in the generated values, or a managed identity without the
rights it needs. This is the issue to read first when a NodeClaim sits unfulfilled.

**<https://github.com/Azure/karpenter-provider-azure/issues/683>** — *"how to allow karpenter to only
use sku with ephemeral OS disk support?"* (February 2025, closed). A real cost and performance
question. Ephemeral OS disks live on the VM's local storage instead of a managed disk: they are
faster and they remove a per-node managed-disk charge, but only some SKUs support them and only up
to a size limit — the `osDiskSizeGB` in the `AKSNodeClass` must fit within the SKU's cache or
temporary storage, or the node silently falls back to a managed disk. The thread covers how to
express that constraint in the NodePool requirements. Relevant here because the repository's own
`AKSNodeClass` sets `osDiskSizeGB: 512`, which is large enough to rule ephemeral out on most SKUs.

**The setup commands.** The recorded sequence for installing the chart against an existing cluster:

```bash
export CLUSTER_NAME=xxxxxx
export RG=xxxxxxxxx
export LOCATION=eastus2
export KARPENTER_NAMESPACE=kube-system

export KARPENTER_VERSION=1.5.4
curl -sO https://raw.githubusercontent.com/Azure/karpenter-provider-azure/v${KARPENTER_VERSION}/karpenter-values-template.yaml
curl -sO https://raw.githubusercontent.com/Azure/karpenter-provider-azure/v${KARPENTER_VERSION}/hack/deploy/configure-values.sh
chmod +x ./configure-values.sh && ./configure-values.sh ${CLUSTER_NAME} ${RG} karpenter-sa karpentermsi-aks-prd
```

What this does: `configure-values.sh` interrogates the existing AKS cluster and fills the values
template with everything the controller needs to bootstrap nodes into *that specific cluster* — API
server endpoint, cluster CA, node resource group, network configuration, and the identity binding
between the `karpenter-sa` ServiceAccount and the `karpentermsi-aks-prd` managed identity.

The important consequence: **these values are cluster-specific and generated, not hand-written.**
They are also the values that go stale — the generated output is what issue 696 is usually about.
Note that the script targets `kube-system`, which is consistent with the HelmRelease here, and that
the version used to generate values (1.5.4) is ahead of the pinned chart (1.4.0); regenerate against
the version actually being installed.

**The bootstrap token commands.**

```bash
kubectl get secrets \
  --field-selector type=bootstrap.kubernetes.io/token \
  -o jsonpath='{range .items[*]}{.data.token-secret}{"\n"}{end}' \
  | while read encoded; do echo "$encoded" | base64 -d; echo; done

kubectl get secret karpenter-join-token \
  -o jsonpath="{.data.KUBELET_BOOTSTRAP_TOKEN}" | base64 -d
```

Both decode the token a new node uses to authenticate to the API server and register itself. The
first lists every bootstrap token in the cluster; the second reads the specific secret Karpenter
holds. **These are the debugging commands for "the node never joins":** if the token in
`karpenter-join-token` does not appear among the cluster's live bootstrap tokens, or has expired,
new VMs will boot and never register. Bootstrap tokens are short-lived by design, which is why this
failure appears weeks after a working installation rather than immediately.

Treat both outputs as credentials — a valid bootstrap token lets a machine join the cluster.

**On the deployment here.** Flux, from `oci://mcr.microsoft.com/aks/karpenter/karpenter` at tag
**1.4.0**, into `kube-system`, with `spotToSpotConsolidation` enabled — the gate that lets a spot
node be replaced by cheaper spot capacity instead of the fleet freezing at whatever it first
acquired.

The `NodePool` and `AKSNodeClass` examples in `example/` are the more informative part: spot capacity
type, `WhenEmptyOrUnderutilized` consolidation, `expireAfter: 168h`, SKU families limited to D, E and
L, a memory ceiling below 512 GiB, a single zone (`eastus2-1`), and NodePool limits of 100 CPU /
1000 GiB. A commented-out question is recorded alongside — *whether Azure already applies the
`kubernetes.azure.com/scalesetpriority` taint automatically, and to test without it first*. AKS
applies that taint to spot agent pools by convention, so the manual taint may well be redundant
here — and testing without it is the right instinct, because a duplicated taint is invisible until
some workload cannot be scheduled and nobody remembers which of the two put it there.

---

[← Karpenter](../README.md)
