# Upgrades

## Approach
- Upgrade Terraform versions in staging first.
- Validate providers and state migrations.
  - run plan/apply on a representative repo
  - validate lockfile updates are intentional
- Roll out to production.
  - canary repos first
  - then expand rollout

## Pre-Upgrade Checklist
- Confirm current Terraform version and provider constraints.
- Confirm whether state migrations are expected.
- Confirm rollback plan exists.

## Rollback
- Revert workflow changes and Terraform version pin.
- If state migrations happened, follow Terraform state rollback procedures.
- If rollback is not possible, freeze applies and escalate.
