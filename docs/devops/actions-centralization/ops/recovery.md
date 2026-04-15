# Recovery

## Goal
Restore CI/CD execution if workflow repositories or a new release causes widespread failures.

## Steps
- Revert consumers to last known-good versions.
- Restore workflow repo availability.
  - ensure default branch and tags are accessible
- Publish a fixed version and communicate upgrade path.
  - hotfix tag
  - rollout guidance (canary first)
