# ADR

## Status
Accepted

## Context
Some CI/CD workflows require access to internal services that are only reachable through private endpoints. GitHub-hosted runners execute in public infrastructure and cannot reliably or securely access these internal resources. This also raises security and compliance concerns for workflows handling sensitive operations.

## Decision
Deploy self-hosted GitHub Actions runners inside the private network on Kubernetes using Actions Runner Controller (ARC) and Runner Scale Sets for autoscaling and availability. Use a custom Docker image for runner workloads to ensure consistent tooling and faster execution.

## Consequences
- Workflows that require private connectivity can run securely inside the private network.
- Runner capacity can scale based on demand.
- Maintenance responsibility increases (runner platform operations, upgrades, and incident response).
- The custom runner image becomes part of the supply chain and must be built, scanned, and maintained.
