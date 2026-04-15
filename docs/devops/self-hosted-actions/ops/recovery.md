# Recovery

## Scope
Disaster recovery guidance for restoring self-hosted runner functionality.

## Failure Scenarios
- ARC controller failure
- Runner Scale Set misconfiguration
- Cluster outage or namespace deletion
- Broken runner image preventing pod startup

## Recovery Plan
- Restore Kubernetes manifests for ARC and Scale Sets from Git.
- Restore required secrets/configuration for runner registration.
- Re-deploy ARC controller.
- Re-deploy runner Scale Sets.
- Validate runners appear online in GitHub.
- Execute a smoke workflow to confirm internal private endpoint connectivity.

## Data Considerations
- Runners should be treated as ephemeral.
- Workflow artifacts should rely on GitHub storage or designated artifact storage, not runner local storage.
