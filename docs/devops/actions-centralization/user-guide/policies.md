# Policies

## Versioning
- Consumers must pin to a tag or SHA.
- Consumers must not reference floating branches.
- Upgrades must be intentional (version bump + review).

## Permissions
- Use least-privilege `permissions:` blocks.
- Secrets must be explicitly passed.
- Workflows must not request broad default permissions.

## Governance
- Changes require review and release notes.
- Breaking changes require an explicit compatibility policy and upgrade guidance.
