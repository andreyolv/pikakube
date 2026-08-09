[← KubeClarity](../README.md)

# KubeClarity — Helm deployment

The Flux resources that install KubeClarity into the cluster.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://openclarity.github.io/kubeclarity` as a chart source |
| `helmrelease.yaml` | `HelmRelease` (`kubeclarity`) | installs chart `kubeclarity` version `2.23.1`, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `kubeclarity` namespace |

No values are overridden — the `values:` block carries only the reference comments. That means
chart defaults, which for KubeClarity include its bundled database and no ingress. Both are
things to revisit before treating this as anything other than an evaluation deployment:

| Default | Consequence |
|---|---|
| Bundled PostgreSQL | fine for evaluation, not something to keep inventory data in long term — see [`databases/`](../../../../../databases/README.md) |
| No ingress or authentication configured | the UI is only reachable by port-forward, which is safe by accident rather than by design |
| Scanner backends at defaults | which SBOM generator and which vulnerability scanner run is chart-configurable; leaving it default means you have not chosen |

## Notes

- The chart values references kept in the file:
  <https://artifacthub.io/packages/helm/kubeclarity/kubeclarity> and
  <https://github.com/openclarity/kubeclarity/blob/main/charts/kubeclarity/values.yaml>.

- The version pinned here (`2.23.1`) is from the standalone KubeClarity chart. As noted in
  [`../README.md`](../README.md), development has moved to the consolidated **OpenClarity**
  project, so confirm this chart is still receiving updates before relying on it.

---

[← KubeClarity](../README.md)
