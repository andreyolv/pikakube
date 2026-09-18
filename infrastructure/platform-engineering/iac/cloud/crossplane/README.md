[← Cloud control planes](../README.md)

# Crossplane

<https://github.com/crossplane/crossplane>
<https://github.com/crossplane-contrib>

Subfolders: [`crossview/`](crossview/README.md)

---

## The problem it solves

Crossplane is the vendor-neutral member of this folder. Where
[ACK](../aws-controllers-for-kubernetes/README.md),
[ASO](../azure-service-operator/README.md) and
[Config Connector](../gcp-config-connector/README.md) are each one cloud's own operator, Crossplane
is a framework: **providers** supply the managed-resource CRDs for a cloud, and everything above
them — composition, packaging, the API teams actually consume — is Crossplane's, not the vendor's.

That second half is the reason to choose it, and it is what the three vendor operators do not have
at all.

| | Vendor operators | Crossplane |
|---|---|---|
| Resource CRDs | shipped by the vendor | shipped by a **provider**, installable per resource in v2 |
| Abstraction over them | none — teams use the raw CRD | **XRD + Composition**: you define the API |
| Scope | one cloud | a provider for each, plus anything with an API |
| Governance | Kubernetes RBAC on the vendor CRD | RBAC plus whatever the composition refuses to expose |

A vendor operator gives an application team `RDSInstance` with two hundred fields. Crossplane lets
the platform team publish `PostgreSQLInstance` with four, and decide what the other hundred and
ninety-six are — region, backup retention, encryption, tags. The abstraction is the product; the
managed resources are the implementation detail behind it.

Everything in [`cloud/`](../README.md) sections 1 and 2 still applies here — no state file,
continuous reconciliation, no `plan`, a cluster that now holds cloud-admin credentials, and
deletion that follows Kubernetes rules. Crossplane does not change that trade. It changes what sits
in front of it.

## What v2 changed, and why it matters here

v2 is worth knowing about before reading anything written about v1, because the mental model moved:

- **Composite resources and managed resources are namespaced by default.** The separate *claim*
  type, the v1 workaround for giving a namespaced team a cluster-scoped resource, is no longer the
  way this is done.
- **Compositions can include any Kubernetes resource** — a `Deployment`, a `ConfigMap`, a custom
  resource — not only Crossplane-defined ones. An abstraction can now be the application *and* its
  infrastructure, which is most of what an [IDP](../../../idp/README.md) golden path is.
- **Native patch-and-transform is gone.** Compositions are function pipelines. Anything older,
  including most blog posts, describes a mode that no longer exists.
- **Managed resource filtering**: install only the resources a provider actually needs to expose,
  instead of several hundred CRDs per provider.
- **Removed**: `ControllerConfig` (now `DeploymentRuntimeConfig`), external secret stores (use
  [External Secrets](../../../../security/2-cluster/secrets/README.md)), and composite connection
  details.

The upgrade path is sequential through minor versions, and lands on v1.20 before v2.

## When to use it

- **more than one cloud**, or a serious chance of a second one — this is the only option in the
  folder that is not a single vendor's
- the platform team wants to **publish its own API** to application teams rather than expose the
  provider's CRDs directly
- the same abstraction should cover infrastructure *and* the workload that uses it (v2)
- there are non-cloud APIs to manage the same way — providers exist for far more than the three
  hyperscalers

## When not to use it

- **one cloud, and no appetite to build abstractions.** The vendor operator is less machinery for
  the same result, and ASO is the one with working manifests here
- nobody owns the compositions. An XRD is an API: it needs versioning, deprecation and a
  maintainer, exactly as [`resource-orchestrator/`](../../../kubernetes/managed/resource-orchestrator/README.md)
  section 3 describes — and that is the failure mode, not the install
- a reviewed plan before production data-store changes is non-negotiable
- the abstraction is being designed before the underlying manifests have been written by hand a few
  times; the shape is still a guess at that point

## Notes

- <https://github.com/crossplane/crossplane> — the core project. The `providers/`, `functions/` and
  `configurations/` around it are separate packages, installed into the control plane as OCI
  artefacts.
- <https://github.com/crossplane-contrib> — the community organisation, and where most
  non-hyperscaler providers, composition functions and the tooling in
  [`crossview/`](crossview/README.md) live.

Worth knowing that most modern providers are **generated from Terraform providers** by Upjet, which
is why their coverage is good and why the CRD field names read like HCL arguments. The coverage
objection in [`cloud/`](../README.md) section 2 is weaker here than for the vendor operators for
that reason.

### The comparison that actually comes up

Not ACK or ASO — [kro](../../../kubernetes/managed/resource-orchestrator/README.md). Both let you
define a simple CRD that expands into other resources with no controller code. The difference is
what they expand *into*: kro composes resources that already have controllers in the cluster,
while Crossplane brings the cloud resources with it through its providers. If the cloud CRDs come
from somewhere else — ACK, ASO — kro is the smaller way to put an API in front of them.

### What is checked in

[`crossview/`](crossview/README.md) only: a dashboard for Crossplane, with a complete Flux setup.
**Crossplane itself is not deployed here** — no provider, no XRD, no composition — which makes this
folder a description plus a UI for something that is not yet running. The
[docs write-up](../../../../../docs/platform-engineering/crossplane.md) records the Azure
compositions built with it elsewhere; none of that is in this repository.

---

[← Cloud control planes](../README.md)
