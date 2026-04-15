# Reusable GitHub Actions Workflow Templates for for Multi-Repository CI/CD Projects

## Problem:
- Scattered Workflow Management: Workflows are spread across multiple repositories, leading to inconsistent CI/CD processes and duplicated code.

- Maintenance Overhead: Managing and updating workflows across various repositories increases operational complexity and effort.

- Lack of Standardization: Inconsistent usage of actions, naming conventions, and triggers make it difficult to enforce best practices and governance.

- Reduced Visibility and Control: Lack of a centralized approach makes monitoring, auditing, and improving workflows a challenging task.

## Solution:
- Workflow Template Repositories: Created centralized repositories containing reusable GitHub Actions workflows as templates. This approach allows individual projects to reference and reuse standardized workflows, improving consistency and reducing maintenance effort.

- Composite Actions: Developed composite actions to encapsulate commonly used CI/CD tasks, promoting code reuse and simplifying workflow definitions.

- Centralized Governance: Implemented rules and guidelines for creating, updating, and using workflows across repositories, ensuring adherence to security policies and best practices.

- Version Control for Workflows: Leveraged Git tags and versioning to maintain compatibility while providing the flexibility to update workflows when needed.

- Streamlined Maintenance: By centralizing workflows, updates and improvements can be made once and propagated automatically to all referencing projects, enhancing scalability and reducing operational overhead.

- Improved Visibility and Control: Introduced monitoring and logging mechanisms to enhance visibility into workflow execution and performance, allowing for better troubleshooting and optimization.

- Documentation & Training: Created detailed documentation on how to use, customize, and extend the centralized workflows, promoting consistent usage across teams.

- Security Enhancements: Ensured that all workflows comply with security guidelines, including token management, permission scopes, and access control.

## Skills:
- DevOps

## Tools:
- Github Actions
- Hadolint

## Docs

### Planning
- [Business Case](planning/business-case.md)
- [PoC](planning/poc.md)
- [RFC](planning/rfc.md)
- [Roadmap](planning/roadmap.md)
- [Tech Debt](planning/tech-debt.md)

### Tech
- [Project](tech/project.md)
- [ADR](tech/adr.md)

### Ops
- [Observability](ops/observability.md)
- [Playbook](ops/playbook.md)
- [Runbook](ops/runbook.md)
- [Upgrades](ops/upgrades.md)
- [Recovery](ops/recovery.md)

### User Guide
- [Policies](user-guide/policies.md)
- [Reference](user-guide/reference.md)
- [Catalog](user-guide/catalog.md)
- [FAQ](user-guide/faq.md)


GitHub Actions: Centralized and Standardized Workflows
1. Overview

This documentation describes the strategy for centralizing pipelines using GitHub Actions Reusable Workflows. The goal of this approach is to consolidate CI/CD logic into a single governed repository, allowing multiple data repositories to consume standardized processes for deployment, testing, and validation.
2. Motivation and Challenges

Managing individual .github/workflows files in every repository led to the following issues:

    Inconsistency: Different versions of deployment scripts (Airflow, DBT, Terraform) running across various projects.

    Maintenance Difficulty: A change in security policy or an ECR endpoint required manual updates across dozens of repositories.

    Shadow IT: Developers creating pipelines without mandatory security checks or failing to follow naming conventions.

    Audit Complexity: The inability to guarantee that all deployments passed the same quality gates.

3. Solution Architecture
3.1 Central Workflow Repository

All logic is centralized in the org/dataops-actions repository. It functions as a CI/CD "function library."

    Location: .github/workflows/

    Trigger: Utilizes the workflow_call event, allowing the receipt of inputs (parameters) and secrets.

3.2 Call Structure

Application repositories (e.g., data-pipeline-marketing) do not contain complex scripts. They simply "call" the centralized workflow, passing context-specific variables.

    Flow: Data Repository —(uses)—> org/dataops-actions —(executes on)—> DataOps Runner (EKS)

3.3 Branch-Based Consumption Strategy

To ensure agility and immediate parity across the organization, we reference workflows via branches instead of semantic tags:

    main branch: Stable version used for all Production deployments.

    dev branch: Staging version used for Development/Sandbox deployments.

Reasons for this choice:

    Patch Agility: Critical fixes are instantly propagated to all repositories.

    Zero Toil: Eliminates the need to open hundreds of PRs just to update a tag version.

    Enforced Compliance: Ensures all teams are always using the latest security definition approved by the DataOps team.

4. Standardized Workflows Available
Workflow	Description	Mandatory Checks
deploy-airflow-dag.yml	Deploys Airflow DAGs via S3/GitSync.	Python Linter, Airflow Syntax Validation.
build-push-ecr.yml	Builds Docker images and uploads to ECR.	Vulnerability Scan (Trivy), Semantic Tagging.
terraform-plan-apply.yml	Executes Infrastructure-as-Code for data resources.	TFLint, Checkov (Security Scan).
5. Implementation Example (Consumer)

To deploy a new Airflow DAG following company standards, the .github/workflows/deploy.yml file in the local repository is simplified:
YAML

name: Deploy DAGs

on:
  push:
    branches: [main]

jobs:
  call-central-workflow:
    # Reference to the centralized workflow and its version (branch)
    uses: org/dataops-actions/.github/workflows/deploy-dags.yaml@main
    secrets: inherit

6. Governance Benefits

    Single Source of Truth: If the platform team decides to change a security scanning tool, the change is made in one place and reflects across the entire organization.

    Complexity Abstraction: Data developers focus on code (.py, .sql), while AWS authentication and environment configuration complexity are hidden within the reusable workflow.

7. Lifecycle and Versioning

To maintain speed without compromising production, the update flow follows this rite:

    Direct Development: Changes and improvements are committed/merged directly into the dev branch of the dataops-actions repository.

    Sample Validation: Once in dev, the DataOps team monitors executions in selected sample repositories (e.g., 2 or 3 active projects from different squads).

    Observation Period: The code remains in dev long enough to validate the changes in the sampled repositories.

    Promotion via PR: After successful sampling and observation, a Pull Request (PR) is opened from dev to main.

    Production Deployment: Merging into main instantly updates the production pipeline for the entire organization with the validated features or fixes.