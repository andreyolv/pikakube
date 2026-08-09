[← Trivy](../README.md)

# Trivy — Crossplane IAM

The AWS identity that lets the operator read image metadata from ECR, declared as Kubernetes
resources through Crossplane.

---

## The problem this solves

Trivy Operator inventories the images running in the cluster. To do that it must **pull the
image manifest and configuration from the registry**. For private ECR repositories that requires
AWS credentials, and without them every private image is reported as unscannable — the operator
appears to be working while producing nothing useful for exactly the images you care about.

The wrong answers are a static access key in a Secret, or a node role broad enough that every
pod on the node inherits registry access. The right answer is a role scoped to this one
ServiceAccount.

## What is here

| File | Resource | What it does |
|---|---|---|
| `role.yaml` | `iam.aws.upbound.io/v1beta1` `Role` | creates the IAM role `trivy-operator-eks-data-dev`, attaching the AWS managed policy `AmazonEC2ContainerRegistryReadOnly`. Its trust policy allows `pods.eks.amazonaws.com` to `sts:AssumeRole` and `sts:TagSession` |
| `podidentityassocitation.yaml` | `eks.aws.m.upbound.io/v1beta1` `PodIdentityAssociation` | binds that role to the ServiceAccount `trivy-trivy-operator` in namespace `trivy`, on cluster `eks-data-dev` in `us-east-2` |

Both are managed resources reconciled by the AWS provider, with `providerConfigRef: aws`, and
both are tagged `team: dataops`.

## Why EKS Pod Identity rather than IRSA

Two mechanisms exist for giving a pod an AWS role, and this uses the newer one:

| | IRSA (OIDC) | **EKS Pod Identity** |
|---|---|---|
| Trust principal | the cluster's OIDC provider URL | `pods.eks.amazonaws.com` |
| Setup per cluster | an OIDC provider must be registered, and the trust policy embeds the cluster-specific issuer URL | none — the same trust policy works for any cluster |
| Role reuse across clusters | awkward: the trust policy is cluster-specific | straightforward |
| Where the binding lives | an annotation on the ServiceAccount | a separate `PodIdentityAssociation` resource |

The trust policy in `role.yaml` names `pods.eks.amazonaws.com`, which is the Pod Identity
principal. Note that the [HelmRelease](../helm/README.md) *also* sets the legacy IRSA annotation
`eks.amazonaws.com/role-arn` on the ServiceAccount — harmless, and typical of a migration where
the annotation was left in place, but the association resource is what is actually granting
access here.

## Notes

- **The permission is `AmazonEC2ContainerRegistryReadOnly` and nothing else.** That is the
  correct scope: the operator reads image metadata, it never pushes. Anything broader would be a
  scanner with write access to your registry, which is a worse problem than the one it solves.

- **The naming ties the role to one cluster** — `trivy-operator-eks-data-dev` — which is the
  right convention when the same manifests are copied per environment, because it prevents two
  clusters silently sharing an identity.

- **`podidentityassocitation.yaml` is misspelled** (`associtation`). Filenames do not affect
  Kubernetes behaviour, so nothing is broken; it is worth fixing only if someone greps for it.

- The `Role` carries `description: Flux`, recording that the resource is Flux-managed rather
  than created by hand — useful when someone finds it in the AWS console and wonders where it
  came from.

---

[← Trivy](../README.md)
