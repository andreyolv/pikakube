[← Lifecycle orchestration](../README.md)

# Kargo

<https://github.com/akuity/kargo>
<https://kargo.akuity.io/>

---

## The problem it solves

In GitOps, promoting a version between environments means editing a file in another directory.
Nothing records that it happened, nothing verifies the previous environment was healthy, and
"which version is in staging?" is answered by reading YAML.

Kargo makes promotion a **first-class operation**:

| Concept | What it is |
|---|---|
| **Warehouse** | where artefacts come from — a container registry, a Helm chart repo, a Git repository |
| **Freight** | a specific, immutable set of artefact versions — the thing that gets promoted |
| **Stage** | an environment, with the Freight currently in it |
| **Promotion** | moving Freight from one Stage to the next, with verification |

Freight is the useful abstraction. Instead of promoting "an image tag", you promote a
**coherent set** — image, chart and config together — which is what actually needs to move as
a unit.

## When to use it

- more than one environment, and promotion is currently a manual edit
- **Argo CD** is the GitOps tool, which is where the integration is
- you need to answer "what is in production, and how did it get there" without archaeology
- promotions should be gated on verification rather than on someone remembering

## When not to use it

- one environment, where there is nothing to promote
- Flux is the GitOps tool. Kargo is Argo-centric; check the fit before assuming it transfers
- the promotion process is a simple tag bump nobody has ever got wrong

## What it adds over image automation

Flux and Argo both have image update automation, which watches a registry and bumps a tag.
That is not promotion — it is the same change reaching one environment automatically.

Kargo's addition is **ordering and gating between environments**: production receives what
staging validated, not what the registry published.

---

[← Lifecycle orchestration](../README.md)
