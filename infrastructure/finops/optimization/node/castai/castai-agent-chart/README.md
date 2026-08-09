[← CAST AI](../README.md)

# castai-agent — the Helm deployment

<https://github.com/castai/helm-charts>
<https://github.com/castai/helm-charts/blob/main/charts/castai-agent/values.yaml>

---

## The problem it solves

[CAST AI](../README.md) is installed by piping a generated manifest from the vendor's API into
`kubectl apply`. That works once, from a laptop, and leaves nothing in Git: no record of what was
installed, no way to review a change, and no reconciliation when someone edits it in the cluster.

This folder is the same agent as a **Flux-managed HelmRelease** — a `HelmRepository` pointing at
`https://castai.github.io/helm-charts`, a `Namespace`, and a `HelmRelease` with its values in
version control. The install becomes reviewable and revertible like everything else on the platform.

## What this shape is

Three objects, and the split matters:

| Object | Why it is separate |
|---|---|
| `Namespace` (`castai-agent`) | created by Flux, with `createNamespace: false` in the values so the chart does not also try |
| `HelmRepository` in `flux-system` | one source, reusable, refreshed on a 24-hour interval |
| `HelmRelease` | the values — `provider: aks`, and `apiKeySecretRef` for the credential |

Only the read-only agent is here. CAST AI's components that provision, evict and rebalance nodes are
separate charts, and are not in this repository — which means what is deployed reports and
recommends but changes nothing. That is the right first step.

## When it fits

- evaluating CAST AI against a cluster whose costs you already believe you understand
- the whole platform is reconciled by Flux and a `curl | kubectl apply` install would be the one
  exception
- the API key must live in a Secret rather than in a values file — which is what the empty
  `apiKeySecretRef` is for

## When it does not

- a throwaway evaluation on a cluster nobody else touches; the generated manifest is faster
- when the goal is the *automation* rather than the reporting — that needs the additional charts,
  and a decision about granting an external control plane authority to delete nodes

## Notes

**No chart version is pinned.** The `HelmRelease` names the chart but not a version, so Flux
installs whatever the repository resolves to at reconcile time and will upgrade when a new one
appears. For a read-only agent that is defensible; for anything with authority over nodes it is not,
and every other release in this folder — Karpenter, Goldilocks, VPA, StormForge — does pin. Worth
pinning here too, for consistency if nothing else.

**`apiKeySecretRef` is empty in the values.** Deliberate: the key names a Secret rather than
inlining the token. The Secret itself is not in this repository, which is correct — see the
platform's secret handling rather than committing it.

**`provider: aks`** ties this deployment to Azure. The same chart takes `eks`, `gke` and others; the
value tells the agent which cloud APIs to interrogate for pricing and inventory, and getting it
wrong produces a cluster that registers but reports no cost.

**The values file reference** in the manifest points at the chart's upstream `values.yaml` and its
Artifact Hub page. That comment convention is used throughout this repository and is worth keeping:
the set of options a chart accepts is the one thing that is never in the HelmRelease itself.

---

[← CAST AI](../README.md)
