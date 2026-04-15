# Recovery

## Goal
Restore the ability to run safe Terraform plans and applies if automation or state access breaks.

## Steps
- Restore workflow configuration from Git.
  - revert to last known-good workflow tag/commit
- Restore backend access (S3/DynamoDB) and locks.
  - validate bucket/table policies
  - validate lock table exists and is reachable
- Run a plan to validate.
  - validate expected diff only
- Run a controlled apply in non-prod.
  - confirm end-to-end pipeline health before unfreezing production

## Fallback
Perform a manual plan/apply only with explicit approval and full audit trail until automation is restored.
