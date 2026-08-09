[← Cloud](../README.md)

# aws-iam-authenticator

<https://github.com/kubernetes-sigs/aws-iam-authenticator>

---

## The problem it solves

Kubernetes has no user database. AWS already has one — IAM — with users, roles, MFA,
permission boundaries and CloudTrail. `aws-iam-authenticator` is the bridge that lets an IAM
principal authenticate to the Kubernetes API without a second credential existing anywhere.

The mechanism is the interesting part, and it is worth knowing even on a cluster that uses the
newer EKS Access Entries, because Access Entries only replaced the *mapping*, not the
authentication:

1. The client (`aws-iam-authenticator token`, or `aws eks get-token`) builds an **AWS STS
   `GetCallerIdentity` request**, signs it with SigV4 using the caller's local AWS credentials,
   and does **not** send it to STS.
2. That pre-signed URL is base64-encoded and presented to the Kubernetes API server as a bearer
   token.
3. The server-side authenticator takes the URL and **calls it**. STS validates the signature
   and replies with the caller's account, ARN and user ID.
4. The authenticator maps that ARN to a Kubernetes username and a list of groups.
5. RBAC takes over from there.

Two properties fall out of this design:

- **No AWS secret ever crosses the wire.** The signature proves possession of the key without
  revealing it — the "something you have" family from
  [`../../README.md`](../../README.md).
- **The token expires quickly** (15 minutes by default) because it is a signed request with a
  timestamp, not a credential. Short lifetime is structural rather than configured.

The mapping in step 4 is the part with the reputation. Classically it lives in the `aws-auth`
ConfigMap in `kube-system`, mapping IAM role and user ARNs to usernames and groups:

| ConfigMap key | Maps |
|---|---|
| `mapRoles` | IAM **roles** — the normal case, including node instance roles |
| `mapUsers` | IAM **users** — rarer, and usually a smell |
| `mapAccounts` | whole accounts, by ID |

That ConfigMap is the single most infamous lockout mechanism in EKS. It is not validated, it
takes effect immediately, and **a malformed edit or a deleted `mapRoles` entry can lock every
principal out of the cluster at once** — including the nodes, which use it to authenticate the
kubelet. Recovery from the fully locked-out state has historically meant recreating the
cluster.

## When to use it

- **Self-managed Kubernetes on EC2.** This is the strongest remaining case: you want IAM as the
  identity source and there is no EKS control plane to configure for you. You run the
  authenticator yourself as a static pod alongside the API server.
- **EKS clusters predating Access Entries**, where `aws-auth` is still the mapping mechanism.
  You do not run the component — EKS does — but you manage its configuration.
- **Anywhere IAM must remain the single identity source of truth**, so that offboarding in IAM
  is offboarding from the cluster, with no second directory to keep in step.

## When not to use it

- **Current EKS.** Use **EKS Access Entries**. They express the same mapping through the AWS
  API, which means IAM-controlled, CloudTrail-audited, validated, and recoverable — every
  property `aws-auth` lacks. There is no reason to choose the ConfigMap on a cluster that
  supports the alternative.
- **Anything that is not AWS.** It is AWS-specific by construction. On other clouds use the
  provider's own path; on self-managed or local clusters use
  [`federation/dex`](../../federation/dex/README.md) or a full
  [`identity-provider/`](../../identity-provider/README.md).
- **For pods that need AWS credentials.** This is the opposite direction and a completely
  different problem — see the Notes below, and
  [`workload-identity/`](../../workload-identity/README.md). Confusing the two is the single
  most common mistake in this area.
- **As a substitute for RBAC.** It produces a username and groups and stops. Every permission
  is still a RoleBinding, and mapping an IAM administrator to no group means a perfectly
  authenticated user who can do nothing.

## Notes

The recorded note for this folder was a single link, and it points at a different tool
entirely:

**`https://github.com/jtblin/kube2iam`**

kube2iam is **not** aws-iam-authenticator, and the distinction is exactly the one drawn in
[`../README.md`](../README.md) §3 — the two run in opposite directions:

| | aws-iam-authenticator | kube2iam |
|---|---|---|
| Direction | AWS identity → **into** the cluster | cluster identity → **out to** AWS |
| Authenticates | a human running `kubectl` | a **pod** calling S3, DynamoDB, SQS |
| How | pre-signed STS `GetCallerIdentity` as a bearer token | intercepts the EC2 instance metadata endpoint (`169.254.169.254`) and hands the pod credentials for the role named in a pod annotation |
| Trust anchor | IAM signature verification | pod annotation plus network interception |

So the link is filed under the wrong folder, and preserving that is useful rather than
embarrassing: it is the exact confusion that this section of the documentation exists to
prevent, recorded in the wild.

Worth adding, since kube2iam is what was actually noted: **kube2iam is legacy and should not
be deployed today.** Its mechanism — a DaemonSet that intercepts metadata traffic and answers
on behalf of pods — has structural weaknesses. Any pod with host networking bypasses it, the
metadata endpoint is a shared, unauthenticated surface, and the identity assertion is a pod
annotation rather than anything cryptographic. Its successors, `kiam` and then **IRSA (IAM
Roles for Service Accounts)**, replaced it. IRSA is the correct answer on EKS: the pod receives
a projected, audience-bound, short-lived ServiceAccount token, and AWS STS validates it against
the cluster's public OIDC issuer. That is federation, not interception, and it is the same
pattern as [azure-workload-identity](../../workload-identity/azure-workload-identity/README.md).

No manifests are staged in this folder — it holds only the link. That is consistent with the
platform being local: there is no AWS account for any of this to apply to.

---

[← Cloud](../README.md)
