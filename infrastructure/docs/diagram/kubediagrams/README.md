[← Diagrams](../README.md)

# KubeDiagrams

<https://github.com/philippemerle/KubeDiagrams>

---

## The problem it solves

Every other tool in this folder draws what somebody **says** is there. This one draws what
**is** there — generated from Kubernetes manifests, from a Helm chart, or from a live cluster.

That is a different guarantee, and it is the only one in this folder that cannot go stale:

| | Hand-written diagrams | KubeDiagrams |
|---|---|---|
| Source | somebody's understanding | the manifests, or the cluster |
| Accurate on day one | yes | yes |
| Accurate in six months | only if someone maintained it | **yes, it is regenerated** |
| Shows what you forgot | no | **yes** |

The last row is the underrated one. A hand-drawn architecture diagram contains what its author
remembered; a generated one contains the sidecar nobody mentions, the orphaned Service, and the
ConfigMap three Deployments read from.

## What it does

Reads Kubernetes resources and draws them as a graph with their relationships — Deployments to
their Services, Services to their Ingresses, workloads to the ConfigMaps and Secrets they mount,
ownership through to Pods.

It accepts:

| Input | Use |
|---|---|
| Manifest files | diagram the repository, in CI |
| `helm template` output | see what a chart actually produces before installing it |
| **A live cluster** | what is running right now, including what nobody committed |
| Kustomize output | the rendered result rather than the bases |

The Helm case deserves attention on its own. `helm template | KubeDiagrams` answers "what does
this chart actually create?" — which is otherwise several hundred lines of YAML to read.

## When to use it

- documenting **what is deployed**, as a reference
- reviewing a chart before adopting it
- onboarding, where the question is "what is in this cluster?"
- comparing the manifests against the live cluster, which is a drift check

## When not to use it

- **explaining how something works** — the output is complete, uniform and unreadable for that
  purpose. Use [Mermaid](../mermaid/README.md) or [Excalidraw](../excalidraw/README.md)
- a presentation to a non-technical audience
- a cluster large enough that everything at once is a wall of boxes — scope it to a namespace
- cloud infrastructure outside Kubernetes — [Diagrams](../diagrams/README.md)

## The limitation worth stating

Completeness is both the feature and the problem. A generated diagram of a namespace with thirty
workloads shows all of them at equal weight, which answers *"what exists?"* precisely and
*"how does this work?"* not at all.

That is the distinction made in [`../README.md`](../README.md#5-the-case-for-hand-drawn), and it
is why this tool complements the hand-written diagrams rather than replacing them. Scoping the
output — one namespace, one application — is what keeps it useful.

## Notes

**Not present in this repository, and it is the clearest gap in this folder.**

This repository is a large collection of Kubernetes manifests across nineteen disciplines. Every
diagram in it is currently either hand-written Mermaid or a Python script — nothing is derived
from the manifests themselves.

The immediate uses, in order of value:

1. **Per-capability diagrams** generated from the manifests, so each folder's picture cannot
   contradict its YAML
2. **`helm template` inspection** before adopting a chart, which is a recurring activity here
   given how much of the tree is `HelmRelease` resources
3. **Drift detection** — the live Kind cluster against what Flux should have applied

The first is the one that would compound, because it turns a documentation-maintenance cost into
a build step.

---

[← Diagrams](../README.md)
