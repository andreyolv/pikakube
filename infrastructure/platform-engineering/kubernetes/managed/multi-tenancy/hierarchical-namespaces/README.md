[← Multi-tenancy](../README.md)

# Hierarchical Namespaces

<https://github.com/kubernetes-sigs/hierarchical-namespaces>

---

## The problem it solves

Kubernetes namespaces are flat. There is no way to say "these five namespaces belong to the payments
team, and anything granted to the team applies to all of them" — so RoleBindings, NetworkPolicies and
quotas get copied by hand into each one and then drift.

HNC adds a **parent–child relationship** between namespaces and propagates objects down the tree. A
RoleBinding created in the parent appears in every descendant, and stays in step when it changes.
Teams can also create subnamespaces beneath their own without cluster-wide namespace-creation rights.

It is a `kubernetes-sigs` project, which is a meaningful signal for something that intercepts
namespace operations.

## When to use it

- Organisational structure that genuinely is a tree — division, team, environment
- RBAC and policy that should be inherited rather than duplicated
- Delegated namespace creation, scoped beneath a parent a team already owns
- You want a small, well-scoped addition rather than a tenancy framework

## When not to use it

- Flat tenants with enforced policy — [Capsule](../capsule/README.md) is a better shape for that
- Tenants needing their own CRDs or API version — [vcluster](../vcluster/README.md)
- Hard multi-tenancy; propagation is convenience, not isolation
- If the organisation is not actually a hierarchy; forcing one produces a fake tree nobody maintains

## Notes

**Installed from a `GitRepository`**, with a namespace manifest and examples:
`examples/hncconfiguration.yaml`, and `examples/namespaces/parent.yaml` and `child.yaml`. The
examples are the useful part — the propagation model only becomes clear once you have a parent and a
child in front of you.

Sourcing the chart from Git rather than a Helm repository is the same pattern used by
[KubeView](../../dashboards/kubeview/README.md) here: the project does not publish a packaged chart,
so Flux builds it from the repository tree. It works, and it means upgrades are a Git ref change
rather than a chart version bump.

**What `HNCConfiguration` controls** is worth understanding before applying the example: it is a
single cluster-scoped object listing which resource types are propagated and how —
`Propagate`, `Remove` or `Ignore`. By default only RBAC objects (Roles and RoleBindings) propagate.
Adding types is how NetworkPolicies, LimitRanges or ConfigMaps come along too.

Two consequences that catch people out:

- **Propagation overwrites.** A propagated object in a child namespace is managed by HNC; edit it
  locally and the change is reverted. That is the intended behaviour and it surprises everyone once.
- **Adding a type to the configuration is retroactive and cluster-wide.** Propagating Secrets, for
  instance, copies them into every descendant namespace — which is either exactly what you wanted or
  a significant accidental disclosure.

**It works through an admission webhook**, so the warning in the
[parent](../README.md) applies here as much as it does to Capsule: a broken webhook affects namespace
operations. HNC's scope is narrower and its SIG maintenance is reassuring, but the failure mode is
the same one.

No notes were recorded against this tool beyond the project link — installed, exercised with
examples, no problems written down.

---

[← Multi-tenancy](../README.md)
