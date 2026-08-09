[← Dependency updates](../README.md)

# Renovate

<https://github.com/renovatebot/renovate>
<https://github.com/renovatebot/github-action>
<https://github.com/renovatebot/helm-charts>

Deployment shapes: [`renovate-ce/`](renovate-ce/README.md) ·
[`renovate-operator/`](renovate-operator/README.md)

---

## The problem it solves

Renovate is the dependency updater that assumes your repository is more than a `package.json`.
Two properties make it the default choice for a platform repository:

**1. It understands almost everything.** Ninety-plus package managers, plus the things that are
not package managers at all:

| Manager | What it updates |
|---|---|
| `flux` | `HelmRelease` chart versions, `HelmRepository`, `OCIRepository` — the exact gap that rules out Dependabot here |
| `helmv3`, `helm-values` | chart dependencies and image tags inside values |
| `docker`, `kubernetes` | image tags **and digests**, in manifests and Dockerfiles |
| `github-actions` | action versions, including re-pinning a SHA and updating the trailing version comment |
| `terraform`, `terraform-version` | providers, modules, **and the Terraform binary version** |
| `kustomize`, `docker-compose`, `devbox`, `pre-commit`, `nix`, … | the long tail |
| **`customManagers` (regex)** | any version string in any file, matched by a regular expression with a datasource attached |

The last row is the escape hatch that means "Renovate cannot update this" is almost never true.

**2. The configuration is expressive enough to control the noise.** Everything
[`../README.md`](../README.md) section 2 asks for is a first-class feature:

```json5
{
  "extends": ["config:recommended"],
  "schedule": ["before 6am on monday"],
  "prConcurrentLimit": 5,
  "minimumReleaseAge": "3 days",
  "packageRules": [
    { "matchUpdateTypes": ["patch", "digest"], "automerge": true },
    { "matchManagers": ["flux"], "groupName": "flux charts" }
  ],
  "vulnerabilityAlerts": { "schedule": ["at any time"], "minimumReleaseAge": null }
}
```

That last block is the one people miss: **security updates should bypass the schedule and the
stability delay**. Everything else waits for Monday; a vulnerability fix does not.

It is self-hostable in every shape — as a CLI, a GitHub Action, a scheduled container, a
server, or a Kubernetes operator — which matters because it means the tool holding write access
to all your repositories can be infrastructure you run.

## When to use it

- **GitOps and platform repositories.** Flux HelmReleases, image digests, pinned actions and
  Terraform versions are its native territory, and nothing else covers all of them
- **When the noise has to be controlled.** Grouping, scheduling, concurrency limits, automerge
  and stability delays are configuration rather than aspiration
- **Self-hosting is a requirement** — an internal GitLab, a private network, or a policy against
  granting a SaaS write access to every repository
- **Non-GitHub forges.** GitLab, Bitbucket, Gitea, Azure DevOps are all supported first-class
- **Monorepos and multi-repo estates**, where shared configuration presets (`extends`) let one
  policy govern many repositories

## When not to use it

- **A single simple application repository on GitHub** where Dependabot's ten-line config is
  enough. Renovate's power is configuration surface, and configuration surface is a cost
- **Without committing a configuration file.** Running with `config:recommended` and no
  packageRules on a real repository produces exactly the flood described in
  [`../README.md`](../README.md) section 2
- **With no test suite.** Automerge is what makes the volume manageable, and automerge without
  trustworthy CI automates breakage
- **More than one deployment shape at once.** The Action, the CE server and the operator all do
  the same job; running two against the same repositories means duplicate pull requests

## What is committed here

`renovate.yaml` — a GitHub Actions workflow that runs Renovate. Reading it as an example of the
surrounding work done properly:

| Line | Why it is right |
|---|---|
| `on: schedule: cron: '0 6 1 * *'` | monthly, not continuous — a batch someone owns |
| `permissions: contents: read` | least privilege at the workflow level; the App token supplies write access explicitly |
| `actions/create-github-app-token` | authenticates as a **GitHub App**, not as a personal access token. Scoped, rotatable, and it does not die when a person leaves — the exact failure recorded in [`../dependabot/README.md`](../dependabot/README.md) |
| every `uses:` pinned to a commit SHA, with `# vX.Y.Z` after it | a mutable tag on an action is a supply-chain hole; this is what [`../../pipeline/zizmor/README.md`](../../pipeline/zizmor/README.md) checks for. The trailing comment is also what lets Renovate update its own pins |
| `runs-on: dataops-actions-runner` | a self-hosted runner, so private networks are reachable |

What is **not** committed is the Renovate configuration itself (`renovate.json5` or
`.github/renovate.json`). Every noise control listed above lives in that file, so until it
exists the workflow will run with defaults. That is the next piece of work, and the reference
repositories in the notes below are what to copy from.

## Notes

Every original note recorded for this tool, with what each one is for.

### The project and its documentation

- <https://github.com/renovatebot/renovate> — the tool itself. Also the place to read the
  manager implementations when you need to know exactly what a manager detects.
- <https://docs.renovatebot.com/reading-list/> — the maintainers' own curated reading order
  through the documentation. Worth following rather than skimming: Renovate's documentation is
  large and the configuration options are only comprehensible in a particular sequence
  (presets → managers → datasources → packageRules). This link is the shortcut past that.

### Running it

- <https://github.com/renovatebot/github-action> — the official GitHub Action, which is what
  `renovate.yaml` in this folder uses.
- <https://github.com/marketplace/actions/renovate-bot-github-action> — the same Action's
  marketplace listing, which carries the usage documentation and input reference.
- <https://artifacthub.io/packages/helm/renovate/renovate> and
  <https://github.com/renovatebot/helm-charts> — the **official** Helm chart, which runs Renovate
  as a scheduled `CronJob` in the cluster. This is a fourth deployment shape, distinct from the
  two staged in the subfolders here: no server, no operator, just the CLI on a schedule. For a
  cluster that only needs to update a handful of repositories it is the simplest self-hosted
  option and is worth considering before either of the others.
- <https://github.com/mogenius/renovate-operator> — the community Kubernetes operator, documented
  in [`renovate-operator/README.md`](renovate-operator/README.md).

### Reference configurations from real repositories

These four links are working home-ops and homelab repositories, kept as examples because
Renovate's documentation explains options in isolation and these show a **complete, coherent
configuration** for exactly this kind of GitOps repository:

- <https://github.com/auricom/home-ops/tree/main/.github> — the whole `.github` directory,
  including the Renovate configuration and its supporting workflows.
- <https://github.com/auricom/home-ops/tree/main/.github/workflows> — the workflow set.
- <https://github.com/auricom/home-ops/blob/main/.github/workflows/renovate.yaml> — the specific
  workflow, which is the direct counterpart of the `renovate.yaml` in this folder. Comparing the
  two is the fastest way to see what is missing here.
- <https://github.com/bjw-s/home-ops/tree/main/.github> — a second, independently maintained
  example of the same pattern. Useful precisely because it differs.
- <https://github.com/brettinternet/homelab/blob/main/.github/renovate.json5> — **the
  configuration file**, in JSON5 with comments. This is the most valuable link in the list, since
  it is the artefact this repository does not yet have: real `packageRules`, grouping and
  automerge policy for a Flux-based repository.
- <https://github.com/brettinternet/homelab/blob/main/.github/workflows/schedule-renovate.yaml>
  — the scheduling workflow that drives it.

Why home-ops repositories specifically: they are Flux-based GitOps repositories maintained by one
or two people, which means their Renovate configuration has to be aggressive about automerge and
grouping or it becomes unmanageable. That constraint produces exactly the configuration a small
platform team needs.

---

[← Dependency updates](../README.md)
