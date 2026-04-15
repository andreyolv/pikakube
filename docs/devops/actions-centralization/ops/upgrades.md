# Upgrades

## Approach
- Release changes as new tags.
- Validate with canary consumers.
- Roll out by consumer version bump.
- Prefer small, frequent releases over large, breaking changes.

## Pre-Upgrade Checklist
- Review release notes and required inputs/secrets.
- Upgrade a canary consumer first.
- Verify permissions remain least-privilege.

## Rollback
- Consumers revert to a previous tag/SHA.
