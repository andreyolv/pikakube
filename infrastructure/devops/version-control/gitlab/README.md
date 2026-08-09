[← Version control](../README.md)

# GitLab

<https://gitlab.com/gitlab-org/gitlab>
<https://gitlab.com/gitlab-org/cloud-native/gitlab-operator>
<https://github.com/gitlabhq/gitlabhq>

---

## The problem it solves

**A whole DevOps platform, of which the git forge is one component.** That framing is the point:
evaluating GitLab as a place to keep repositories misses both what it is for and what it costs.

| Area | What it includes |
|---|---|
| Forge | repositories, merge requests, issues, wiki, snippets |
| **CI/CD** | pipelines, runners, environments, deployments, review apps |
| **Registries** | container registry, package registries, Terraform state |
| **Security** | SAST, DAST, dependency scanning, container scanning, secret detection |
| Kubernetes | agent-based cluster integration, Auto DevOps |
| Planning | epics, boards, roadmaps, milestones, portfolio management |
| Compliance | approval rules, audit events, protected environments |

Everything shares one identity, one permission model and one audit trail, and that integration is
the genuine argument for it. The counter-argument is what it takes to run.

## When to use it

- when a **substantial part of the platform list above is actually wanted** — forge, CI, registry
  and scanning under one roof, with one set of permissions
- where an integrated compliance and audit story is a requirement
- where GitLab is already the organisational standard
- **as SaaS (gitlab.com)** — most of the benefit, none of the operational weight

## When not to use it

- **to store repositories.** [Gitea](../gitea/README.md) does that with a pod and a database
- where there is no team to own it: upgrades, database migrations, Gitaly, object storage and
  runner fleets are a continuing responsibility, not an installation
- on a small cluster — the resource requirements alone rule it out
- where the CI features are unused, which removes most of the reason to accept the weight

## Notes

There is no `doc.md` for this folder; what follows is recorded from the manifests.

**What GitLab self-hosted actually is.** Not one application:

| Component | Role |
|---|---|
| Webservice (Puma) | the Rails application |
| **Sidekiq** | background jobs — everything asynchronous |
| **Gitaly** | the git RPC service; the actual repository storage |
| **PostgreSQL** | all metadata |
| **Redis** | cache, queues, sessions |
| Object storage | uploads, artefacts, LFS, registry, backups |
| Container registry | if enabled |
| **Runners** | a separate fleet, if CI is used |
| Ingress, certificates, mail | the surrounding infrastructure |

Each is a thing to size, monitor, upgrade and back up. This is the "serious commitment" in
[§2 of the parent](../README.md#2-the-forges), stated concretely — and the reason the honest
default for GitLab is **use the SaaS**.

**What is configured here.** Not the GitLab chart directly, but the **Operator**:

- a Flux `HelmRelease` deploying the `gitlab-operator` chart at version **1.3.1** from GitLab's
  chart repository, into a `gitlab` namespace
- `example/gitlab.yaml`, a `GitLab` custom resource (`apps.gitlab.com/v1beta1`) showing the
  minimum instance definition:

```yaml
spec:
  chart:
    version: "X.Y.Z"   # from CHART_VERSIONS for the operator version
    values:
      global:
        hosts:   { domain: example.com }
        ingress: { configureCertmanager: true }
      certmanager-issuer:
        email: youremail@example.com
```

The operator pattern is the right choice here and worth understanding. GitLab's Helm chart is
enormous and upgrading it means coordinating database migrations across many components in the
correct order. The Operator encodes that knowledge: you declare a `GitLab` resource and it manages
the underlying chart, the upgrade sequence and the component lifecycle. The nested `chart.version`
inside the custom resource is exactly that indirection — the operator version and the GitLab chart
version are separate things, and the comment in the example points at GitLab's `CHART_VERSIONS`
file for the pairing that the installed operator supports. Choosing an unsupported pairing is the
usual first failure.

The two placeholders are the ones that must be real: `domain` must be a domain you control and
whose DNS points at the Ingress, and the cert-manager issuer `email` must be a real address —
Let's Encrypt rejects the ACME registration otherwise, and the symptom is a certificate that never
issues.

## Where it fits here

Mapped as the heavyweight self-hosted option in [`version-control/`](../README.md), and mapped
correctly via the Operator rather than the raw chart.

For this repository it is not proportionate: the requirement is a forge, and
[Gitea](../gitea/README.md) meets it at a fraction of the cost. GitLab earns its weight when the
CI, registry, scanning and compliance features are all in use — and when they are, the question in
[§3 of the parent](../README.md#3-self-hosted-or-saas) becomes the real one: **is there a team to
operate it, and has anyone tested a restore?**

---

[← Version control](../README.md)
