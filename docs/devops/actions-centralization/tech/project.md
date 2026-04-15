# Project
 
 ## Overview
 A centralized set of reusable GitHub Actions workflows and composite actions used across multiple repositories to standardize CI/CD.
 
 ## Key Concepts
 - Reusable workflows invoked via `workflow_call`.
 - Composite actions for repeatable steps.
 - Pinned versions (tag/SHA) to control rollout.
 
 ## Boundaries
 - Workflow repository provides standardized building blocks.
 - Consumer repositories keep ownership of:
   - what inputs/secrets are passed
   - when to upgrade versions
   - repo-specific steps that are not generic
 
 ## Contract
 - Reusable workflows should behave like a stable API:
   - inputs are explicit and documented
   - outputs are stable
   - breaking changes require a major version bump (or equivalent policy)
 
 ## Security
 - Minimal permissions by default.
 - Explicit `permissions:` blocks.
 - Standardized token handling and secret usage.
 - Prefer OIDC/short-lived credentials when interacting with cloud providers.
 
 ## Versioning
 - Tags for stable releases.
 - Compatibility rules to avoid breaking consumers.
 - Canary consumers validate new tags before broad adoption.
