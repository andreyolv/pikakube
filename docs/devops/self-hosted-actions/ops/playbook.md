# Playbook

## Scope
Emergency response guidance for failures affecting CI/CD workflows running on self-hosted runners.

## Symptoms and Actions

### Jobs Stuck in Queue
- Confirm GitHub is routing jobs to the expected runner labels.
- Confirm runners are `Online`.
- Check if Scale Set is at max capacity.
- Check Kubernetes cluster capacity (nodes, quotas).

### Runners Offline / Not Registering
- Check ARC controller health.
- Check network connectivity to GitHub endpoints.
- Check runner pod logs for registration/auth errors.

### Workflows Fail to Reach Internal Services
- Confirm pod network policies and DNS are correct.
- Confirm the internal private endpoint is reachable from the runner namespace.
- Validate there is no unintended egress path forcing traffic outside the private network.

### High Failure Rate After Image Update
- Roll back to the previous runner image version.
- Re-run a minimal “smoke workflow” to validate runner functionality.

## Escalation
- Platform/Kubernetes team for cluster capacity and network.
- Security team for credential exposure or policy violations.

