[← Pipeline security](../README.md)

# zizmor

<https://github.com/zizmorcore/zizmor>

---

## The problem it solves

Workflow files are the most privileged programs in a repository — they hold the secrets, assume
the cloud roles and publish the artefacts — and they are reviewed less carefully than application
code, because they look like configuration.

zizmor is a static analyser for **GitHub Actions workflows**. It reads the YAML and reports the
known-dangerous patterns:

```bash
# audit every workflow in the repository
zizmor .github/workflows/
```

The audit categories map onto exactly the failure modes in [`../README.md`](../README.md):

| Audit | What it catches |
|---|---|
| **Template injection** | `${{ github.event.* }}` interpolated into a `run:` block — untrusted input becoming shell code |
| **Dangerous triggers** | `pull_request_target` used in ways that expose secrets to untrusted code |
| **Unpinned actions / impostor commits** | `uses:` by mutable tag or branch, and references that do not correspond to a real commit in the named repository |
| **Excessive permissions** | `permissions` absent or broader than needed, including `write-all` |
| **Credential persistence** | `actions/checkout` leaving the token in the local Git config, where later steps (and anything they run) can use it |
| **Artifact and cache poisoning** | artefacts or caches written in one context and consumed in a more privileged one |
| **Self-hosted runner exposure** | untrusted workflows reaching self-hosted runners |
| **Secret handling** | secrets passed where they are not needed |

The reason it matters more than a generic linter: **these are not style problems.** Template
injection is remote code execution in a system holding every secret the organisation has, and it
looks completely innocuous in review. A tool that flags it mechanically is the only reliable
defence, because the human check is "does this line look dangerous" and the answer is no.

It is fast, needs no build and no network, and runs as a CLI, a pre-commit hook or a GitHub
Action. Findings can be suppressed inline with a comment, so accepted cases are recorded next to
the code rather than in a separate file.

## When to use it

- **Any repository with GitHub Actions workflows.** The cost is one CI step and the findings are
  concrete
- **Before making a repository public.** A public repository means anyone can open a pull request,
  which turns every template-injection finding from theoretical into immediately exploitable
- **Where self-hosted runners are in use** — the exposure audits are directly relevant, and this
  repository uses one
- **On a repository that publishes anything** — images, packages, releases. Compromising the
  workflow means compromising everything it publishes afterwards
- **As a pre-commit hook**, so a dangerous pattern never reaches the default branch

## When not to use it

- **You do not use GitHub Actions.** It is GitHub-specific by design. GitLab CI, Jenkins and
  Tekton have their own equivalents; the *categories* of problem transfer, the tool does not
- **Expecting it to audit what the workflow does.** It analyses the workflow definition, not the
  scripts the workflow invokes. A `run:` block calling `deploy.sh` is opaque to it, and
  `deploy.sh` is where much of the actual behaviour lives
- **Expecting it to cover the runner or the secrets.** Runner hardening is
  `security/0-governance/runner-hardening/`; removing static credentials is
  [`../../secret-scanner/README.md`](../../secret-scanner/README.md) section 5. zizmor audits the
  definition, which is one layer of the three
- **As the only review of a workflow.** It catches known patterns; it cannot tell you the job
  should not have had that permission in the first place

## Notes

Original note recorded for this tool:

- <https://github.com/zizmorcore/zizmor> — the upstream project. Note the organisation:
  development moved to `zizmorcore` from the author's personal namespace, so older links redirect.
  The repository documents every audit rule with an explanation and a remediation, the
  configuration file (`zizmor.yml`) for ignoring specific rules per file, the inline
  `# zizmor: ignore[rule-id]` suppression comment, the online/offline modes (some audits, such as
  impostor-commit detection, need GitHub API access), and the SARIF output for GitHub code
  scanning.

Two points worth carrying:

- **The "impostor commit" audit is the unusual one** and it is worth understanding. A `uses:`
  reference pinned to a SHA looks safe, but a SHA can exist in a *fork* rather than in the
  upstream repository — pinning to it means running code that was never in the action you think
  you are using. Detecting that requires querying GitHub, which is why it only runs in online
  mode.
- **Run it against this repository's existing workflow.** `dependency/renovate/renovate.yaml`
  already follows the practices zizmor checks for — SHA-pinned actions, minimal `permissions`, a
  GitHub App token — so the first run should be quiet. That makes it a cheap step to add *now*,
  while the baseline is clean, rather than later when it produces a backlog.

---

[← Pipeline security](../README.md)
