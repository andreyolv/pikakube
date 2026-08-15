[← Network policies](../README.md)

# network-policy-api — ClusterNetworkPolicy

<https://github.com/kubernetes-sigs/network-policy-api>

<https://network-policy-api.sigs.k8s.io>

The upstream answer to everything the core `NetworkPolicy` cannot express: a **cluster-scoped**
policy with real `Deny`, priorities, and tiers that sit above and below the namespaced API.

---

## The problem it solves

The core API's limits are not accidents, they are scope decisions — and
[§5](../README.md#5-policies-are-additive-there-is-no-deny-rule) states them exactly: every rule is
an allow, policies are additive, nothing can subtract, there is no order, and everything is
namespaced. Three consequences follow that no amount of careful YAML fixes:

| Gap | What it means in practice |
|---|---|
| **No cluster-wide rule** | *"no namespace may ever reach the cloud metadata endpoint"* has to be written in every namespace, and re-written for every new one |
| **No deny** | a platform-wide guardrail can be **removed by any team**, simply by writing a policy that allows the traffic in their own namespace |
| **No default without isolation** | a namespace with no policy is wide open, and giving it a baseline means writing a policy per namespace forever |

Those are three descriptions of the same missing thing: **an administrative tier**. Something the
platform team owns, that applies across namespaces, that tenants cannot override — and, at the other
end, a default that applies only where tenants have not expressed an opinion.

`network-policy-api` is the SIG-Network working group that defines that tier, delivered as CRDs in
the `policy.networking.k8s.io` group. It is the same shape as
[Gateway API](../../../../network/gateway-api/README.md): a Kubernetes SIG project shipping an API
out of tree, with a conformance suite, that CNIs implement and that eventually becomes the portable
standard.

## The API, as it now stands

**Read this section before any older material, including [§6](../README.md#6-beyond-the-core-api-cni-extensions-and-clusternetworkpolicy)
of the parent page.** In `v1alpha2` (October 2025) the two original resources were **consolidated
into one**:

| Was (`v1alpha1`) | Is now (`v1alpha2`) |
|---|---|
| `AdminNetworkPolicy` | `ClusterNetworkPolicy` with `tier: Admin` |
| `BaselineAdminNetworkPolicy` (a cluster singleton named `default`) | `ClusterNetworkPolicy` with `tier: Baseline` |

The model did not change — **only the way evaluation order is expressed**. It used to be implied by
which resource you wrote; it is now a `tier` field on one resource.

### Evaluation order

Three tiers, checked in order, first match wins:

```
1. Admin tier        — ClusterNetworkPolicy, tier: Admin       ← platform team; cannot be overridden
2. NetworkPolicy     — the ordinary namespaced API             ← tenants
3. Baseline tier     — ClusterNetworkPolicy, tier: Baseline    ← the default when nobody said anything
```

Within a tier, policies are ordered by an integer **`priority`**, and **lower is evaluated first** —
the opposite convention from most systems, and the detail to check twice.

### Three actions

| Action | Effect |
|---|---|
| **`Accept`** | allow the traffic and **stop evaluating** — no later tier can take it back |
| **`Deny`** | drop the traffic and **stop evaluating** — this is the real deny the core API lacks |
| **`Pass`** | stop evaluating *this tier* and hand the decision to the next one |

`Pass` is the one that makes the design work rather than merely adding a firewall. It is how a
platform team writes *"I care about this traffic in general, but the owning namespace may decide"* —
delegation as an explicit action, instead of the all-or-nothing choice between blocking centrally
and not writing the rule at all.

The two canonical uses, which between them cover most of the value:

- **Admin tier, `Deny`:** no workload may reach `169.254.169.254`, ever. One object, every
  namespace, not overridable by a tenant policy.
- **Baseline tier, `Deny` all:** the cluster's default is deny instead of allow — the posture
  [§2](../README.md#2-the-default-is-wide-open) argues for — while any namespace that writes its own
  `NetworkPolicy` still decides for itself, because the NetworkPolicy tier is evaluated first.

That second one deserves emphasis. Default-deny today means a policy object in **every** namespace,
and a namespace created without one is silently open. A Baseline `ClusterNetworkPolicy` makes
default-deny a property of the cluster rather than a checklist item per namespace — which is the
single biggest practical improvement in this API.

## When to use it

- **you are the platform team on a multi-tenant cluster** and need guardrails that tenants cannot
  remove. This is the case the API was designed for and nothing else in Kubernetes covers it
- **cluster-wide default-deny** without a per-namespace policy and the process to guarantee one
- you already write per-tenant `NetworkPolicy` and keep discovering the gaps above
- you want the **portable** form of what you are already doing with `CiliumNetworkPolicy` or
  Antrea-native policies — same capability, one vendor-neutral object, and a conformance suite behind
  it
- you are choosing a CNI now, and want the one whose implementation of this is furthest along

## When not to use it

- **before checking that your CNI implements it.** The rule from
  [§1](../README.md#1-the-fact-that-matters-most-networkpolicy-is-an-api-not-an-implementation)
  applies with more force here, not less: these are **CRDs**, so they install and accept objects on
  *any* cluster, including one whose CNI has never heard of them. Objects apply cleanly, report
  nothing, and enforce nothing
- **as a stable API**, today. It is `v1alpha2`, it already broke once — the consolidation described
  above — and Beta is a stated target rather than a shipped fact
- for tenant-level rules. Ordinary `NetworkPolicy` remains the right tool for *"my service accepts
  traffic from my frontend"*; the admin tier is for policy the tenant does not own
- as a substitute for perimeter controls — a `Deny` here still governs pod traffic, not the account
  edge ([cloud network §2](../../../1-cloud/network/README.md#2-why-this-is-a-different-world-from-networkpolicy))
- if the cluster is single-tenant and you already write per-namespace default-deny reliably. The
  benefit is real but it is not worth an alpha API dependency

## Implementation status

The part that decides whether any of this is usable, and the part that changes fastest:

| CNI | Where it stands |
|---|---|
| [**Cilium**](../../../../network/cni/cilium/README.md) | supports `ClusterNetworkPolicy` from **1.20**, behind `--enable-k8s-cluster-network-policy` — off by default |
| [**Calico**](../../../../network/cni/calico/README.md) | implements the tiers and all three actions; there are open reports of trouble in specific dataplane combinations, so verify on your version |
| [**Antrea**](../../../../network/cni/antrea/README.md) | an early implementer of the `v1alpha1` `AdminNetworkPolicy`/`BaselineAdminNetworkPolicy` pair, alongside its own richer CRDs |
| [**OVN-Kubernetes**](../../../../network/sdn/ovn-kubernetes/README.md) | implements the tiered model — the shape OpenShift exposes as admin, namespaced and baseline tiers |
| Managed platforms | GKE has announced `ClusterNetworkPolicy` support; managed clusters are where a portable admin tier is worth the most, because the CNI is not yours to swap |

Two conclusions from the table, and they matter more than the individual rows. First, **support for
the consolidated `v1alpha2` object is newer than support for the old pair** — a CNI advertising
"AdminNetworkPolicy support" may mean `v1alpha1`, and the two are not the same object. Check the
version, not the feature name. Second, the flag on Cilium is the norm rather than the exception:
this arrives disabled, and enabling it is a deliberate cluster change.

## Notes

**It is CRDs, and that is the trap.** Because these are custom resources, `kubectl apply` succeeds
on a cluster with no implementation whatsoever. The core `NetworkPolicy` at least has a built-in
type; here the *appearance* of a working admin tier is one `kubectl apply -f` away on any cluster in
the world. The verification is the same as always and is not optional: apply a `Deny`, then confirm
the connection actually fails.

**The conformance suite is why this is worth waiting for rather than replacing.** The repository
ships conformance tests, which is what makes "portable" a checkable claim instead of a hope — the
same mechanism that turned Gateway API from a specification into something you can rely on across
implementations. It is also the reason to prefer this API over `CiliumNetworkPolicy` or Antrea CRDs
once your CNI implements it: the same policy, without the migration.

**Beta is a stated target for KubeCon NA 2026**, with the API in active development and further
proposals — FQDN-based selectors among them, which would close the other large gap named in
[§3](../README.md#why-egress-is-where-the-value-and-the-pain-both-live), where `ipBlock` is the only
way the core API can name an external destination and cloud IPs move.

**Where this fits in pikakube.** Nothing here uses it, and on this cluster it would be
theatre — [Kind](../../../../network/cni/kindnet/README.md) with kindnet enforces nothing, which is
the finding recorded in [§9](../README.md#9-how-this-applies-to-pikakube) of the parent page. It is
catalogued because it changes the *sequence* of two decisions this repository has already written
down: the CNI choice is made before segmentation is possible, and from now on that choice should be
made against **`ClusterNetworkPolicy` support**, not only core NetworkPolicy support. If this cluster
ever moves to Cilium, Calico or Antrea, the first policy to write is not a per-namespace default-deny
— it is a Baseline-tier `ClusterNetworkPolicy`, and an Admin-tier `Deny` for the metadata endpoint.

---

[← Network policies](../README.md)
