# RFC

## Summary
Introduce self-hosted GitHub Actions runners on Kubernetes inside the private network to securely execute CI/CD workflows that require private endpoint access and/or handle sensitive operations.

## Motivation
- GitHub-hosted runners are not suitable for workflows that must reach internal services via private endpoints.
- Security/compliance requirements require execution within controlled infrastructure.

## Proposed Design
- Deploy Actions Runner Controller (ARC).
- Use Runner Scale Sets for autoscaling.
- Provide a custom runner image with required dependencies.
- Define labels and governance to route workloads appropriately.

## Alternatives Considered
- Keep using GitHub-hosted runners: rejected due to private connectivity and compliance gaps.
- Dedicated VMs for runners: feasible, but less aligned with Kubernetes-native operations and autoscaling.

## Open Questions
- What is the required minimum/maximum runner capacity per repo/team?
- Which workflows are approved to run on self-hosted runners?
- What are the mandatory security controls for runner images and secrets?
