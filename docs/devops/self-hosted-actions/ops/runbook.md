# Runbook

## Scope
Day-to-day operational procedures for self-hosted GitHub Actions runners deployed on Kubernetes using Actions Runner Controller (ARC) and Runner Scale Sets.

## Routine Checks
- Confirm runner pods are healthy and ready.
- Confirm runner registration is visible in GitHub.
- Confirm Scale Set can scale up/down.
- Confirm runner image pull succeeds and nodes have capacity.

## Common Procedures

### Validate Runner Availability
- Check Kubernetes runner pods for `Ready` status.
- Check GitHub UI to confirm runners are `Online`.

### Scale Capacity
- Adjust Scale Set configuration (min/max runners) according to demand.
- Validate new runner pods register successfully.

### Rotate/Update Runner Image
- Publish a new version of the custom runner image.
- Update the Scale Set / runner deployment to use the new image.
- Validate a test workflow completes successfully.

### Connectivity Validation (Private Endpoints)
- Run a controlled workflow/job that performs a minimal check against an internal service.
- Confirm traffic stays within the private network boundary.

## Permissions and Secrets
- Verify jobs use scoped credentials.
- Remove unused secrets and avoid long-lived credentials.

