# Standardized Terraform CI/CD with GitHub Actions

## Problem:

- Inconsistent Deployments: Lack of a standardized structure for Terraform files and tags (team, project), leading to fragmented infrastructure and untraceable costs.
- State Vulnerability and Conflict: Manual terraform apply executions and shared tfstate files without environment isolation, causing state corruption and security risks.
- Uncontrolled Changes: Infrastructure changes being applied without a formal review process (Plan-on-PR) or using non-audited local environments.
- Race Conditions: Simultaneous Pull Requests generating inconsistent tf plan outputs, resulting in unpredictable and conflicting tf apply results.
- Security Risk: Using overly permissive IAM credentials for automation instead of scoped roles for state management and resource provisioning.

## Solution:

- Automated GitOps Pipeline: Implemented GitHub Actions workflows to execute terraform plan on PRs and terraform apply on Merges for Dev and Prd branches.
- Plan Integrity with Encrypted Artifacts: Configured the pipeline to pass the tfplan as a persistent, encrypted artifact from the PR stage to the Merge stage, ensuring the exact reviewed code is deployed.
- State Isolation and RBAC: Defined a standardized S3/DynamoDB backend pathing by repository/environment and implemented scoped IAM roles—one for state management and another for resource provisioning.
- Workspace and Tfvars Management: Utilized Terraform Workspaces to separate environments (Dev/Prd) using environment-specific tfvars files for consistent configuration.
- Concurrency Locking: Enforced GitHub Actions concurrency groups to prevent multiple simultaneous PRs from running Terraform workflows, eliminating state inconsistency.
- Directory and Tag Enforcement: Standardized the /terraform directory structure and mandated resource tagging (team, project) as a prerequisite for successful pipeline execution.
