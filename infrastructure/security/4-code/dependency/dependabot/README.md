[← Dependency updates](../README.md)

# Dependabot

<https://github.com/dependabot/dependabot-core>

---

## The problem it solves

Dependabot is GitHub's built-in dependency updater. Its argument is entirely about friction: a
`.github/dependabot.yml` file with a handful of lines, no service to run, no token to manage, no
infrastructure. It opens pull requests when new versions appear, and it is wired directly into
GitHub's advisory database so **security updates** are raised automatically for vulnerable
dependencies without any configuration at all.

It has three distinct modes, and conflating them causes confusion:

| Mode | What it does | Configuration |
|---|---|---|
| **Dependabot alerts** | flags vulnerable dependencies in the security tab | on by default for public repositories |
| **Dependabot security updates** | opens PRs for those vulnerabilities only | one toggle |
| **Dependabot version updates** | opens PRs to keep everything current | `.github/dependabot.yml` |

The first two are genuinely close to free and worth enabling on any GitHub repository regardless
of what else you use. The third is where it competes with [Renovate](../renovate/README.md), and
where the limitations below apply.

Grouping (`groups:`) and scheduling exist, and both have improved. They remain less flexible than
Renovate's, but the gap on plain application ecosystems — npm, pip, Maven, Go modules, Bundler,
Cargo — is narrower than it used to be.

## When to use it

- **Application repositories on GitHub with mainstream ecosystems**, where you want dependency
  updates without operating anything
- **Security alerts and security updates, everywhere.** Even on repositories using Renovate for
  version updates, Dependabot's alerts cost nothing and surface in GitHub's security tab
- **Small teams with no appetite for configuration.** A ten-line YAML file against Renovate's
  configuration surface is a real difference
- **When GitHub's integration is the point** — alerts, the dependency graph and the advisory
  database in one place, with no external service holding a token to your repositories

## When not to use it

- **GitOps and platform repositories.** This is the decisive case for this repository, and the
  specific reasons are recorded below with issue links. Flux `HelmRelease` chart versions,
  Terraform core versions, private Terraform modules and IAM-authenticated registries are all
  things a platform repository is made of, and all things Dependabot does not handle
- **When you need fine control over grouping, scheduling, automerge or stability delays.**
  Renovate's `packageRules` have no equivalent
- **When updates must cover files no package manager owns** — a version pinned in a Makefile, a
  README, a devbox definition. Renovate's regex managers or
  [`../updatecli/README.md`](../updatecli/README.md) cover this; Dependabot does not
- **Outside GitHub.** `dependabot-core` is open source and can be run standalone, but the
  experience is built around GitHub

## Notes

Every original note recorded for this tool, translated, with what it means. These are field
findings, and together they are the reason Renovate is used in this repository rather than
Dependabot.

### The project

- <https://github.com/dependabot/dependabot-core> — the open-source engine behind the hosted
  GitHub feature. Each ecosystem is a separate updater in this repository, which is why support
  is uneven: what works well is what someone maintained. It is also where every issue below is
  filed, so it is the place to check whether any of them have since been resolved.

### Self-hosted runners

- <https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-on-self-hosted-runners>
  — GitHub's documentation for running Dependabot jobs on **self-hosted runners** rather than
  GitHub-hosted ones. This matters when dependencies live behind a VPN or in a private network:
  by default Dependabot runs on GitHub's infrastructure, which cannot reach an internal artefact
  repository. Relevant here because this repository's own Renovate workflow already runs on a
  self-hosted runner (`dataops-actions-runner`).

### It does not work with Flux HelmReleases

> *"does not work for Flux's HelmRelease"*

- <https://github.com/dependabot/dependabot-core/issues/1744>
- <https://github.com/dependabot/dependabot-core/issues/12482>

**What this means:** a Flux `HelmRelease` pins the chart version in
`spec.chart.spec.version`. That is an ordinary field in a Kubernetes custom resource, not a
package manifest Dependabot recognises, so chart versions are simply never updated. For a GitOps
repository this is close to fatal — **the chart versions are the dependencies.** The two issues
are the long-running requests for Helm and Flux support; the second being recent indicates the
gap is still open rather than historical.

Renovate, by contrast, ships a dedicated `flux` manager that understands `HelmRelease`,
`HelmRepository` and `OCIRepository` resources.

### It does not update the Terraform version, only providers

> *"does not work for updating the Terraform version, nor the `.terraform-version` file. It only
> updates providers"*

- <https://github.com/dependabot/dependabot-core/issues/5797>
- <https://github.com/dependabot/dependabot-core/issues/8725>

**What this means:** Dependabot's Terraform support covers **providers and modules**, but not the
Terraform binary itself — neither the `required_version` constraint in the `terraform {}` block
nor the `.terraform-version` file used by `tfenv` and `tfswitch`. So the thing most likely to
cause a drift incident across an estate — different engineers and different CI runners on
different Terraform versions — is exactly what it will not keep in step.

Renovate has both: a `terraform-version` manager and support for `required_version` constraints.

### Private Terraform modules require a personal access token

> *"private Terraform modules only work with a PAT — absolute rubbish"*

- <https://github.com/dependabot/dependabot-core/issues/3723>

**What this means:** to update a module sourced from a private Git repository, Dependabot needs
credentials, and the supported route is a **personal access token** stored as a Dependabot
secret. That is bad for reasons that are structural rather than stylistic:

- a PAT carries the access of a *person*, not of a service — usually far more than the job needs
- it dies when that person leaves, breaking updates for reasons nobody connects to the departure
- it is a long-lived static credential in a system that already supports GitHub App
  authentication for everything else

The strength of the recorded opinion is proportionate: in 2025, requiring a human's token for a
machine task is a design failure, not a missing feature.

### No IAM role support for ECR

> *"does not support an IAM role for ECR, only static credentials — completely ridiculous"*

- <https://github.com/dependabot/dependabot-core/issues/6152>
- <https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-private-registries>
- <https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-access-to-private-registries>

**What this means:** to read image tags from a private ECR registry, Dependabot wants an AWS
access key and secret key stored as Dependabot secrets. It will not assume an IAM role, and it
does not use OIDC federation — despite GitHub Actions having supported OIDC-to-AWS for years,
which is precisely the mechanism that removes static AWS credentials from CI.

The consequence is that using Dependabot with ECR means creating and rotating a static IAM user
credential. That is the exact practice every cloud security baseline tells you to eliminate, and
it is why the note calls it ridiculous. The two documentation links are the official
configuration references — read them to confirm the supported credential types, which is where
the limitation is visible.

For contrast, this repository already uses **EKS Pod Identity** for Trivy's registry access, with
no static credentials anywhere — see
[`../../../3-container/scan/trivy/crossplane/README.md`](../../../3-container/scan/trivy/crossplane/README.md).

### The pattern in all of it

Read together, the five findings are not a list of unrelated bugs. They describe a tool built for
**application repositories on GitHub**, which works well there and degrades sharply outside that
shape. A platform repository — Flux, Terraform, private modules, cloud registries — is entirely
outside it. That is a legitimate scoping decision by GitHub, and it is also a complete answer to
"why not just use Dependabot, it is free".

---

[← Dependency updates](../README.md)
