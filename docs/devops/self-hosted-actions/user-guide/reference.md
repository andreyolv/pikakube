# Reference

## Purpose
Define guidance on when GitHub Actions workflows should run on self-hosted runners (Kubernetes) versus GitHub-hosted runners.

## Use Self-Hosted Runners When
- Workflows require access to internal services via private endpoints.
- Workflows execute sensitive operations that must remain inside a controlled network boundary.
- Compliance requirements mandate execution within the organization network.
- You need consistent tooling and faster execution by using a prebuilt runner image.
- You need predictable compute characteristics and Kubernetes-based autoscaling.

## Prefer GitHub-Hosted Runners When
- Workflows do not require private connectivity.
- You want minimal platform maintenance overhead.
- Jobs are short-lived, low-risk, and do not handle sensitive data.

## Anti-Patterns
- Using self-hosted runners as a default for all repositories without a security/network requirement.
- Installing large dependency stacks on every job instead of relying on a curated runner image.
- Allowing broad credentials on runners instead of scoped, short-lived access.
