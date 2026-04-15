# Upgrades

## Scope
Guidance for upgrading Actions Runner Controller (ARC), runner images, and related Kubernetes resources.

## Upgrade Targets
- ARC (controller) version
- Runner Scale Set configuration
- Custom runner image version

## General Upgrade Approach
- Upgrade in a controlled environment first.
- Use a canary approach: update a subset of runners, validate workflows, then roll out broadly.

## Runner Image Upgrades
- Build and tag a new image.
- Validate required tools/dependencies.
- Run a smoke workflow before broad rollout.

## ARC Upgrades
- Review release notes for breaking changes.
- Apply changes during a maintenance window if necessary.
- Verify controller health and runner registration post-upgrade.

## Rollback Strategy
- Keep at least one previously known-good runner image tag.
- Maintain the ability to revert ARC manifests to a prior version.
