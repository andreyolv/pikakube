[← Internal developer platform](../README.md)

# OpenChoreo

<https://github.com/openchoreo/openchoreo>

---

## The problem it solves

Backstage gives you a portal and leaves the platform to you. OpenChoreo takes the opposite
position: it is an **opinionated internal developer platform** — an open-source distillation of
WSO2's Choreo — that ships the abstractions themselves. Components, environments, deployment
pipelines and promotion between environments are first-class resources, expressed as Kubernetes
CRDs rather than as things you assemble from Argo, Crossplane and a portal.

The pitch is that a platform team configures it once and application teams work in terms of
"promote this component from dev to staging" instead of in terms of YAML.

## When to use it

- You want a promotion model between environments without building one
- You are willing to adopt its component/environment abstraction wholesale
- The platform team is small and would rather configure than integrate

## When not to use it

- You already have a working GitOps flow — this replaces the model, it does not layer on top
- You need the abstraction to match an existing internal model; opinionated means non-negotiable
- Project maturity matters to you — it is young, and the ecosystem around it is thin
- You only need a catalog; that is [Backstage's](../backstage-chart/README.md) job and much less invasive

## Notes

The original note here was a single line — the GitHub URL and nothing else. That is the recorded
state of the evaluation, and it is worth keeping as such rather than dressing it up: **this is a
bookmark, not an assessment.** Nothing in this repository deploys it, and there is no chart, no
`HelmRelease`, no manifest.

Read the empty folder as the finding. An opinionated platform is the highest-commitment choice in
this discipline — it decides how every team ships — and committing to one on the strength of a
README is exactly the mistake this repository exists to avoid.

---

[← Internal developer platform](../README.md)
