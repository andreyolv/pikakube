[← CI/CD](../README.md)

# PipeCD

<https://github.com/pipe-cd/pipecd>

---

## The problem it solves

PipeCD is a **continuous delivery** tool — not CI — built around the same premise as Flux and Argo
CD: an agent inside the cluster pulls desired state from Git, so no pipeline outside ever holds
cluster credentials. See [CI/CD §2](../README.md#2-push-based-cd-vs-pull-based-gitops) for why that
distinction is the important one.

What it adds on top of plain reconciliation:

| Capability | Detail |
|---|---|
| **Progressive delivery built in** | canary, blue/green and analysis are pipeline stages in the deployment definition, not a separate controller |
| **Multi-platform, one model** | Kubernetes, Terraform, Cloud Run, Lambda and ECS all deploy through the same pipeline syntax |
| **Deployment as a defined pipeline** | explicit stages with manual approval gates, rather than "reconcile and hope" |
| **Automated rollback** | on analysis failure, back to the previous state |
| **Drift detection** | live state compared against Git, per application |
| Single binary control plane | a `piped` agent per cluster, one control plane with a UI |

The architectural difference from Flux and Argo CD is worth stating precisely: those two reconcile
toward a desired state and delegate progressive rollout to a separate controller
([Flagger or Argo Rollouts](../../../site-reliability-engineering/progressive-delivery/README.md)).
PipeCD makes the **rollout strategy part of the deployment definition itself**. Fewer moving parts;
less composability.

## When to use it

- You deploy to **Kubernetes and non-Kubernetes targets together** — Terraform, Lambda, Cloud Run,
  ECS — and want one delivery model rather than one per platform. This is its strongest case and
  the one Flux and Argo CD genuinely do not cover
- You want **canary and analysis without installing a second controller**
- A single control plane with a deployment-centric UI across many clusters and many platforms
- Greenfield delivery with no existing GitOps investment, where the multi-platform story is
  worth more than ecosystem size

## When not to use it

- **You already run Flux or Argo CD.** They solve the same problem, and the ecosystem, tooling and
  hiring pool around them are far larger. Running two reconcilers is worse than either
- Kubernetes-only estates. The multi-platform advantage — its main differentiator — evaporates,
  and what remains is a smaller-community alternative to two dominant tools
- You want CI. PipeCD does not build or test anything; it deploys what already exists
- You need the largest possible ecosystem of integrations, plugins and community answers. PipeCD
  is a CNCF incubating project with a real but comparatively small community

## Notes

<https://github.com/pipe-cd/pipecd> — the single recorded link. Nothing is deployed in this folder;
PipeCD is **mapped as an alternative**, not installed.

The reason it is worth keeping visible even unused: **PipeCD is the only tool in `cicd/` that is
genuinely pull-based CD.** Everything else here either does CI, or does CD by pushing from a
pipeline that holds cluster credentials. That places PipeCD on the same side of the line as Flux —
which is precisely why it is not adopted here.

**This platform already made that decision.** Flux is the reconciler, documented in
[`platform-engineering/gitops/`](../../../platform-engineering/gitops/README.md), and every
`helm/helmrelease.yaml` in this repository is an instance of it. PipeCD is not a complement to
Flux, it is a replacement for it, and running both would mean two controllers competing to own the
same cluster state.

The one condition under which revisiting it would be rational is specific and worth writing down:
**if delivery ever has to span Kubernetes and non-Kubernetes targets** — Terraform, Lambda, ECS,
Cloud Run — under a single model with progressive rollout, PipeCD covers that in one tool where
Flux plus Flagger plus a separate Terraform pipeline covers it in three. Absent that, the choice is
already made and PipeCD stays a mapped alternative.

Given it is filed under `cicd/`, the classification is worth stating plainly: **PipeCD does not
belong to the CI half of this folder at all.** It sits next to `gitops/` conceptually, and is
documented here only because that is where it was recorded.

---

[← CI/CD](../README.md)
