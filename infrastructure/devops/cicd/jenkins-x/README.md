[← CI/CD](../README.md)

# Jenkins X

<https://github.com/jenkins-x/jx>

---

## The problem it solves

Jenkins X set out to answer a question that was genuinely open around 2018: *what does a complete,
opinionated CI/CD experience for Kubernetes look like, if you do not want to assemble it yourself?*

Its answer was a bundle, delivered through one CLI (`jx`):

| Piece | What it gave you |
|---|---|
| Pipelines | originally Jenkins, later rewritten around [Tekton](../tekton/README.md) |
| GitOps promotion | environments as Git repositories, promotion as a pull request |
| Preview environments | a temporary deployment per pull request, with a comment linking to it |
| Build packs | detect the language, generate the Dockerfile, chart and pipeline for you |
| Versioning | automatic semantic version bumps and changelogs from commits |
| Cluster bootstrap | `jx boot` — create the cluster and the whole platform in one command |

Two of those ideas were genuinely ahead of their time and are now mainstream: **promotion as a pull
request against an environment repository**, and **preview environments per PR**. If you want to
understand where the modern promotion model came from, this is a large part of the answer.

## When to use it

Honestly: **there is no strong case for adopting it today.** The situations where it still makes
sense are narrow:

- An **existing Jenkins X installation** that works and that the team understands. Migrating is a
  project with no immediate payoff
- You want the *whole* opinionated bundle — build packs, automatic versioning, preview
  environments, promotion — from one CLI, and you accept its conventions wholesale rather than
  choosing components
- As a **reference**, for how PR-based promotion and preview environments were first assembled

## When not to use it

- **Greenfield, in 2026.** Its constituent parts have been replaced by better, independently
  maintained tools, and assembling them is no longer the hard problem it was
- You want to choose your components. Jenkins X is opinionated by design; deviating from its
  conventions fights the tool
- You need a project with strong momentum. Development slowed substantially after the Tekton
  rewrite, and the community moved to Argo CD and Flux
- The name suggests it. Jenkins X is **not** a newer [Jenkins](../jenkins/README.md) — after the
  rewrite it does not even use Jenkins. The name is a source of genuine confusion and a bad reason
  to pick it

## Notes

<https://github.com/jenkins-x/jx> — the single recorded link, the CLI that is the whole entry
point to the product. Nothing is deployed in this folder: Jenkins X is **mapped as a historical
alternative**, not installed.

**Jenkins X is past its peak, and it is worth being direct about why**, because the reasons are
instructive rather than merely dismissive.

It attempted a **mid-life rewrite of its own engine**, moving from Jenkins to
[Tekton](../tekton/README.md). That is expensive under any circumstances: documentation, tutorials
and blog posts written for the earlier version stopped applying, and anyone evaluating it hit
conflicting material. Momentum did not survive it.

At the same time, its most valuable ideas were absorbed by tools that did **one thing each**:

| Jenkins X piece | What replaced it |
|---|---|
| GitOps promotion | Argo CD, Flux — see [`platform-engineering/gitops/`](../../../platform-engineering/gitops/README.md) |
| Environment promotion with gates | [Kargo](../../../site-reliability-engineering/lifecycle-orchestration/kargo/README.md) |
| Preview environments | vcluster, Argo CD ApplicationSets, and per-PR namespaces |
| Pipelines | [Tekton](../tekton/README.md) directly, or [GitHub Actions](../github-actions/README.md) |
| Progressive rollout | [Flagger and Argo Rollouts](../../../site-reliability-engineering/progressive-delivery/README.md) |

A user can now assemble that set from components that are each better maintained than the bundle
was, and each replaceable independently. That is the structural reason integrated CI/CD bundles
lost: **the composable stack got good enough that the bundle's main advantage — not having to
choose — stopped being worth its coupling.**

The same argument applies to [Spinnaker](../spinnaker/README.md), for the same reason and in the
same period.

What to actually take from Jenkins X, given it is not going to be installed: **promotion as a pull
request into an environment repository** is the correct model, and this repository already lives
that way through Flux. Jenkins X is where a lot of people first saw it.

---

[← CI/CD](../README.md)
