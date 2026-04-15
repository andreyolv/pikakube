# RFC

## Summary
Centralize reusable GitHub Actions workflows and composite actions to standardize CI/CD across multiple repositories.

## Motivation
- Avoid duplicated workflow logic.
- Enforce conventions (naming, permissions, security hardening).
- Improve maintainability and visibility.

## Goals
- Consumers adopt a standard pipeline by referencing reusable workflows.
- Rollouts are controlled by version pinning.
- Security posture improves via consistent `permissions:` and secret handling.
- Workflow changes are auditable (reviewed, released, and communicated).

## Non-Goals
- Automatically forcing upgrades for all consumers.
- Supporting arbitrary “custom CI/CD” inside the workflow repo.

## Proposed Design
- Reusable workflows
  - Use `workflow_call` for invocation.
  - Consumers pass only required inputs/secrets.
  - Standardize `permissions:` and set safe defaults.
- Composite actions
  - Encapsulate repeated steps (lint, build, docker, security scan).
  - Keep them small and composable.
- Versioning
  - Consumers must pin by tag/SHA.
  - Releases must include a changelog and upgrade notes.
- Governance
  - Define ownership, review requirements, and a release process.
  - Use canary consumers before recommending broader upgrades.

## Open Questions
- Repo layout (single mono-repo vs per domain).
- Compatibility policy (semver vs date-based).
- Adoption process (migration strategy for existing repos).
- How to validate workflows behave as a contract (tests/linting for workflows).
