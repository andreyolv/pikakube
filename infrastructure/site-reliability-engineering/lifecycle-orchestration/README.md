[← Site Reliability Engineering](../README.md)

# Lifecycle orchestration

How a change moves through environments, and what has to be true at each gate.

Tools covered: [`kargo`](kargo/README.md) · [`keptn`](keptn/README.md)

---

## The problem it solves

GitOps answers "how does the cluster match Git". It does not answer **"how does a change get
from dev to production"**.

That gap is usually filled by convention and copy-paste: someone bumps an image tag in the
staging directory, waits, then bumps the same tag in production. It works, it is manual, and
nothing enforces that staging actually succeeded first.

The concerns this folder covers:

| Concern | Question |
|---|---|
| **Promotion** | how does an artefact move dev → staging → production? |
| **Gates** | what must be true before it moves? |
| **Verification** | did it actually work in the previous environment? |
| **Traceability** | which commit is in which environment, right now? |

## The tools

| Tool | Model | Shines when | Detail |
|---|---|---|---|
| **Kargo** | promotion pipelines over GitOps — Warehouses, Stages, Freight | you run Argo CD and want **artefact promotion** between environments as a first-class thing | [→](kargo/README.md) |
| **Keptn** | observability-driven lifecycle — pre- and post-deployment checks, SLO evaluation | deployments should be **gated on evidence**, not on someone confirming | [→](keptn/README.md) |

They solve adjacent halves:

- **Kargo** is about *movement* — what version is where, and how it advances. It makes promotion an explicit, auditable operation instead of an edit.
- **Keptn** is about *evidence* — running checks before and after a deployment and evaluating an SLO to decide whether it succeeded.

## Where this sits against neighbouring folders

| Question | Where |
|---|---|
| How does the cluster match Git? | [`platform-engineering/gitops/`](../../platform-engineering/gitops/) |
| **How does a change move between environments?** | **here** |
| How is a single release rolled out safely? | [`progressive-delivery/`](../progressive-delivery/README.md) |
| What does "successful" mean, numerically? | [`service-level/`](../service-level/README.md) |

The overlap with progressive delivery is real but the scope differs: Flagger decides whether
*this rollout* is healthy; Kargo decides whether *this version* may proceed to the next
environment at all.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Promotion by editing a tag in another directory | nothing enforces that the earlier environment succeeded | an explicit promotion with a gate |
| Different manifests per environment | production drifts from what was tested | one source, environment-specific configuration |
| Gates that are human confirmation only | "did staging work?" answered from memory | evaluate a metric or an SLO |
| No record of what is where | rollback starts with archaeology | promotion history as an artefact |

## How this applies to pikakube

Not deployed, and honestly not applicable yet: the repository has **one cluster and one
environment**, so there is nothing to promote between.

It is mapped because the moment a second environment exists, the informal approach — edit the
tag in the other folder — becomes the mechanism by which untested changes reach production.

Worth noting the ecosystem fit: Kargo pairs with Argo CD, and this repository is Flux-based.
Both are mapped under [`platform-engineering/gitops/`](../../platform-engineering/gitops/), so
the choice is open rather than settled.

---

[← Site Reliability Engineering](../README.md)
