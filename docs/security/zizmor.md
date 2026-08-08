# Static Application Security Testing for GitHub Actions Workflows with zizmor

## Problem:
- Unreviewed High-Value Code: CI/CD pipelines hold the most privileged credentials in the organization and are the least reviewed code in it. Application SAST covers the source tree and nothing covers `.github/workflows/`, even though a single defect there is a direct path to production secrets.

- Template Injection: Interpolating attacker-controlled fields such as `${{ github.event.pull_request.title }}` directly into a `run:` block executes that content as shell on the runner. The workflow is syntactically valid, so linters raise nothing.

- Dangerous Triggers: `pull_request_target` runs with repository secrets in scope. Combined with a checkout of the fork's code, it hands write-level credentials to anyone who opens a pull request.

- Over-Permissive Tokens: When `permissions:` is omitted, `GITHUB_TOKEN` inherits the repository default, frequently granting write access to contents, packages, and deployments that the job never needs.

- Mutable Third-Party Dependencies: `uses: some/action@v4` resolves to a tag the maintainer can move. A compromised upstream action executes arbitrary code with access to every secret passed to that job.

## Solution:
- Purpose-Built Static Analysis: Implemented zizmor to audit workflows and composite actions specifically for security defects, with dedicated checks for template injection, dangerous triggers, excessive permissions, credentials persisted in the workspace by `actions/checkout`, artifact poisoning, and untrusted code scheduled onto self-hosted runners.

- Integration with GitHub Advanced Security: Exported findings as SARIF and uploaded them to GitHub code scanning, so workflow vulnerabilities appear in the Security tab alongside application SAST results, with alert history and dismissal tracking, instead of living in a separate report nobody reads.

- Separation from Correctness Linting: Runs next to actionlint over the same files. actionlint answers whether the workflow is valid, zizmor answers whether it is safe. Neither substitutes for the other, and both are required checks.

- Detection Connected to Remediation: The most frequent finding, unpinned actions, is resolved at the source by the existing Renovate configuration through the `helpers:pinGitHubActionDigests` preset, which converts tag references to digests automatically.

- Staged Rollout: Started in report-only mode to baseline the findings, gated the build on high-confidence results first, and promoted to a required status check after the high-severity backlog was remediated. Legitimate exceptions are annotated inline with `# zizmor: ignore[rule]` plus a justification comment, which becomes the audit trail during security review.

- Standard Remediation Pattern: Injection findings are fixed by moving the untrusted value into an `env:` variable and referencing it as a quoted shell variable inside the script, removing the interpolation from the shell entirely.

## Skills:
- Security
- DevSecOps
- CI/CD

## Tools:
- zizmor
- Github Actions
- GitHub Advanced Security (SARIF)
- Renovate
- actionlint
