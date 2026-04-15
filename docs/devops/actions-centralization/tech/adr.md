# ADR

## Status
Accepted

## Context
Duplicated workflows across repositories create drift, increase maintenance effort, and make governance/security enforcement difficult.

Key drivers:
- CI/CD changes must be rolled out safely without forcing all repos to upgrade at once.
- Security posture depends on consistent `permissions:` and secret handling.
- Operational efficiency improves when fixes are implemented once.

## Decision
Centralize reusable workflows and composite actions with strict versioning and governance so consumer repositories can adopt standardized CI/CD with controlled upgrades.

## Consequences
- Less duplication and faster standardization.
- Requires ownership and a release process for workflow repositories.
- Consumers must manage version bumps to receive updates.
- Canary consumers become important to prevent regressions.
