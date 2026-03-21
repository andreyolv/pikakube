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


automação e padronização de deploy de infra via terraform por github acitons
só adicionar arquivos terraform dentro da pasta terraform no repositório com padrão de arquivos pra garantir padronização de tags (team, project etc)
roles com permissões mínimas e especificas pra provisionar recursos ao time de engenharia e role especifica pra salvar tfstate
workspaces para deploy multi ambiente (dev e prd) baseado apenas em tfvars de cada ambiente
diretório do tf state padronizado e isolado por repositório e ambiente
abre PR pra branch dev -> tf plan no PR pra revisar
merge PR da branch main -> tf apply dev 
abre PR pra breanch prd -> tf plan no PR pra revisar 
merge PR pra branch main -> tf apply prd
travamento de concorrência de PR pra não ter mais de 1 PR aberto de terraform ao mesmo tempo e gerar inconsistência nos tf plans de PRs simultâneos
tf plan passa via artefato no github criptografado entre workflow do plan e workflow do apply pra garantir q o apply vai rodar o plan anterior exato e não gerar inconsistencia
