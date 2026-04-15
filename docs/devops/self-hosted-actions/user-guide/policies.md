# Policies

## Runner Selection
- Use self-hosted runners only for workflows that require private network access or handle sensitive operations.
- Prefer repository- or organization-scoped labels to route workloads to the correct runner group.

## Network
- Runners must run in a private cluster/network segment with access to internal private endpoints.
- Outbound access should be restricted to what is required for GitHub connectivity and dependency fetching.

## Identity and Access
- Apply least privilege for any runner service account and any cloud identities used by jobs.
- Prefer short-lived credentials over long-lived secrets.

## Images
- Use a curated custom runner image containing required tools/dependencies.
- The image should be versioned and rebuilt on a predictable cadence.
- The image must be scanned and built from trusted sources.

## Scaling and Availability
- Use Runner Scale Sets for autoscaling and availability.
- Define resource requests/limits for runner pods to avoid noisy-neighbor behavior.

## Operational Guardrails
- Centralize logs/metrics for runner workloads.
- Maintain a clear upgrade path for ARC and runner images.
