# ADR
 
## Status
Accepted
 
## Context
Terraform changes applied manually or without strict review can corrupt state, introduce security risk, and create non-auditable infrastructure changes.
 
Key drivers:
- Terraform has high blast radius and requires strong change control.
- State backends can be corrupted by concurrent or ad-hoc execution.
- Cost governance depends on consistent tagging and repeatable processes.
- Production changes must be traceable to an approval process.
 
## Decision
Adopt a standardized GitHub Actions pipeline with:
- plan-on-PR
- apply-on-merge using the reviewed plan artifact
- strict state isolation
- concurrency controls
- least-privilege role separation (state vs provisioning)
 
## Consequences
- More consistent and auditable infrastructure changes.
- Additional CI/CD complexity (artifact integrity, role separation).
- Requires repo structure and tagging conventions.
- Manual/local applies become exceptional (break-glass) and require explicit approval + auditing.
