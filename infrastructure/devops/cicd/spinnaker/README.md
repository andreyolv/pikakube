[← CI/CD](../README.md)

# Spinnaker

<https://github.com/spinnaker/spinnaker>

---

## The problem it solves

Spinnaker was built at Netflix to answer a question that was very hard in 2015: **how do you deploy
the same application safely across multiple clouds, with canaries and automated analysis, at scale,
through one control plane?**

Its answer was a deployment-orchestration platform:

| Capability | Detail |
|---|---|
| Multi-cloud deployment | AWS, GCP, Azure, and later Kubernetes, through one abstraction |
| Deployment strategies | red/black (blue/green), rolling red/black, canary — as first-class options |
| **Automated canary analysis** | Kayenta compares metrics between baseline and canary and decides, statistically |
| Pipeline orchestration | stages, manual judgement gates, fan-out across regions and accounts |
| Immutable server groups | the model that made cloud deployments reproducible |

**Automated canary analysis was the genuinely novel part** and it remains influential — the idea
that a rollout should be gated on a statistical comparison of metrics rather than on someone
watching a dashboard is now standard, and Spinnaker is where it came from.

The cost was equally distinctive: Spinnaker is roughly a dozen microservices — Deck, Gate, Orca,
Clouddriver, Front50, Rosco, Igor, Echo, Fiat, Kayenta — each needing configuration, storage and
upgrades. Halyard existed solely to manage that installation, which tells you how much there was.

## When to use it

Honestly: **there is essentially no case for adopting it today.** The remaining ones are narrow:

- An **existing Spinnaker installation** with real pipeline investment, where migration is a
  project and the platform is already operated by people who know it
- Genuine **multi-cloud deployment across VM-based estates** — not containers — where the
  server-group model is still the right abstraction and no Kubernetes-native tool applies
- You need Kayenta's canary analysis specifically, and the alternatives are not sufficient

## When not to use it

- **Greenfield, on Kubernetes.** The operational cost is enormous relative to what has replaced it
- A small team, or any team without dedicated platform capacity. A dozen microservices is not a
  side project
- You want GitOps. Spinnaker is push-based orchestration — the credentials problem described in
  [CI/CD §3](../README.md#3-the-credentials-consequence), at maximum scope: a system holding
  deployment rights to every cloud account
- You want CI. Spinnaker does not build; it orchestrates deployment of artifacts built elsewhere
- You want a project with momentum. Netflix's own investment declined, the community narrowed, and
  the concerns it owned have been split across tools that each do one of them better

## Notes

<https://github.com/spinnaker/spinnaker> — the single recorded link, the umbrella repository (the
actual services live in their own repositories, which is itself a signal of the architecture).

**What is deployed here: a namespace, and nothing else.** `namespace.yaml` creates `spinnaker`.
There is no HelmRelease, no source, no configuration. That is an accurate record of the evaluation
— the folder was created, the namespace was created, and installation stopped there.

**Spinnaker is past its peak, and the reasons are structural rather than a matter of taste.**

It solved multi-cloud deployment orchestration for a **pre-Kubernetes-operator world**, where
"deploy" meant creating immutable server groups of VMs across cloud APIs that had nothing in
common. That problem was real and hard, and Spinnaker's architecture — a service per concern,
a cloud driver abstracting the providers — was a reasonable response to it.

Kubernetes then absorbed most of that problem. Deployment became a controller reconciling a
declarative object, and the cloud-specific orchestration layer largely stopped being needed. What
was left of Spinnaker's value split into pieces that are each now a small, focused tool:

| Spinnaker concern | What owns it now |
|---|---|
| Getting the desired state into the cluster | Flux, Argo CD — [`gitops/`](../../../platform-engineering/gitops/README.md) |
| Canary, blue/green, automated analysis | [Flagger, Argo Rollouts](../../../site-reliability-engineering/progressive-delivery/README.md) |
| Promotion across environments with gates | [Kargo](../../../site-reliability-engineering/lifecycle-orchestration/kargo/README.md) |
| Pipeline orchestration | [GitHub Actions](../github-actions/README.md), [Argo Workflows](../argo-workflows/README.md) |

Each of those runs as one controller. Together they cost a fraction of Spinnaker's footprint, and
any of them can be replaced without touching the others. That is the whole argument, and it is the
same one that applies to [Jenkins X](../jenkins-x/README.md): **the composable stack got good
enough that the integrated platform's coupling stopped being worth its convenience.**

What is worth keeping from Spinnaker: **Kayenta's idea**. Automated canary analysis — a rollout
gated on a statistical comparison of metrics between baseline and canary — is the right model, and
it is what Flagger implements against Prometheus today at a tiny fraction of the operational cost.
Spinnaker's contribution outlived Spinnaker.

---

[← CI/CD](../README.md)
