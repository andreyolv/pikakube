# GitHub Repository Standardization as Code with Terraform

## Problem:
- Configuration Drift Across Repositories: Repository settings applied through the GitHub UI diverge over time. Merge strategies, branch protections, required reviews and security features end up different in every repository, and nobody can state what the organization's standard actually is because it exists only as a habit.

- Manual and Unauditable Changes: Settings changed by hand leave no record of what was changed, by whom, or why. A protection rule relaxed "temporarily" to unblock a release stays relaxed, and the only way to notice is to open each repository and compare.

- Slow and Inconsistent Repository Onboarding: Creating a repository correctly means repeating a checklist of settings — visibility, rulesets, team permissions, labels, CODEOWNERS, security features, environments. Steps are skipped under time pressure, and the gaps are discovered during an audit rather than at creation.

- No Way to Scale Governance: Applying a new organizational requirement — a mandatory status check, secret scanning push protection, an approval rule — means editing every repository by hand, with no reliable way to confirm the change landed everywhere.

## Solution:
- Repositories as Declarative Infrastructure: Modeled GitHub repositories with the Terraform `integrations/github` provider, so repository settings, rulesets, permissions and security features are declared in code and reconciled by `terraform apply` instead of configured through the interface.

- Reusable Repository Module: Built a single Terraform module encoding the organizational standard — merge strategy, branch deletion on merge, default branch, issue labels, security settings — and instantiated it per repository from a declarative inventory. The standard is defined once; a repository declares only what makes it different.

- Branch Protection via Repository Rulesets: Expressed protection as GitHub Rulesets rather than the legacy branch protection API, covering required approvals, CODEOWNERS review, required status checks, linear history, and deletion and force-push blocking. Bypass actors are declared explicitly, so every exception to the policy is visible in a diff instead of hidden in a settings page.

- Security Baseline Enforced by Default: Enabled secret scanning with push protection, Dependabot security updates, vulnerability alerts and — where licensed — code scanning, as module defaults rather than per-repository decisions. Restricted GitHub Actions to an allowlist of permitted actions, closing the supply-chain path where any third-party action can run inside a repository holding credentials.

- Access Control by Team, Not by Person: Bound repository permissions to GitHub teams mapped from the identity provider, so joining or leaving a team grants and revokes repository access automatically and no individual collaborator grants accumulate.

- Standardized Governance Files: Managed `CODEOWNERS`, pull request templates and deployment environments as part of the same definition, keeping required reviewers and release gates consistent with the protection rules that depend on them.

- Adoption of Existing Repositories: Imported repositories created before the project into Terraform state, which converted an unknown inventory into a reviewed one — the first `plan` against the existing estate is itself the compliance report, listing exactly how far each repository had drifted from the standard.

- Plan on Pull Request, Apply on Merge: Delivered changes through a GitHub Actions pipeline that runs `fmt`, validation, linting and a plan on every pull request, and applies only after review on merge, with remote state and locking. Scheduled plans surface drift caused by manual changes, so a setting altered in the UI is reported rather than silently accepted.

## Skills:
- DevOps
- Platform Engineering
- Security

## Tools:
- Terraform
- Github
- Github Actions
- Github Advanced Security
