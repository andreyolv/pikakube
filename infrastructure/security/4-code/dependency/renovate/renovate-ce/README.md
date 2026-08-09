[← Renovate](../README.md)

# Renovate CE

<https://github.com/mend/renovate-ce-ee>

Deployment: [`helm/`](helm/README.md)

---

## The problem it solves

Running Renovate as a CLI or a GitHub Action works well for a handful of repositories. Across an
organisation it starts to hurt: every repository needs its own scheduled workflow, there is no
central view of what ran or what failed, autodiscovery has to be scripted, and the credentials
granting write access to everything are duplicated into every workflow.

**Renovate CE (Community Edition)** is Mend's self-hosted Renovate **server**. It runs as a
persistent service, discovers repositories, maintains its own job queue and schedule, exposes an
admin API and a dashboard, and holds the platform credentials once.

| | Action / CLI | **Renovate CE server** |
|---|---|---|
| Scheduling | one workflow per repository | central, server-side |
| Repository discovery | listed or scripted | autodiscovery |
| Credentials | duplicated per repository | held once by the server |
| Visibility | scattered across workflow runs | one dashboard and API |
| Operational cost | none | a service, its storage and its upgrades |

CE is the free tier of Mend's commercial `renovate-ce-ee` product; **EE** is the paid tier, adding
scale, support and enterprise features. The same repository serves both, which is why the link is
to a Mend repository rather than to `renovatebot`.

## When to use it

- **Many repositories under one organisation**, where per-repository workflows have become the
  administrative problem
- **Self-hosted forge** — an internal GitLab, Bitbucket Server or Gitea — where a hosted service
  cannot reach the repositories anyway
- **Centralised credential handling.** One service account, one place, rather than the same token
  configured into dozens of workflows
- **You want a dashboard.** Knowing which repositories Renovate is actually processing, and where
  it is failing, is genuinely useful at scale and absent from the Action

## When not to use it

- **A handful of repositories.** The Action or the official `CronJob` chart does the same job with
  nothing to operate — see [`../README.md`](../README.md)
- **You have not read the CE tier limits.** CE is free but limited (notably in the number of
  repositories it will process); confirm the current limits before designing around it, because
  hitting the ceiling means either a commercial conversation or a migration
- **You want a Kubernetes-native, declarative shape.** Renovate CE is a server configured through
  environment variables and a config file, not through CRs. The operator is the alternative —
  [`../renovate-operator/README.md`](../renovate-operator/README.md)
- **Alongside another shape.** Running CE and the GitHub Action against the same repositories
  produces duplicate pull requests

## Notes

Original note recorded for this tool:

- <https://github.com/mend/renovate-ce-ee> — Mend's repository for both the Community and
  Enterprise editions. It holds the Helm charts, the container images, the configuration
  reference (environment variables and `config.js`) and the documentation of the differences
  between the CE and EE tiers. That last part is the one to read first, since it determines
  whether CE is viable for your repository count.

From the manifests committed here:

- The chart comes from <https://mend.github.io/renovate-ce-ee>, chart `mend-renovate-ce` version
  `46.217.1`, released as `renovate` into the `renovate` namespace.
- The values references kept in the file:
  <https://artifacthub.io/packages/helm/renovate/renovate> and
  <https://github.com/mend/renovate-ce-ee/blob/main/helm-charts/mend-renovate-ce/values.yaml>.
  Note the first of those points at the **official renovatebot chart**, which is a *different*
  chart from the one this release installs — a useful reference, but not the values file for this
  deployment. The second is the correct one.
- **No values are set**, so no platform credentials, no autodiscovery configuration and no
  Renovate configuration are supplied. As committed this deploys the server; it does not connect
  it to anything — see [`helm/README.md`](helm/README.md).

---

[← Renovate](../README.md)
