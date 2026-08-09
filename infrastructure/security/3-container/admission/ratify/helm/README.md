[← Ratify](../README.md)

# Ratify — Helm deployment

The Flux resources that install Ratify.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://ratify-project.github.io/ratify` as a chart source |
| `helmrelease.yaml` | `HelmRelease` (`ratify`) | installs chart `ratify` version `1.14.0`, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `ratify` namespace |

No values are overridden — the `values:` block contains only the two reference comments.

## The missing half

Ratify is an external data provider. It answers questions; something else has to ask them and
act on the answer. As committed, that something else is **not present**:

| Required | Present in this repository? |
|---|---|
| Ratify | yes, this release |
| **OPA Gatekeeper** | no — Kyverno is the policy engine here |
| A Gatekeeper `Constraint` and `ConstraintTemplate` calling Ratify | no |
| `Store` / `Verifier` / `KeyManagementProvider` CRs | no |

So this release installs a component that will run, expose its API, and never be consulted.
That is a legitimate state for an evaluation — but it means the folder should be read as "Ratify
was considered", not "Ratify is enforcing anything". The architectural point is made in
[`../README.md`](../README.md): Ratify is the right choice **only** when Gatekeeper is already
the policy engine.

## Notes

- The chart values references kept in the file:
  <https://artifacthub.io/packages/helm/ratify/ratify> and
  <https://github.com/ratify-project/ratify/blob/dev/charts/ratify/values.yaml>. Note the second
  points at the `dev` branch, so it describes values that may be ahead of the pinned `1.14.0`
  chart.

- Three verifiers are staged in this tree — this one,
  [Connaisseur](../../connaisseur/README.md) and
  [sigstore policy-controller](../../sigstore-policy-controller/README.md). Only one should ever
  be enforcing.

---

[← Ratify](../README.md)
