# Business Case

## Problem
Terraform is a high-leverage capability: small changes can provision, modify, or destroy critical infrastructure. When Terraform execution is manual and inconsistent across repositories, teams face slower delivery and elevated operational risk.

The main pain points are:
- **State conflicts and drift** caused by concurrent applies, shared state layouts, and out-of-band changes.
- **Unreviewed or non-audited changes** executed from local machines without consistent approval controls.
- **Inconsistent repo structure and tagging**, which reduces cost traceability and governance.
- **Security exposure**, when automation relies on broadly-scoped credentials instead of least-privilege roles.

These issues manifest as delivery bottlenecks, emergency rollbacks, and increased incident probability.

## Value
- **Delivery speed and reliability**
  - Predictable, repeatable infrastructure changes across repos.
  - Fewer “snowflake” pipelines and less time re-implementing CI/CD patterns.
- **Governance and auditability**
  - Plan-on-PR makes the change visible and reviewable.
  - Apply-on-merge ensures production changes are tied to an approved PR.
- **State safety and reduced failure modes**
  - Backend standardization + isolation reduces lock contention and state corruption.
  - Concurrency controls prevent overlapping runs that produce inconsistent outcomes.
- **Security improvements**
  - Role separation (state vs provisioning) and scoped permissions reduce blast radius.
  - Enables stronger controls with environments/approvals.
- **Cost and ownership clarity**
  - Enforced tags (team, project) increase cost attribution quality.

## Expected Outcomes
- **Standard pipeline across repositories**
  - A repeatable workflow (fmt/validate/plan on PR, apply on merge) that can be adopted broadly.
- **Higher integrity deploys**
  - Reviewed plans are applied consistently (avoid “plan drift” between PR and merge).
- **Reduced operational incidents**
  - Fewer state conflicts/locks and fewer emergency fixes caused by manual applies.
- **Faster onboarding**
  - New IaC repos can ship with a ready baseline (structure, backend, tagging, approvals).

## Stakeholders
- Platform/Cloud engineering
- DevOps/SRE
- Security
- Application teams owning Terraform repositories
- FinOps (tagging / cost attribution)

## Options Considered
- Keep manual execution + best-effort guidelines
- Provide a shared pipeline template but allow local applies
- Standardize CI/CD with strict apply-on-merge and environment approvals

## Risks and Mitigations
- **Initial migration effort**
  - Mitigation: incremental rollout (pilot repos, then expand) and reusable templates.
- **False sense of safety if guardrails are not enforced**
  - Mitigation: branch protections, required reviews, environment approvals, and least-privilege roles.
- **Pipeline failures blocking delivery**
  - Mitigation: runbooks, clear ownership, and staged rollouts for workflow changes.

## Success Criteria
- Most Terraform repos adopt the standard pipeline.
- Fewer incidents related to state conflicts and manual applies.
- Improved auditability: every apply traceable to a reviewed PR.
- Consistent tagging coverage for cost attribution.
