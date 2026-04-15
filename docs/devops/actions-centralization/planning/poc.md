# PoC

## Goal
Validate consumption of centralized workflow templates and/or composite actions from multiple repositories with safe versioning and least-privilege permissions.

## Scope
- One workflow repository providing reusable workflows.
- Two consumer repositories.
- One composite action (e.g., lint/build/test).
- Version pinning and an upgrade workflow (canary -> broader rollout).

## Prerequisites
- A GitHub organization or equivalent namespace.
- A repo that hosts reusable workflows (invoked via `workflow_call`).
- At least one consumer repo that already has a local workflow to be replaced.

## PoC Steps
- Publish a reusable workflow in the workflow repo (e.g., `ci.yml`).
- Publish a composite action for a common step (e.g., `lint` or `docker-build`).
- Update consumers to reference:
  - reusable workflow by tag/SHA
  - composite action by tag/SHA
- Validate `permissions:` and secret flow:
  - consumer defines what secrets/vars are passed
  - workflow repo does not assume access to secrets by default

## Test Cases
- Consumer pins to a tag and runs successfully.
- Update workflow repo and release a new tag:
  - canary consumer upgrades and validates
  - second consumer upgrades after approval
- Intentional breaking change is prevented or clearly communicated by release notes.
- Rollback path works by reverting the pinned tag.

## Success Criteria
- Consumers can reference pinned versions (tag/SHA).
- Updates can be rolled out safely (opt-in by version bump).
- Security permissions are minimal and consistent.
- Rollback is possible by reverting a tag without code duplication.
