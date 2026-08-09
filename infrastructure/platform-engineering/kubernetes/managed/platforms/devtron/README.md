[← Platforms](../README.md)

# Devtron

<https://github.com/devtron-labs/devtron>

---

## The problem it solves

Devtron is a delivery platform: CI pipelines, CD pipelines with environment promotion, a GUI for
building Helm-based deployment configuration, RBAC over who may deploy what where, and cost and
security views on top. It installs into a cluster and becomes the way applications are built and
shipped.

The audience is teams who want the whole build-and-deploy path as a product rather than as an
assembly of GitHub Actions, Argo CD and a spreadsheet of which version is in which environment.

## When to use it

- You want CI and CD in one product, running inside the cluster
- Environment promotion with approvals is a requirement and nothing provides it today
- A UI for deployment configuration suits the team better than editing YAML
- No existing GitOps or CI investment to conflict with

## When not to use it

- You already run GitOps — Devtron wants to own deployment, and so does Flux
- Your CI is external and works; this replaces it rather than integrating with it
- Where the UI-driven configuration model conflicts with Git as the source of truth
- Open-core caution: check which features are in the free tier before designing around them

## Notes

**Chart** `devtron-operator` version `0.22.68` from `https://helm.devtron.ai`, with a namespace
manifest and empty values. Recorded as a link only.

Note the chart name: **`devtron-operator`**, not `devtron`. The chart installs an operator which then
installs and manages the platform's components. That indirection matters for two reasons — the values
you set are the operator's, not the platform's, and the platform's version is managed by the operator
rather than by the chart version. Looking for a Devtron configuration option in the chart's values
and not finding it is the predictable first hour.

**The overlap to resolve before installing.** Devtron includes its own CD, built on Argo CD, and its
own configuration model for deployments. This repository reconciles with Flux. Two GitOps engines in
one cluster is not a merge; it is a choice, and it has to be made deliberately rather than discovered
when both start reverting each other's changes.

**Footprint.** Devtron is a large installation — several databases, a queue, an object store, a
number of controllers, and Argo CD. It is closer to running an internal SaaS than to installing a
chart, and it needs monitoring and backup of its own state like anything else that holds the record
of what is deployed where.

Open core: the project is open source with a commercial enterprise edition. Which features sit on
which side changes over time; verify against the current documentation rather than against a blog
post.

---

[← Platforms](../README.md)
