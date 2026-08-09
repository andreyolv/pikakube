[← Karpenter](../README.md)

# Karpenter — GCP provider

<https://github.com/cloudpilot-ai/karpenter-provider-gcp>

---

## The problem it solves

GKE's own answer to capacity is node pools plus the cluster-autoscaler, or Autopilot. A node pool is
a fixed machine type, a fixed disk and a fixed set of zones, decided before the workloads existed —
so a mixed workload profile means either several pools to maintain or one pool that is wrong for
half of what runs on it.

This provider brings the Karpenter model to GKE: pending pods in, an appropriately sized instance
out, chosen from whole machine families rather than one pinned type, and consolidated away again
when demand drops. Spot becomes a value of `karpenter.sh/capacity-type` rather than a separate pool.

The scheduling and disruption behaviour is identical to the other providers, because it comes from
[the upstream core](https://github.com/kubernetes-sigs/karpenter) — see
[`../README.md`](../README.md#2-core-plus-provider). Only the "create this machine" half is GCP's.

## The thing to know first: who maintains it

This is the difference that matters, and it is not technical.

| Provider | Maintained by |
|---|---|
| [AWS](../karpenter-aws/README.md) | **AWS** — `aws/karpenter-provider-aws` |
| [Azure](../karpenter-azure/README.md) | **Microsoft** — `Azure/karpenter-provider-azure`, and the engine behind AKS Node Auto Provisioning |
| **GCP** | **CloudPilot AI** — a third-party company, not Google |

AWS and Azure ship a provider for their own platform and stand behind it. Google does not, and this
fills that gap. The README carries an attribution notice stating the code is derived from
`karpenter-provider-aws` under Apache 2.0, which is the honest lineage: it is a port rather than a
parallel implementation.

That is not a criticism — the gap is real and someone had to fill it. It is a statement about what
you are depending on: at roughly 300 stars, the project's continuity rests on one company's
commercial interest, and there is no vendor escalation path when a node fails to join.

Licence is **Apache 2.0**.

## When to use it

- **GKE, and node cost matters** — spot plus consolidation is the largest single lever available
- a workload mix where one node pool machine type is always wrong for something
- capacity policy should be a reviewed Kubernetes object in Git rather than Terraform or console
  state
- the Karpenter object model is already used on another cloud and consistency is worth something

## When not to use it

- **GKE Autopilot** — Google already schedules and bills per pod; there are no nodes for Karpenter
  to provision
- the cluster-autoscaler with a small number of well-chosen node pools genuinely covers the
  workload. That is a legitimate end state, and it has Google behind it
- a third-party dependency in the node-provisioning path is unacceptable for the environment
- workloads that cannot tolerate node replacement, before PDBs and SIGTERM handling exist
- AWS or Azure — use [karpenter-aws](../karpenter-aws/README.md) or
  [karpenter-azure](../karpenter-azure/README.md)

## What to verify before adopting it

The provider is young enough that the evaluation is mostly about closing gaps rather than comparing
features. In rough order:

| Question | Why it decides the outcome |
|---|---|
| **The NodeClass kind and its fields** | the provider-specific object — machine family, image, disk, service account, network. Read the CRD, not a blog post |
| **How the instance authenticates to GCP** | Workload Identity Federation is the expected route; a static service-account key would be a finding, not a configuration |
| **How a new instance joins the cluster** | this is where the Azure provider's [canonical failure](../karpenter-azure/README.md#the-hard-part-identity-and-bootstrap) lives, and there is no reason GCP is exempt |
| **Which machine families are discovered** | Karpenter is only as good as the set it is allowed to choose from |
| **Spot / preemptible semantics** | GCP preemptible VMs and Spot VMs are not the same product; confirm which is used and what the interruption handling is |
| **Upstream core version** | the provider pins a core version, and the v1 API migration is the dividing line |

The bootstrap row is the one to spend time on. Across every provider in this folder, the recurring
failure is not scheduling — it is a machine that gets created, appears in the cloud console, and
never registers as a Node.

## Installing it

The chart is split in two, which is the correct pattern and worth noting:

| Chart | Contains |
|---|---|
| `karpenter-crd` | the CustomResourceDefinitions |
| `karpenter` | the controller |

That split exists because **Helm does not reliably install a chart's CRDs before the resources that
use them** — the same problem recorded for [Fission](../../../../../software-engineering/serverless/fission/README.md)
and [ByConity](../../../../../databases/analytical/byconity/README.md) in this repository. Installing
the CRD chart first, as its own release, makes CRD upgrades explicit rather than something Helm
silently skips.

In a Flux setup that means two `HelmRelease` objects with a `dependsOn` between them, not one.

## Notes

Added to the catalogue from <https://github.com/cloudpilot-ai/karpenter-provider-gcp>. Nothing is
deployed — there is no GCP account in this platform, which is also true of the
[AWS](../karpenter-aws/README.md) and [Azure](../karpenter-azure/README.md) entries.

What makes it worth cataloguing is that it completes the picture: **the same NodePool model across
all three major clouds**, which is the strongest argument for Karpenter as a concept. Capacity policy
stops being three different vendor mechanisms and becomes one Kubernetes API with three backends.

The caveat in section 2 is the part to carry forward. AWS and Azure are vendor-maintained; this is
not. For a portfolio catalogue that distinction belongs in the record, because "Karpenter works on
all three clouds" is true and slightly misleading — on two of them the cloud provider is
accountable for it, and on the third a startup is.

Worth re-checking periodically: whether Google adopts or blesses a provider, and whether this one
publishes a stability designation. Both would change the recommendation.

---

[← Karpenter](../README.md)
