[← Version control](../README.md)

# GitHub

<https://github.com/github/ruleset-recipes>
<https://github.com/github/docs>
<https://github.com/cli/cli>

---

## The problem it solves

**The forge with the largest ecosystem, operated by somebody else.** GitHub is where this
repository lives, and the practical argument for it is not features in isolation — it is that
everything integrates with it by default.

| Capability | Detail |
|---|---|
| **Actions** | CI/CD with a marketplace of pre-built steps, and hosted runners |
| **Rulesets** | branch and tag protection, applied at repository **or organisation** level |
| `CODEOWNERS` | required reviewers derived from the paths a pull request touches |
| **Advanced Security (GHAS)** | code scanning, secret scanning with push protection, dependency review |
| Packages | an OCI registry and package registries, tied to the same identity |
| Apps and webhooks | a real automation surface — see [`../git/`](../git/README.md) |
| Copilot | code completion, and **automatic pull request review** |
| OIDC to cloud providers | short-lived credentials in Actions instead of stored secrets |

The operational argument is the one in
[§3 of the parent](../README.md#3-self-hosted-or-saas): nobody here runs it, nobody upgrades it,
and nobody is woken up by it.

## When to use it

- **as the default**, unless there is a specific reason not to — code residency, cost at scale, or
  a policy requiring self-hosting
- when Actions removes the need to operate CI at all
- when organisation-wide policy must be enforced consistently across many repositories: rulesets
  do this properly
- **as the source of truth for a GitOps repository**, precisely because its availability is not
  yours to manage — see [§4 of the parent](../README.md#4-the-gitops-consequence)

## When not to use it

- where code may not leave the network
- where the forge must be under your operational control for compliance reasons
- where per-seat cost at scale changes the arithmetic — [Gitea](../gitea/README.md) is a pod and a
  database
- where a specific GHAS feature is required and the licence is not budgeted; several of the
  controls documented here depend on it

## Notes

Recorded link:

- <https://github.com/github/ruleset-recipes> — GitHub's own collection of example rulesets. The
  right starting point, because a ruleset is JSON that is tedious to write from scratch and easy
  to get subtly wrong.

Related links recorded in [`../git/`](../git/README.md), since they are GitHub-specific:
`cli/cli` (the `gh` CLI), `github/docs`, `PyGithub`, `probot`, `actions/labeler`,
`release-drafter`, `delete-merged-branch` and `github/gitignore`.

### The rulesets

Three exported rulesets are kept here, and together they are the most substantial content in this
folder. All three are real exports with identifiers and organisation references intact, which
makes them usable as templates rather than as documentation.

**`main.json`** — a **repository-level** ruleset protecting `refs/heads/main`:

| Rule | Effect |
|---|---|
| `deletion` | the branch cannot be deleted |
| `non_fast_forward` | no force pushes — history cannot be rewritten |
| `pull_request` | changes must go through a pull request |
| `require_code_owner_review: true` | the owners of the touched paths must approve |
| `required_approving_review_count: 0` | no *general* approval count is imposed |
| `allowed_merge_methods` | merge, squash and rebase all permitted |
| `bypass_actors` | one team, with `bypass_mode: always` |

The combination in rows four and five is the interesting one and reads as a mistake until you see
the intent: **zero required approvals, but code-owner review required**. The effect is that
approval is demanded from the people who own the code being changed, and from nobody else — a
review from an unrelated colleague does not unblock the merge. That is a sharper control than
"two approvals from anyone", and it depends entirely on `CODEOWNERS` being accurate.

The `bypass_actors` entry is the part to keep under review. A team that can always bypass is a
team for which the ruleset does not exist; that is a reasonable break-glass arrangement and a poor
default.

**`PR-Copilot-Review.json`** — an **organisation-level** ruleset (`source_type: Organization`,
source `pikakube`) targeting `refs/heads/main` and `refs/heads/release` across `~ALL`
repositories:

| Rule | Effect |
|---|---|
| `deletion`, `non_fast_forward` | the same baseline protections, everywhere |
| `pull_request` | required on both protected branches |
| **`automatic_copilot_code_review_enabled: true`** | Copilot reviews every pull request automatically |

The `~ALL` repository condition is what makes this different from `main.json`: it is a policy
applied once at the organisation and inherited by every repository, including ones created later.
That is the correct level for a baseline — per-repository rulesets drift, and new repositories
start unprotected.

Worth being clear about what automatic Copilot review is and is not: it is an additional reviewer
that comments, not an approver. `required_approving_review_count` is `0` here, so it does not gate
the merge. It catches the obvious and it is not a substitute for the human review that
`main.json`'s code-owner rule requires.

**`Protection-GHAS-B3.json`** — an organisation-level ruleset on `main` and `release` that adds a
`code_scanning` rule requiring code-scanning results before a merge. Its condition is the
mechanism worth stealing:

```json
"repository_property": {
  "include": [{
    "name": "Branch-Protection-SAST-Security-Level",
    "source": "custom",
    "property_values": ["B3"]
  }]
}
```

It targets repositories by **custom repository property**, not by name or pattern. A security
level is attached to a repository as metadata, and the ruleset follows automatically — so
classifying a new repository as `B3` applies the SAST requirement without anyone editing a
ruleset, and reclassifying it removes the requirement in one place. Compared with maintaining a
list of repository names, this scales and does not rot.

Note the dependency: `code_scanning` rules require **GitHub Advanced Security**. On a plan without
it, this ruleset cannot be applied.

### Pull request templates

- `.github/pull_request_template.md` — GitHub's **multi-template selector**. GitHub only supports
  one default template, so the trick is a default that links to the others with
  `?expand=1&template=<name>.md`:

  ```markdown
  - [Data Engineer](?expand=1&template=data_engineer_template.md)
  - [Data Science](?expand=1&template=data_science_template.md)
  ```

  The links only work from the **Preview** tab, which is why the template says so. Clumsy, and it
  is the only way to offer a choice of templates on GitHub.

- `.github/PULL_REQUEST_TEMPLATE/data_engineer_template.md` and `data_science_template.md` — the
  templates the selector points at. The directory name and location are fixed by GitHub;
  alternative templates are only discovered in `.github/PULL_REQUEST_TEMPLATE/`.

- `pr-template/1.md` and `pr-template/2.md` — two further templates, in Portuguese, kept as
  drafts. The first is a data-engineering checklist: **Descrição**, **Dependências Atreladas**
  (linked Jira card and issue), and a **Checklist** covering data validation against the business
  requirements, row counts, spot-checking sample records, column types and table schema, PR
  labelling, documentation updates in README and Confluence, and uploading the notebook used for
  testing. The second is a data-pipeline template with a Jira link, a **Tipo** section (new DAG,
  new task in an existing DAG, business rule change, bug fix, improvement, alerts), problem and
  solution descriptions, evidence of testing in DEV, and the QA execution result with linked PRs
  in the QA environment.

  Both are worth reading for what they enforce rather than their formatting: **evidence, not
  assertion**. "Validated the row count", "insert evidence of successful tests in DEV" — a
  reviewer of a data pipeline cannot verify correctness from the diff, so the template makes the
  author supply what the diff cannot show. That is the right instinct for any template.

### `repos.py`

A small script that pages through `https://api.github.com/user/starred` with a `GITHUB_TOKEN` from
the environment, collects each repository's URL and star count, and sorts the results — one list
alphabetically, one by stars. It is what produced the long link collections that this
documentation is built from.

Two details worth keeping: the token comes from an environment variable rather than the source,
and it pages at 100 per request, which is the API maximum. Unauthenticated requests to the same
endpoint are rate-limited to 60 an hour, which is why the token matters even for public data.

## Where it fits here

**The forge this repository actually uses**, and the only one in
[`version-control/`](../README.md) with real configuration rather than a deployment mapping.

Its role in the platform is larger than "where the code is": by
[§4 of the parent](../README.md#4-the-gitops-consequence), Flux reconciles from a `GitRepository`,
so GitHub is in the path of every reconciliation. That is the right trade — its availability is
professionally managed and not this cluster's problem — and it is still a dependency worth naming.
Two `HelmRelease`s in this repository, [Gitness](../gitness/README.md) and
[Kraken](../../image/p2p-mirror/kraken/README.md), also pull their charts directly from GitHub
repositories.

The self-hosted alternatives are mapped in [`../gitea/`](../gitea/README.md),
[`../gitlab/`](../gitlab/README.md), [`../gitness/`](../gitness/README.md) and
[`../gogs/`](../gogs/README.md) — and none of them is where this repository lives, which by
[§4 of the parent](../README.md#4-the-gitops-consequence) is the correct arrangement.

---

[← Version control](../README.md)
