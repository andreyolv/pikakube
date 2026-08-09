[← Trivy polr-adapter](../README.md)

# polr-adapter — Helm deployment

The Flux resources that install the Trivy Operator Policy Reporter adapter.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://fjogeleit.github.io/trivy-operator-polr-adapter` as a chart source |
| `helmrelease.yaml` | `HelmRelease` (`trivy` namespace) | installs chart `trivy-operator-polr-adapter` version `0.11.1`, reconciled every 5 minutes |

The release deploys into the **`trivy` namespace**, alongside the operator whose CRDs it reads.
The namespace object itself is created by the `namespace.yaml` that sits next to
[Trivy's own deployment](../../helm/README.md). No values are overridden here; the `values:`
block contains only the reference comment.

## Notes

- The chart values reference kept in the file:
  <https://github.com/fjogeleit/trivy-operator-polr-adapter/blob/main/charts/trivy-operator-polr-adapter/values.yaml>
  — that file lists which Trivy report types the adapter translates and how to switch each one
  on or off individually.

- **Running with chart defaults means every supported report type is translated.** On a cluster
  where Trivy Operator is scoped to one namespace (as it is here, via `targetNamespaces:
  airbyte`) that is fine. If the operator is later widened to the whole cluster, revisit this:
  each translated finding becomes an extra `PolicyReport` object, and the object count is the
  thing that hurts first.

- There is no `namespace.yaml` in this folder because the namespace already exists from the
  Trivy Operator deployment — see [`../../helm/README.md`](../../helm/README.md).

---

[← Trivy polr-adapter](../README.md)
