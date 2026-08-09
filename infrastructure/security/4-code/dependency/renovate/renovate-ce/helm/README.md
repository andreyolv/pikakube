[← Renovate CE](../README.md)

# Renovate CE — Helm deployment

The Flux resources that install Mend's self-hosted Renovate server.

---

## What is here

| File | Resource | What it does |
|---|---|---|
| `helmrepository.yaml` | `HelmRepository` (`flux-system`) | registers `https://mend.github.io/renovate-ce-ee` as a chart source |
| `helmrelease.yaml` | `HelmRelease` named `renovate` | installs chart `mend-renovate-ce` version `46.217.1` into the `renovate` namespace, reconciled every 5 minutes |
| `../namespace.yaml` | `Namespace` | creates the `renovate` namespace |

No values are overridden — the `values:` block contains only the two reference comments.

## What is missing to make it work

A Renovate server with no configuration processes no repositories. At minimum this needs:

| Required | Why |
|---|---|
| **Platform credentials** — a GitHub App id and private key, or a token | the server cannot read or write repositories without them. These belong in a Secret, referenced by `valuesFrom`, never inline in the HelmRelease |
| **Autodiscovery or an explicit repository list** | otherwise the server has nothing to do |
| **A Renovate configuration** | grouping, scheduling, automerge and concurrency limits — everything in [`../../../README.md`](../../../README.md) section 2 |
| **Persistence** | the server keeps state; chart defaults should be checked against what you want to survive a restart |

The credential point is the one with security weight: this service holds **write access to every
repository it manages**. That makes it a high-value target, and it is the argument for a scoped
GitHub App over a personal access token — the same argument recorded against Dependabot in
[`../../../dependabot/README.md`](../../../dependabot/README.md).

## Notes

- The chart values references kept in the file:
  <https://artifacthub.io/packages/helm/renovate/renovate> and
  <https://github.com/mend/renovate-ce-ee/blob/main/helm-charts/mend-renovate-ce/values.yaml>.
  The first points at the **official renovatebot chart**, which is a different chart from the one
  installed here — worth knowing before someone copies values from the wrong reference.

- Three deployment shapes are staged in this tree: this server, the
  [operator](../../renovate-operator/README.md), and the GitHub Actions workflow described in
  [`../../README.md`](../../README.md). Only one should run against a given set of repositories.

---

[← Renovate CE](../README.md)
