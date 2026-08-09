[← Platforms](../README.md)

# Otomi

<https://github.com/linode/apl-core>

---

## The problem it solves

Otomi was an open-source Kubernetes platform distribution: a pre-integrated bundle of ingress,
certificates, GitOps, observability, policy and identity, with a self-service developer console on
top.

It has been **acquired by Akamai and rebranded** as the Application Platform for LKE. Development
continues under [`apl`](../apl/README.md) at `linode/apl-core`; the Otomi name and chart repository
are the historical entry point.

## When to use it

- Not on its own account — use [APL](../apl/README.md), which is the same product, current
- The entry remains useful when reading older documentation, blog posts or Helm charts that predate
  the rename

## When not to use it

- As a current choice; the name is superseded
- Alongside APL, which would be installing the same platform twice
- Any of the situations where a full distribution is wrong: an existing cluster with its own ingress,
  GitOps and monitoring

## Notes

**Chart** `otomi` from `https://otomi.io/otomi-core`, with a namespace manifest and empty values.
Recorded as a link only — and note that even the recorded GitHub link points at `linode/apl-core`
rather than at an `otomi` repository, which is the rename showing through.

**The `version:` field is empty**, the same defect as in [APL](../apl/README.md): Flux would resolve
whatever the chart repository currently offers, at reconcile time, with no commit recording the
change.

**The value of keeping this folder** is not that Otomi should be deployed. It is that the pair of
folders records a specific piece of history: a platform distribution changed hands and changed name,
and the old chart repository still exists and still serves charts. Anyone finding an `otomi`
`HelmRelease` in an old repository — or following a tutorial written before the acquisition — needs
to know it is APL now.

That pattern is worth internalising beyond this one product. Platform distributions are
commercially attractive and change ownership often. Question 3 in the
[parent's evaluation list](../README.md) — who maintains it, and would you notice if they stopped —
exists because of cases exactly like this one.

---

[← Platforms](../README.md)
