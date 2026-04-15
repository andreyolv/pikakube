# PoC
 
 ## Goal
 Validate an end-to-end Terraform CI/CD flow that is safe, reproducible, and auditable:
 - `plan` on Pull Request
 - `apply` on merge
 - apply uses the exact reviewed plan artifact
 
 ## Scope
 - One repository using the standard structure (e.g. `/terraform` directory, env-specific tfvars).
 - Backend configured with isolated paths per repository/environment.
 - Concurrency controls enabled (no overlapping plans/applies per env).
 - Minimal permissions model (separate role for state operations vs provisioning).
 
 ## Out of Scope
 - Refactoring existing large Terraform codebases.
 - Multi-account/multi-region promotion model (covered later).
 - Full policy-as-code enforcement (can be validated as an extension).
 
 ## Prerequisites
 - Terraform backend exists (e.g. S3 + DynamoDB lock table) with per-environment isolation.
 - GitHub Actions runner has access to backend and target cloud via least-privilege roles.
 - A simple Terraform stack that can be safely created/destroyed in non-prod.
 
 ## PoC Steps
 - Create a PR that changes a safe resource (or a small module input).
 - Validate pipeline stages:
   - `terraform fmt -check`
   - `terraform validate`
   - `terraform plan` with consistent inputs
 - Persist the plan output as a protected artifact.
 - Merge PR and validate `apply` consumes the plan artifact (not a re-planned diff).
 - Run a second PR concurrently and confirm concurrency controls behave as expected.
 
 ## Test Cases
 - **Happy path**
   - A small change produces a plan and applies successfully after merge.
 - **Concurrent PRs**
   - Second PR is queued/blocked and does not race state.
 - **Backend lock contention**
   - Pipeline fails clearly with actionable error when a lock cannot be obtained.
 - **Permissions regression**
   - If provisioning role is removed, apply fails early and clearly.
 - **Plan integrity**
   - Artifact checksum/identity proves the applied plan equals the reviewed plan.
 
 ## Success Criteria
 - PR produces a deterministic plan given the same inputs.
 - Merge applies the exact reviewed plan artifact.
 - Concurrency rules prevent overlapping runs for the same environment.
 - Failures are actionable (clear errors for backend access, lock contention, permissions).
