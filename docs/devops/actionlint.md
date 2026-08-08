# Static Validation of GitHub Actions Workflows with actionlint

## Problem:
- Runtime-Only Feedback: Workflow files are the only code with no compile step. A typo in an expression, an invalid `needs:` reference, or a wrong runner label is only discovered after a push, burning CI minutes and blocking merges for a mistake that was visible statically.

- Unchecked Shell Code: The `run:` blocks are shell scripts embedded in YAML, and no YAML linter looks inside them. Unquoted variables, unset references, and broken conditionals ship straight to the runner.

- Silent Expression Errors: `${{ }}` expressions referencing a context that does not exist, matrix keys that were renamed, or deprecated commands such as `set-output` pass code review unnoticed because nothing validates them.

- Blast Radius of Centralized Workflows: With reusable workflows consumed by dozens of repositories, a single broken `workflow_call` signature breaks every consumer at once.

## Solution:
- Static Analysis of Workflow Syntax: Implemented actionlint to parse every file under `.github/workflows/` and validate job dependency graphs, matrix combinations, runner labels, event triggers, and `workflow_call` inputs before the workflow ever runs. It is a single static binary with no token and no API calls, so it cannot be rate limited and adds no secret to the pipeline.

- Expression and Context Checking: Validates `${{ }}` expressions against the contexts actually available at that point in the workflow, catching references to undefined secrets, inputs, and matrix keys that schema-based validators cannot see.

- Embedded Shell and Python Linting: Runs shellcheck over each `run:` block and pyflakes over inline Python. This is the capability that separates actionlint from alternatives such as action-validator and check-jsonschema, which validate only against the JSON Schema and never inspect the script.

- Shift-Left Enforcement: Installed as a pre-commit hook locally and as a CI job on every pull request touching `.github/`, introduced as non-blocking until the existing backlog of findings was cleared, then promoted to a required status check in the branch ruleset.

- Reviewer-Friendly Output: Combined with reviewdog, findings are posted as inline comments on the changed lines instead of being buried in job logs.

- Controlled Upgrades: New releases add checks, so a version bump can turn a green pipeline red without any workflow change. The version is pinned and bumped deliberately via Renovate rather than tracking latest. Self-hosted runner labels are declared in `.github/actionlint.yaml`, which is the main source of false positives when omitted.

## Skills:
- DevOps
- CI/CD

## Tools:
- actionlint
- Github Actions
- shellcheck
- pre-commit
- reviewdog
- Renovate
