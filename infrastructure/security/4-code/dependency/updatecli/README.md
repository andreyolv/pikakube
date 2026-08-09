[← Dependency updates](../README.md)

# Updatecli

<https://github.com/updatecli/updatecli>

---

## The problem it solves

Renovate and Dependabot update **dependencies**: things a package manager knows about. A
surprising amount of what goes stale in a repository is not a dependency at all:

- the Kubernetes version in a Terraform variable, a kubeadm config and a CI matrix — three places,
  one value
- a tool version pinned in a Makefile, a Dockerfile, a devcontainer and the README's installation
  instructions
- a chart's `appVersion` that should follow the upstream release it packages
- a base image digest referenced from a document rather than from a Dockerfile
- a value in repository B that must follow a value in repository A

None of these have a package manager, so no dependency bot will ever touch them. They drift, and
they drift silently.

Updatecli is a **general-purpose value synchronisation engine** built on three primitives:

| Primitive | Question |
|---|---|
| **Source** | where does the desired value come from? A GitHub release, a Docker tag, a Helm chart index, a file, an HTTP endpoint, a Git tag |
| **Condition** | should we proceed? Does the corresponding artefact actually exist yet |
| **Target** | where does the value need to be written? A YAML path, a JSON key, a regex match in any file, a Dockerfile `FROM` |

A manifest wires those together, and updatecli opens a pull request when the target does not match
the source. That model is deliberately more primitive than Renovate's, and that is the point:
anything you can describe as "this value should follow that value" is expressible.

## When to use it

- **Values no package manager owns.** The primary case, and there is no real alternative
- **The same version appearing in several places.** Updatecli makes one source of truth and
  several targets explicit, which is the only durable fix for that class of drift
- **Cross-repository synchronisation** — repository B tracking a value produced by repository A
- **Keeping documentation honest.** Installation instructions with a version number in them are
  wrong within a month; updatecli can update them from the same source that updates the code
- **Custom promotion flows.** Because source and target are arbitrary, "promote the version that
  passed staging into the production values file" is expressible

## When not to use it

- **As your dependency updater.** It has no curated vulnerability database, no advisory
  integration, no automatic detection of what your repository depends on, and no grouping across
  ecosystems. Renovate exists for that — [`../renovate/README.md`](../renovate/README.md)
- **When Renovate's regex managers already cover it.** Renovate's `customManagers` handle many of
  the "arbitrary file" cases within the tool you already run. Reach for updatecli when that is not
  enough, not before
- **When you will not maintain the manifests.** Every synchronisation is hand-written; there is no
  autodiscovery. Twenty manifests is twenty things to keep correct
- **For security updates.** It updates to whatever the source says is current. It has no concept
  of "this version fixes a vulnerability"

## Notes

Original note recorded for this tool:

- <https://github.com/updatecli/updatecli> — the upstream project. The repository documents the
  manifest format, the full list of resource plugins for sources, conditions and targets (GitHub
  releases, Docker registries, Helm chart indexes, Maven, npm, YAML, JSON, TOML, `shell`, and
  more), the `updatecli diff` / `apply` commands, and the autodiscovery feature which can generate
  manifests for some common cases.

Two points worth carrying:

- **It is complementary to Renovate, not competing.** The natural split is: Renovate for anything
  with a package manager, updatecli for the values that fall outside one. Running both is the
  intended pattern, and neither will touch the other's territory.
- **The manifest is code and should be reviewed as such.** A target expressed as a regex
  replacement across files is a small program with write access to the repository; a wrong pattern
  rewrites more than intended.

---

[← Dependency updates](../README.md)
