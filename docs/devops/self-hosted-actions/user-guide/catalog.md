# Catalog

## What This Provides
A self-hosted execution environment for GitHub Actions workflows that need private network access and secure execution inside Kubernetes.

## Who Should Use It
- Teams whose workflows require access to internal services via private endpoints.
- Teams running sensitive automation tasks that should remain inside the private network.

## How to Consume
- Configure workflow `runs-on` labels to target the self-hosted runners.
- Use the approved custom runner image where applicable.
- Follow standards for secrets and permissions.

## Limitations
- Not intended for all workflows by default.
- Capacity depends on the configured Scale Set limits and cluster resources.
