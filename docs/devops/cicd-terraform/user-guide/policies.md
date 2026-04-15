# Policies

## Review
- Applies must only happen after PR review and approval.
- Protected environments must require explicit approvals (environment rules / branch protection).
- Changes that impact networking, IAM, or state backends should require senior review.

## State
- Backend must be isolated per repo/environment.
- State locking must be enabled.
- State paths must be deterministic and documented.
- Manual state edits are prohibited except break-glass with audit trail.

## Security
- Use scoped roles and least privilege.
- Avoid overly permissive credentials.
- Prefer short-lived identity (OIDC / assume-role) over long-lived secrets.
- Separate permissions for:
  - state operations (read/write state, locking)
  - provisioning (create/update/destroy resources)
