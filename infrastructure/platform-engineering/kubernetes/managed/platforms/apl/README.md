[← Platforms](../README.md)

# APL

<https://github.com/linode/apl-core>

---

## The problem it solves

Application Platform for LKE — Akamai/Linode's open-source Kubernetes platform distribution, and the
continuation of [Otomi](../otomi/README.md) after acquisition. It installs an entire opinionated
stack in one go: ingress, certificates, GitOps, observability, logging, policy enforcement, identity
and a developer-facing console.

The proposition is that a small team gets a complete platform without spending a quarter integrating
a dozen projects, and without having to know which of them work well together.

## When to use it

- A green-field cluster with no existing ingress, GitOps or monitoring to conflict with
- A small team that needs a working platform faster than it can build one
- Linode/Akamai LKE, where it is the native offering
- You are comfortable accepting its component choices wholesale

## When not to use it

- A cluster already running Flux, cert-manager and an ingress controller — it brings its own of each
- Where you need to choose components yourself; the integration *is* the product
- If exiting later matters and nobody has priced it
- Alongside Otomi; they are the same product, not alternatives

## Notes

**Chart** `apl` from `https://linode.github.io/apl-core`, with a namespace manifest and empty values.
Recorded as a link only.

**The `version:` field is empty.** In a Flux `HelmRelease` an unset version resolves to the latest
available chart at reconcile time, so the deployed version can change with no commit and no review.
For a platform distribution — which upgrades every component it manages as a unit — that is the
highest-impact place in this repository for an unpinned version. Pin it before this is ever
reconciled against a cluster that matters.

**Same product as Otomi.** Otomi was acquired by Akamai and rebranded as APL; `apl-core` is the
continuation of `otomi-core`. Both folders exist here, which is useful as a record of the transition
and misleading if read as two options. If either is ever adopted, it is this one — the Otomi chart
repository is the historical artifact.

**What "distribution" means in practice**, and the thing to check first: APL installs and owns
ingress, certificate management, GitOps, monitoring, logging, policy and identity. Every one of those
is something a cluster may already have. Two ingress controllers with overlapping IngressClasses, or
two GitOps engines reconciling the same namespaces, produce failures that are hard to attribute
because both systems are working exactly as designed.

---

[← Platforms](../README.md)
