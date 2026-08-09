[← Sigstore policy-controller](../README.md)

# policy-controller — Helm deployment

The Flux resources that install the Sigstore policy controller.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://sigstore.github.io/helm-charts` as a chart source |
| `helmrelease.yaml` | `HelmRelease` named `policy-controller` | installs chart `policy-controller` version `0.10.2` into the `sigstore-policy-controller` namespace, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates `sigstore-policy-controller` |

No values are overridden — the `values:` block contains only the two reference comments.

## What this does not do

Worth being explicit, because it is the difference between an installed component and a control:

- **It installs the webhook and the CRDs. It enforces nothing.** Verification requires a
  `ClusterImagePolicy` resource, and none is committed here.
- **It affects no namespace by default.** policy-controller only acts on namespaces labelled
  `policy.sigstore.dev/include: "true"`. Nothing in this repository carries that label.

So as committed, this is an evaluation install: the controller runs, watches, and admits
everything. That is the correct starting state for a rollout — see
[`../../README.md`](../../README.md) section 5 — but it should not be mistaken for enforcement.

## Notes

- The chart values references kept in the file:
  <https://artifacthub.io/packages/helm/sigstore/policy-controller> and
  <https://github.com/sigstore/helm-charts/blob/main/charts/policy-controller/values.yaml>.

- **Chart defaults decide the failure policy**, and that is a decision worth making explicitly
  rather than inheriting. See [`../../README.md`](../../README.md) section 6 for what depends on
  it — in particular whether the controller's own namespace is excluded from its webhook, which
  is what allows the cluster to recover after a restart.

- Three verifiers are staged in this tree — this one, [Connaisseur](../../connaisseur/README.md)
  and [Ratify](../../ratify/README.md). Only one should ever be enforcing.

---

[← Sigstore policy-controller](../README.md)
