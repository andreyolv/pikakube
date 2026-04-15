# Runbook

## Plan Failing
- Check formatting/validation.
  - `terraform fmt -check`
  - `terraform validate`
- Confirm backend access and workspace selection.
  - backend bucket/table exists
  - correct backend path for repo+env
- Confirm required variables are provided.
  - missing `TF_VAR_*` or tfvars inputs
- Confirm provider credentials are available.
  - role assumption/OIDC errors

## Apply Failing
- Confirm apply uses the reviewed plan artifact.
  - artifact exists and matches PR/commit
  - apply job is not re-running `plan` implicitly
- Check state lock and permissions.
  - lock table reachable
  - `AccessDenied` indicates policy regression
- Check for out-of-band changes causing drift.
  - re-run a plan to see unexpected diffs
  - identify manual changes and revert to Git state
- Check for breaking provider upgrades.
  - provider version constraints and lockfile

## Emergency Stop
- Disable applies temporarily (branch protection / environment rules).
- Re-run plan to re-baseline.
- Communicate freeze window and scope.
