[← Manifest scanners](../README.md)

# flux-schema

<https://github.com/fluxcd/flux-schema>
<https://github.com/controlplaneio-fluxcd/schema-catalog>

The CLI, and the schema catalogue it validates against — <https://schemas.fluxoperator.dev>. Two
repositories, one capability; the catalogue is [§ below](#the-ecosystem-catalogue-schema-catalog).

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
| A hosted ecosystem catalog | [`schemas.fluxoperator.dev`](#the-ecosystem-catalogue-schema-catalog), resolved by name rather than assembled by hand |
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

`default` is the built-in catalog; `ecosystem` resolves
[the hosted one](#the-ecosystem-catalogue-schema-catalog). Both a container image
(`ghcr.io/fluxcd/flux-schema`) and composite GitHub Actions are published, so it does not require the
`flux` CLI to be present in the runner.

The **`ecosystem` location fetches over the network**, which is worth deciding deliberately: it keeps
schemas current and makes the pipeline depend on a CDN. The image ships with the catalog embedded,
which is the answer for an air-gapped or reproducibility-sensitive pipeline.

## The ecosystem catalogue: schema-catalog

<https://github.com/controlplaneio-fluxcd/schema-catalog> · <https://schemas.fluxoperator.dev>

The CLI is only as good as the schemas it can resolve, and `-s ecosystem` resolves **this**: a
generated, hosted catalogue of JSON schemas for the CNCF ecosystem, produced *with* flux-schema from
upstream stable releases.

| | |
|---|---|
| Coverage | ~118 projects, ~8,800 schemas |
| Freshness | **regenerated daily** from upstream releases |
| Served from | `schemas.fluxoperator.dev`, on Cloudflare |
| Also exposed as | a browsable index, and an **MCP endpoint** at `/mcp` |
| Repository / owner | `controlplaneio-fluxcd` — **ControlPlane**, not the `fluxcd` org |
| Licence | **AGPL-3.0**, where the CLI is Apache-2.0 |

The project list is the recognisable shape of a platform tree, which is why the coverage claim is
credible rather than aspirational: Kubernetes and OpenShift; Crossplane, Cluster API, the AWS ACK
controllers, Azure Service Operator; Cilium, Calico, Rook, Longhorn; Istio, Linkerd, KEDA, Karpenter;
Flux, Argo, Knative, Kubeflow; Prometheus, Grafana and the vendor operators. **That list and this
repository's operator list are close to the same list** — coverage is not a percentage in the
abstract, it is whether the CRDs *you* deploy are in there.

Two properties are decisions rather than details, and both are inherited silently from a copied
command:

- **The data has a different owner and a different licence from the tool.** The CLI is a Flux project
  artefact under a permissive licence; the catalogue is a vendor artefact under a copyleft one,
  offered primarily as a hosted service. That is a normal, sustainable arrangement — the daily
  regeneration is work somebody funds — but AGPL-3.0 on a dependency is the kind of thing an
  organisation would rather notice now than in a review later. It is schema data fetched over HTTP
  rather than linked code, which is the mild end of that question.
- **`-s ecosystem` puts a third-party CDN in the CI path.** The embedded catalogue in the container
  image is the answer for an air-gapped or reproducibility-sensitive pipeline, at the cost of being a
  snapshot.

Two limits worth stating plainly: **in-house CRDs are in nobody's catalogue** — schemas for your own
operators still have to be generated from their CRD definitions and supplied locally — and a
catalogue does not reach layer 3. A perfectly schema-valid Deployment with no probes and no limits is
still [kube-score](../kube-score/README.md)'s problem.

**The MCP endpoint is the unexpected part.** `schemas.fluxoperator.dev/mcp` serves the catalogue over
the [Model Context Protocol](../../../../ai/mcp/README.md), so a coding agent can look up the real
shape of a `HelmRelease` or a `Cluster` CR instead of producing a plausible one from training data —
the same argument made for `context7` in
[`ai/` §7.10](../../../../ai/README.md#710-skills-prompts-and-context-for-agents), applied to
Kubernetes CRDs rather than library documentation. It makes generated YAML *structurally* more likely
to be right and says nothing about whether the resource is a good idea, which is a reason to run
layer 2 more rather than less.

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

**Open limitation:** <https://github.com/fluxcd/flux-schema/issues/86> — the `validate` action only
takes a root `path` and walks the whole tree, so every PR revalidates all ~1,700 manifests. The CLI
takes paths, so a `run:` step over the changed files is the workaround until it accepts a file list.

---

[← Manifest scanners](../README.md)
