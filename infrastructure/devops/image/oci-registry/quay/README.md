[← OCI registry](../README.md)

# Quay

<https://github.com/quay/quay>
<https://github.com/quay/quay-operator>

---

## The problem it solves

**Red Hat's registry platform** — the software behind `quay.io`, available to run yourself, with an
Operator to manage it.

Feature-wise it occupies the same space as [Harbor](../harbor/README.md):

| Capability | Detail |
|---|---|
| Organisations and teams | multi-tenancy with a role model |
| **Robot accounts** | machine credentials scoped per repository, which is the right model for CI |
| **Clair** integration | vulnerability scanning, from the same project family |
| Repository mirroring | sync from an upstream registry on a schedule |
| Geo-replication | multi-region distribution of the same content |
| **Time machine** | recover tags that were deleted or overwritten, within a retention window |
| Build triggers | build from a Git repository on push |
| Operator-managed | the components' lifecycle handled by an Operator, including its dependencies |

Two features stand out against Harbor. **Time machine** — a window during which deleted or
overwritten tags can be restored — is a genuinely useful safety net that nothing else in this
folder offers. And **geo-replication** is more mature, because `quay.io` itself runs on it.

The architecture is correspondingly large: the Quay application, Clair, PostgreSQL, Redis and an
object store, all managed by the Operator.

## When to use it

- **an OpenShift or Red Hat estate**, where Quay is the supported registry and the Operator is the
  expected installation path
- where a Red Hat support contract covers it and that matters
- where time-machine recovery of deleted tags is a stated requirement
- where geo-replication across regions is needed

## When not to use it

- **as a new choice on a vanilla Kubernetes cluster** — [Harbor](../harbor/README.md) covers
  substantially the same ground with a more straightforward installation, or
  [zot](../zot/README.md) if the platform features are not needed
- where an Operator and OLM are not already part of the platform
- where the deployment effort is not justified by the requirements; see the recorded note
- on a small cluster, where the component count alone rules it out

## Notes

Recorded links:

- <https://github.com/quay/quay> — the registry application itself.
- <https://github.com/quay/quay-operator> — the Kubernetes Operator, which is the intended
  installation route and manages the whole component set.

Recorded verdict, in full:

> installation is a bit rubbish, could not be bothered

Blunt, and a real evaluation outcome rather than a shrug. What is behind it: Quay's supported path
is the **Operator**, distributed through OLM, and OLM is not part of a vanilla Kubernetes cluster —
it has to be installed first. In a Flux repository where every other component is a `HelmRelease`,
that means introducing a second lifecycle mechanism to install one registry. The Operator then
brings up PostgreSQL, Redis, Clair and an object store, several of which need configuration before
anything works.

Compare with [Harbor](../harbor/README.md), which is a single `HelmRelease`, or
[zot](../zot/README.md), which is one binary. Quay is not worse software; it is software whose
installation assumes an OpenShift-shaped platform, and on anything else that assumption is the
cost.

The note is therefore recorded as a **status**, not a dismissal: Quay was evaluated, the
installation path did not fit this repository's conventions, and the evaluation stopped there.
Nothing in this folder is deployed — there are no manifests, only the reference links.

## Where it fits here

Documented for completeness among the registry options in [`oci-registry/`](../README.md), and
explicitly not a candidate here.

The functional comparison that matters: Quay and [Harbor](../harbor/README.md) answer the same
questions, and Harbor installs cleanly with Helm on any cluster. Choose Quay when the environment
is Red Hat's; choose Harbor when it is not.

---

[← OCI registry](../README.md)
