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

AWS Resource Tagging Standardization
1. Objective

The purpose of this standardization is to enable cost allocation across business units with precision and transparency.

    Coverage Target: Reach 95% of the total billed cost with valid tags.

    Relevance Weighting: We prioritize high-impact financial resources (Instances, Clusters, Databases). Low-cost or "noise" resources (e.g., firewall rules, cryptographic keys) do not have strict tagging requirements to avoid operational overhead.

    Handling the Residual (5%): Untagged costs or shared infrastructure costs (within the 5% margin) will either be:

        Absorbed by the Data Engineering team.

        Allocated proportionally among teams based on their identified consumption weight.

2. Formatting Standard: kebab-case

To ensure consistency across different cloud platforms and avoid duplicate categories caused by typos, we strictly adopt the kebab-case standard:
Rule	Correct Example	Incorrect Example
All lowercase	data-ops	DataOps
Hyphen as separator	customer-360	customer_360 or customer 360
Simple characters	lead-scoring-v2	lêad-scøring!
3. Standard Keys

These tags are mandatory for all resources generating significant costs (above $100 USD/month).
3.1. Key: team

Defines the technical team responsible for the resource and its associated cost. Values must be selected exclusively from the list below:

    data-engineering: Processing infrastructure (Spark, Glue), ETLs, and Data Lake.

    data-science: Experimentation environments, model training, and notebooks.

    data-analytics: Visualization tools, Data Warehouse, and consumption layers.

    dataops: Core data infrastructure services (e.g., Networking, EKS).

    mlops: Core data science platform services (e.g., SageMaker).

    martech: Marketing integrations, CDPs.

    tech: General tech services used within the data account (e.g., Redshift Clickbus Insights).

3.2. Key: project

Defines the specific initiative, product, or application. This tag is dynamic but must be short and descriptive.

    Project Examples: clickbus-insights, fipe, observo.

    To Do: A complete list of all possibilities needs to be formally defined.

4. Monitoring Dashboards

Use the links below to monitor billing health and tag compliance:

    📊 Costs and Resources by Team: Overview of spending and coverage percentage per team.

    ⚠️ Non-Compliant Resources: List of resources requiring manual correction or IaC updates.

5. Governance and Compliance

    Mandatory Requirement: Every resource created via Terraform, CloudFormation, or the AWS Console must contain, at a minimum, the team and project tags.

    Automation: Resources identified without mandatory tags will be subject to automated notification processes and, in the future, scheduled termination (in non-production environments).