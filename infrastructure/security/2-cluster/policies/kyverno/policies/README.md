[← Kyverno](../README.md)

# Kyverno policies

Policies intended for this cluster, as opposed to [`../examples/`](../examples/README.md), which is
a catalogue to learn from.

Contents: [`sync-secret/`](sync-secret/README.md) — clone a TLS Secret into every namespace

## Contents

1. [What belongs here](#1-what-belongs-here)
2. [Why `generate` is the policy worth having](#2-why-generate-is-the-policy-worth-having)
3. [The RBAC requirement](#3-the-rbac-requirement)
4. [Anti-patterns](#4-anti-patterns)
5. [How this applies to pikakube](#5-how-this-applies-to-pikakube)

---

## 1. What belongs here

The split between this folder and `../examples/` is worth keeping deliberate:

| | `policies/` | `examples/` |
|---|---|---|
| Intent | applied to this cluster | read, copied, adapted |
| Reviewed as | production configuration | reference material |
| Enforcement mode | a decision that has been made | often `Audit`, often commented out |

Right now the folder holds one policy, and it is a `generate` rule rather than a `validate` one —
which, for a platform, is the more useful shape.

Note that neither this folder nor its contents appear in the Kyverno `kustomization.yaml`, which
lists only the namespace, the chart source, the HelmRelease and `rbac.yaml`. The policy here is
applied by hand, and the notes in [`sync-secret/`](sync-secret/README.md) record exactly that
(`kubectl apply -f`).

## 2. Why `generate` is the policy worth having

Most policy engines can only refuse. Kyverno can create.

Consider the requirement "every namespace must have a TLS Secret so its Ingress can serve HTTPS".
Two ways to enforce it:

| Approach | What happens |
|---|---|
| `validate` — reject a namespace with no TLS Secret | the namespace cannot be created until someone copies a Secret in by hand. The error is confusing, the fix is manual, and the copy drifts. |
| `generate` — create the Secret when the namespace appears | the namespace is correct the moment it exists, and stays in sync with the source |

The second is strictly better and it is not a security compromise — it removes the failure mode
rather than reporting it.

The same shape covers the other per-namespace defaults a platform needs: a default deny
NetworkPolicy, an image-pull Secret, a ResourceQuota, a LimitRange. Each of those is a policy that
*produces* the compliant state.

Two fields control the behaviour and both matter:

| Field | Effect |
|---|---|
| `synchronize: true` | changes to the source propagate to every copy, and deleting the generated object recreates it |
| `generateExisting: true` | apply to resources that already exist, not only to ones created from now on |

Without `generateExisting`, the rule only fires on the admission event, so it covers new namespaces
and silently ignores every namespace that was already there. That is the exact gap recorded in the
sync-secret notes, and it is the most common surprise with `generate`.

## 3. The RBAC requirement

Kyverno's default install does **not** grant access to Secrets. This is deliberate: a policy engine
that can read every Secret in the cluster is a very attractive target, and most policies do not need
it.

A `generate` rule that clones a Secret does need it, so `rbac.yaml` in
[`sync-secret/`](sync-secret/README.md) — and its counterpart at the Kyverno folder root — adds
aggregated ClusterRoles:

| ClusterRole | Verbs | Aggregated to |
|---|---|---|
| `kyverno:secrets:view` | `get`, `list`, `watch` | admission, reports and background controllers |
| `kyverno:secrets:manage` | `create`, `update`, `delete` | background controller only |

The split is the interesting part. Only the background controller — the one that materialises
`generate` rules — gets write access. The admission controller, which is the one on the API server's
write path and therefore the one most exposed, gets read-only.

The cost is honest and should be stated: after applying this, Kyverno can read every Secret in the
cluster and create Secrets anywhere. That is a real expansion of what a compromise of the Kyverno
controller would mean.

## 4. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| `generate` without `generateExisting: true` | existing namespaces are silently skipped, and nobody notices until one fails | set it, or run a one-off pass over existing namespaces |
| `generate` without `synchronize: true` | the copies drift from the source and rotation does not propagate | set it, unless divergence is intended |
| Cloning a Secret containing a private key everywhere | the key now exists in every namespace, so any namespace compromise leaks it | re-issue per namespace instead — cert-manager can, and `certificates/trust-manager` distributes public trust material without keys |
| Granting Kyverno blanket Secret access for one policy | broad standing privilege for a narrow need | the split view/manage roles here, and review whether the policy is worth it |
| Policies applied by hand, outside the kustomization | the cluster state is not in the delivery path, so it drifts and cannot be rebuilt | add them as resources to `kustomization.yaml` |
| Mixing reference examples and live policy in one folder | nobody knows which are enforced | keep the split this folder implies |

## 5. How this applies to pikakube

One policy, and it exists to solve a concrete local-development problem: mkcert issues a TLS
certificate for `*.127.0.0.1.nip.io`, every ingress in the cluster wants it, and Secrets are
namespaced.

That is a real recurring need on this platform — Vault, OpenBao, Policy Reporter and everything else
with an ingress reference `secretName: mkcert-tls-secret` — and cloning it with a policy is cheaper
than deploying a dedicated replication controller.

The gap is that the policy is not in the Kustomization, so it is not delivered by Flux. The RBAC
*is* (`rbac.yaml` at the Kyverno folder root), which means the permissions are in place for a policy
that is not. Closing that is a one-line change to `kustomization.yaml`.

The natural second policy for this folder is a default-deny NetworkPolicy per namespace — same
`generate` mechanism, and the thing that makes network segmentation the default rather than an
opt-in.

---

[← Kyverno](../README.md)
