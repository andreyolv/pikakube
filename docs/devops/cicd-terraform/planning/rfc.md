# RFC
 
 ## Summary
 Standardize Terraform CI/CD using GitHub Actions with:
 - plan-on-PR (reviewable)
 - apply-on-merge (controlled)
 - plan artifact integrity (apply the reviewed plan)
 - strict state isolation and concurrency controls
 
 ## Motivation
 - Avoid unreviewed infrastructure changes.
 - Reduce state corruption and inconsistent deploys.
 - Make every apply traceable to an approved change.
 - Enforce repository conventions (structure, tags) for governance and cost attribution.
 
 ## Goals
 - Every Terraform change is executed in CI with consistent inputs.
 - Applies are gated by code review and approvals.
 - Backend/state is isolated per repository/environment.
 - Credentials are least-privilege and separated by responsibility.
 
 ## Non-Goals
 - Supporting ad-hoc local applies as a first-class workflow.
 - Solving all policy-as-code requirements in the first iteration.
 - Implementing a full release management framework for Terraform modules.
 
 ## Proposed Design
 - **PR workflow**
   - `terraform fmt -check`
   - `terraform validate`
   - `terraform plan` (with explicit backend config, workspace/tfvars, and consistent variables)
   - Persist plan as a protected artifact (encrypted at rest where applicable).
 - **Merge workflow**
   - Download plan artifact produced in the PR.
   - `terraform apply` using the artifact, preventing re-plans that can diverge.
 - **State isolation**
   - Standard backend paths per repository/environment.
   - Locking enabled (e.g. DynamoDB) to prevent concurrent state writes.
 - **Security model**
   - Separate roles:
     - state role: read/write state + locking table
     - provisioning role: create/update infra resources
 - **Concurrency controls**
   - GitHub Actions concurrency groups per repo+env to prevent overlapping runs.
 
 ## Assumptions
 - Environments are represented by explicit variables (workspace/tfvars) with stable naming.
 - Branch protection and required reviews exist for protected environments.
 - The pipeline runner can assume roles via a secure mechanism (avoid long-lived credentials).
 
 ## Open Questions
 - Artifact encryption strategy and key management.
 - Environment strategy:
   - separate branches
   - environments in GitHub Actions
   - directory-based environments
 - Policy enforcement integration (OPA/Conftest, Terraform policies, etc.).
 - How to handle emergency break-glass applies (process + audit requirements).
