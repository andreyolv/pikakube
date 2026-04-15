# Roadmap

## Milestones
- M1: Define conventions
  - permissions baseline (`permissions:`)
  - naming and triggers
  - required inputs/secrets patterns
- M2: Publish baseline reusable workflows
  - CI (lint/test/build)
  - release pipeline (if applicable)
- M3: Publish composite actions and examples
  - common steps (lint, build, docker, scan)
  - example consumer repos
- M4: Migrate priority repositories
  - canary consumers
  - migration playbook and support

## Definition of Done
- Consumers use pinned versions.
- Upgrade path exists with minimal breaking changes.
- Operational monitoring and support process exists.
- A release process exists (tags + notes + rollback guidance).
