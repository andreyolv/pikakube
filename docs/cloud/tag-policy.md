# Cloud Resource Tag Standardization and Governance

## Problem:
- No Cost Routing: Cloud costs cannot be accurately allocated to teams, projects, or products due to missing or inconsistent tags.
- Broken FinOps Practices: Budgets, alerts, and cost reports are unreliable without standardized cost-allocation tags.
- Shared Resource Blindness: Shared infrastructure costs cannot be fairly distributed across consuming teams.
- Uncontrolled Spend: Lack of tagging prevents early detection of cost anomalies and waste.
- Non-Enforced Standards: Tags are defined but not enforced during resource provisioning.

## Solution:
- Cost-First Tag Taxonomy: Defined mandatory cost-allocation tags (team, project, cost_center, environment) as a baseline.
- Provisioning-Time Enforcement: Blocked resource creation if required cost tags are missing or invalid.
- FinOps Integration: Enabled accurate chargeback/showback and budget tracking using standardized tags.
- Automated Cost Reporting: Generated cost views and reports grouped by tag dimensions.
- Drift Detection: Continuously detected and flagged resources that lost or changed required cost tags.
- Scalable Governance: Applied the same tagging and cost-routing model across all cloud accounts and environments.



chaves e valores seguindo padrão kebab-case

team = data-engineering, data-science, dataops, mlops, analytics, martech
env = us-east-1 é sempre produção e us-east-2 é sempre dev, então acho q não precisa essa tag, conseguimos gerar essa coluna de ambiente baseda na região
temos outras regiões ainda mas são exeções 

project = x, y, z etc

EKS não consegue propagar tags do EKS para ASG e VM do node group
https://github.com/aws/containers-roadmap/issues/374
https://github.com/aws/containers-roadmap/issues/608
