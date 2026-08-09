[← Manifest scanners](../README.md)

# flux-schema

<https://github.com/fluxcd/flux-schema>

Schema catalog: <https://schemas.fluxoperator.dev>

---

## The problem it solves

[kubeconform](../kubeconform/README.md) validates core Kubernetes types well and **skips every
custom resource it has no schema for** — silently, reporting success. That caveat is stated twice in
[`../README.md`](../README.md#3-layer-2-is-it-kubernetes) because it is the way this whole layer
gets quietly defeated.

Closing it means feeding `-schema-location` a schema for every CRD in the repository, from an
assortment of third-party conversions of varying freshness. Nobody maintains that list, so it drifts,
and the coverage claim degrades without anything failing.

flux-schema removes that work by shipping the catalog:

| It validates against | Detail |
|---|---|
| **A built-in catalog** | Kubernetes, OpenShift, Gateway API, and **the Flux ecosystem CRDs** |
| A hosted ecosystem catalog | `schemas.fluxoperator.dev`, resolved by name rather than assembled by hand |
| **CEL rules** | expression-based checks that go past what JSON Schema can express |

It is officially maintained by the **fluxcd** organisation, and it is Apache 2.0.

## Why it matters specifically here

This repository is roughly 1,700 manifests, and the overwhelming majority of the interesting ones
are **custom resources**: `HelmRelease`, `OCIRepository`, `HelmRepository`, `GitRepository`,
`Kustomization`, plus every operator CRD catalogued across
[`infrastructure/`](../../../../README.md).

Run kubeconform here without schema locations and it validates the `Namespace` objects and skips
almost everything else. That is not a hypothetical — it is the default behaviour, and the pipeline
reports green.

flux-schema is the tool whose built-in catalog covers exactly the resources this repository is made
of.

## The CEL part

The addition that is not just "kubeconform with better schemas".

JSON Schema describes **shape**: this field is a string, that one is required, this enum has four
values. It cannot express a relationship between fields.

CEL can, which reaches a class of error that sits between layer 2 and layer 3 — structurally valid,
and wrong:

- a `HelmRelease` with `chartRef` pointing at a source kind that is not deployed
- an `interval` that is shorter than the timeout beneath it
- a field that is required only when another field has a particular value

Those are the errors that pass every schema check and fail at reconcile time.

## When to use it

- **the repository is full of custom resources**, which for any Flux-managed platform it is
- kubeconform is already in CI and its CRD coverage is the known gap
- Flux CRDs specifically need validating — this is the first-party option
- CEL rules would catch something a schema cannot

## When not to use it

- **the repository is plain core Kubernetes manifests** — [kubeconform](../kubeconform/README.md) is
  established, fast, and enough
- as a replacement for [yamllint](../yamllint/README.md); it still needs valid YAML as input
- as a replacement for [kube-score](../kube-score/README.md) — CEL narrows the gap and does not close
  it; "no probes, no limits, `image: latest`" is still layer 3
- on unrendered Helm templates. Render first — see
  [`../README.md`](../README.md#5-render-first)
- if a young tool in the CI critical path is unwelcome; `flux plugin` is a recent mechanism

## Running it

```bash
flux plugin install schema

flux schema validate ./manifests \
  --schema-location default \
  --schema-location ecosystem
```

`default` is the built-in catalog; `ecosystem` resolves the hosted one. Both a container image
(`ghcr.io/fluxcd/flux-schema`) and composite GitHub Actions are published, so it does not require the
`flux` CLI to be present in the runner.

The **`ecosystem` location fetches over the network**, which is worth deciding deliberately: it keeps
schemas current and makes the pipeline depend on a CDN. The image ships with the catalog embedded,
which is the answer for an air-gapped or reproducibility-sensitive pipeline.

## Notes

Added to the catalogue from <https://github.com/fluxcd/flux-schema>.

Worth recording how this entry was reached, because the first instinct was wrong: the name suggests a
collection of JSON Schemas for another validator to consume. It is not — it is a runnable CLI that
validates against JSON Schema **and** CEL, installed as a Flux CLI plugin.

Its place among the tools in [`../`](../README.md): it belongs in **layer 2** beside
[kubeconform](../kubeconform/README.md), and the choice between them is about what is being
validated rather than about quality.

| | kubeconform | flux-schema |
|---|---|---|
| Core Kubernetes types | yes | yes |
| **CRDs out of the box** | **no** — `-schema-location` per CRD | **yes**, built-in catalog |
| Beyond schema shape | no | **CEL rules** |
| Maturity | established, widely deployed | **newer** |
| Maintainer | an individual (yannh) | **the fluxcd org** |
| Offline | yes, with vendored schemas | yes, via the container image |

The other layer-2 alternative, [kubectl-validate](../kubectl-validate/README.md), has had no release
in roughly two years and carries an open issue titled *"State of the Project"*. Between a tool with
native CRD validation that is not maintained and one with an official catalog that is, this is the
one to try.

Nothing is deployed — it is a CLI, and it belongs in a pipeline rather than in a cluster. The
practical next step is the same one named in
[`../README.md`](../README.md#8-how-this-applies-to-pikakube): this repository has no manifest
validation in CI at all, and the resources it would most benefit from checking are precisely the ones
kubeconform cannot see without help.

---

[← Manifest scanners](../README.md)
