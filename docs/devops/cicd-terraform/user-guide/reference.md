# Reference

## Golden Path
- Open PR
  - pipeline runs fmt/validate/plan
  - reviewers validate the plan output (what changes, where, and why)
- Merge
  - pipeline applies the reviewed plan artifact
  - apply output is recorded and traceable to the PR
- Rollback
  - revert the PR (or open a revert PR)
  - apply the revert via the same pipeline

## Recommended Conventions
- Standard `/terraform` directory structure.
- Mandatory tags (team, project).
- Concurrency groups enabled.
- Use environment tfvars (e.g. `dev.tfvars`, `prd.tfvars`) or a documented workspace strategy.
- Avoid high-risk changes bundled in one PR; prefer incremental diffs.
