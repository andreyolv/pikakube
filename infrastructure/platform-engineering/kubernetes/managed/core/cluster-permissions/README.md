[← Core](../README.md)

# Cluster permissions

<https://kubernetes.io/docs/reference/access-authn-authz/rbac/>

---

## The problem it solves

Giving a group of developers enough access to work in a cluster without giving them the cluster.
This folder is one concrete answer: a `ClusterRole` called `dev-user-full-access` and a
`ClusterRoleBinding` that grants it to a group.

RBAC in Kubernetes is deliberately simple — roles list `apiGroups`, `resources` and `verbs`, and
bindings attach them to users, groups or ServiceAccounts. There are no deny rules. Everything is
additive, and that single property drives every design decision below.

## When to use it

- Handing a development team access to their own workloads plus the platform CRDs they need to see
- Binding by **group** rather than by user, so membership is managed by the identity provider
- Granting access to specific API groups a team genuinely uses — Flux, cert-manager, metrics

## When not to use it

- As a substitute for namespace-level isolation; a `ClusterRoleBinding` applies everywhere
- Where tenants need their own CRDs or API versions — RBAC cannot isolate that, and
  [vcluster](../../multi-tenancy/vcluster/README.md) is the answer
- With `["*"]` verbs on `["*"]` resources, unless you have decided that team is an administrator
- For machine access; ServiceAccounts should get a role scoped to exactly what the code calls

## Notes

**The `ClusterRole` recorded here** grants `["*"]` verbs on `["*"]` resources across a specific list
of API groups:

```
"", "extensions", "apps", "cert-manager.io", "acme.cert-manager.io",
"networking.k8s.io", "image.toolkit.fluxcd.io", "kustomize.toolkit.fluxcd.io",
"metrics.k8s.io", "helm.toolkit.fluxcd.io"
```

That list is the interesting part, because it is a portrait of the platform. The empty string is the
core API group — pods, services, secrets, configmaps. Then Flux's three groups (image automation,
Kustomize, Helm), cert-manager's two, networking, and metrics. It says: developers may do anything
to their workloads, their certificates, their ingress and their Flux resources — and nothing to
RBAC, nodes, admission webhooks or CRDs.

Two structural points about the file:

- **Secrets are included**, via the core group with `["*"]`. Anyone with this role can read every
  Secret in every namespace, which includes the credentials of everything the platform runs. That is
  a deliberate decision if it was made deliberately, and a serious one if it was not.
- The **third rule is redundant**. It grants `get, list, watch` on
  `kustomize.toolkit.fluxcd.io`, which the first rule already grants in full. Harmless, because RBAC
  is additive and the broader rule wins — but a sign the file grew by accretion, and the kind of
  thing worth cleaning up so the intent stays readable.

**The `ClusterRoleBinding`** binds to `kind: Group` with an **empty name**:

```yaml
subjects:
- kind: Group
  name:
```

Left blank as a template — the group name comes from whatever the cluster uses for identity: an
Azure AD group object ID on AKS, an IAM-mapped group on EKS, an OIDC claim elsewhere. Applied as
written it binds to nothing, which is the safe way for a template to be wrong.

Binding to a group rather than to individual users is the right call: membership then lives in the
identity provider, and joining or leaving the team does not require a cluster change.

---

[← Core](../README.md)
