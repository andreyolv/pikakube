# Roadmap

## Milestones
- M1: Define standards
  - Repo structure conventions.
  - Tagging requirements (team, project, env).
  - Backend/state pathing conventions.
- M2: Implement baseline pipeline
  - PR: fmt/validate/plan.
  - Merge: apply gated by approvals.
  - Concurrency controls per environment.
- M3: Plan artifact integrity
  - Persist plan artifact from PR.
  - Apply uses reviewed artifact.
  - Clear traceability (link PR -> plan artifact -> apply run).
- M4: Guardrails
  - Policy checks (linting, tags, security scanning).
  - Environment approvals and branch protections.
  - Break-glass process definition.

## Definition of Done
- Standard pipeline is reusable across repos.
- Promotion between environments is documented and enforceable.
- Rollback procedures exist and are tested.
- Onboarding checklist exists for new repositories.
