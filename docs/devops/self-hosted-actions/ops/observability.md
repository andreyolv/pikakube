# Observability

## Scope
What to monitor for the self-hosted runners platform.

## Key Signals
- Runner availability (online/offline)
- Queue time for jobs (time waiting for runner)
- Job success/failure rates on self-hosted runners
- Runner pod restarts and crash loops
- ARC controller health and reconciliation errors
- Cluster capacity and scheduling failures (insufficient CPU/memory)

## Dashboards
- Kubernetes: node/pod capacity and scheduling
- ARC: controller metrics/logs
- GitHub Actions: workflow queue time and runner utilization

## Alerting Recommendations
- No runners online for a given label/group
- Sustained high queue time
- ARC controller errors above baseline
- Runner pods failing to start (image pull, crash loop)
