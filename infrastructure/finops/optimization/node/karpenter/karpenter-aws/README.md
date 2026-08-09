[← Karpenter](../README.md)

# Karpenter — AWS provider

<https://github.com/aws/karpenter-provider-aws>

---

## The problem it solves

On EKS, capacity means managed node groups: an Auto Scaling Group per shape, created before the
workloads existed. A pod requesting 2 CPU triggers whatever machine the group was defined as, spot
fallback means yet another group, and nothing ever repacks what is left after a peak.

This provider implements Karpenter's "buy the machine that fits" model against EC2. It reads the
pending pods, chooses instance types from the whole permitted set, launches them directly, and
consolidates them away again — including replacing spot nodes with cheaper spot nodes when
`spotToSpotConsolidation` is enabled.

It is the original Karpenter provider and the most mature one. On AWS this is the default answer for
node autoscaling.

## When to use it

- **EKS, and cost matters** — this is the baseline choice, not an optimisation
- a workload mix diverse enough that fixed node groups are always the wrong size
- running production on spot, where diversification across many instance types is what makes it
  survivable
- capacity policy should live in Git as Kubernetes objects rather than in ASG definitions

## When not to use it

- workloads that cannot tolerate a node being replaced, without PodDisruptionBudgets and handled
  SIGTERM in place first — see [`karpenter/`](../README.md) section 4
- clusters where node lifecycle is owned by something else; two controllers on the same nodes is a
  fight, not a strategy
- a genuinely uniform, static workload where a single right-sized node group already fits — the
  operational surface is not free
- non-EKS AWS Kubernetes where the required IAM and instance profile plumbing cannot be provisioned
- Azure — use [karpenter-azure](../karpenter-azure/README.md)

## The IAM problem

The single most painful part of adopting this, and the subject of most of the notes below.

Karpenter needs substantial EC2 permissions: create and terminate instances, manage launch
templates, pass roles, read pricing and, for spot, consume the interruption queue. AWS documents
these **as a CloudFormation template**, not as a policy document — so getting a plain policy means
reading generated YAML and reconstructing the JSON by hand.

The practical workaround is the `terraform-aws-eks` Karpenter submodule's `policy.tf`, which
expresses the same permissions as readable Terraform and is straightforward to translate.

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/aws/karpenter-provider-aws>** — the provider repository. Cloud-agnostic
scheduling behaviour lives upstream in `kubernetes-sigs/karpenter`; anything EC2-specific — instance
type discovery, `EC2NodeClass`, AMI families, interruption queue handling — is here.

**<https://medium.com/@fidelissauro/karpenter-estrat%C3%A9gias-para-resili%C3%AAncia-no-uso-de-spot-instances-em-produ%C3%A7%C3%A3o-398c7bff2cdc>**
— "Karpenter: strategies for resilience when using spot instances in production", by Matheus Fidelis
(in Portuguese). Covers the practical side of running production on spot with Karpenter:
diversification across instance families, interruption handling, PodDisruptionBudgets and topology
spread. It is the applied version of the theory in [`node/`](../../README.md) section 4.

**"Utter rubbish — the permissions example uses CloudFormation garbage instead of plain, simple
IAM JSON."** The recorded complaint, and it is a fair one. AWS ships the controller's required
permissions only as a CloudFormation stack, which is useless to anyone whose infrastructure is not
CloudFormation. Extracting a policy means reading a generated template.

**<https://github.com/aws/karpenter-provider-aws/issues/2649>** — *"JSON IAM Controller Policy"*
(opened October 2022, **still open**). The same complaint, filed upstream, unresolved for years.
Its existence is the useful signal: this is a known, permanent friction point rather than something
you have misread, so plan for it instead of searching for the document that does not exist.

**<https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/docs/getting-started/getting-started-with-karpenter/cloudformation.yaml>**
— the CloudFormation template in question. The authoritative source of *what permissions are
actually required*, whatever you think of the format. Read it to extract the statements.

**<https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/modules/karpenter/policy.tf>**
— the practical answer. The community Terraform EKS module expresses the same permissions as
`aws_iam_policy_document` blocks, which are readable and map directly to JSON. If the platform is
already Terraform, use the module; if not, use this file as the reference policy.

**On the deployment here.** Installed via Flux from `oci://public.ecr.aws/karpenter/karpenter`,
chart version **0.36.0**, into a dedicated `karpenter` namespace, with:

```yaml
settings:
  featureGates:
    spotToSpotConsolidation: true
```

That feature gate is the one worth having on: without it a spot fleet never migrates to the cheaper
spot capacity that becomes available later, and the savings decay over time.

The pin at 0.36.0 is worth revisiting. Karpenter has since reached v1 APIs — `karpenter.sh/v1`
`NodePool` and `NodeClaim`, which is what the [Azure](../karpenter-azure/README.md) examples in this
repository already use. Upgrading across that boundary is an API migration, not a chart bump.

---

[← Karpenter](../README.md)
