RFC: Governance and Cost Allocation Strategy (FinOps)

Status: Draft

Author: Andrey Gustavo de Oliveira

Date: 03/10/2026

Impacted Areas: Data Engineering, Data Science, DataOps, MLOps, Analytics.
1. Abstract

This RFC proposes a cost allocation model for data infrastructure on AWS. The goal is to transition from a "global cost" model to a granular view by Team and Project, utilizing tags, namespaces, and log analysis.

graph TD
    subgraph Kubernetes
        direction LR
        Karpenter -->
        Spot_Instances[Spot Instances] 
        KEDA
        Kubecost
        Grafana[Grafana Resource Advisor]
        VPA[Vertical Pod Autoscaler]
    end

    subgraph AWS [AWS]
        direction LR
        AWS_Cost_Exporter[AWS Cost Exporter]
        Cloud_Reservations[Cloud Reservations]
    end


2. Motivation and Objectives

    Provide financial visibility to business units.

    Identify waste in shared buckets and Spark processing.

    Automate the allocation for services that do not support native per-project tagging (S3, Athena, EKS).

3. Governance and Standardization (Mandatory)

For cost allocation to be accurate, the infrastructure must follow strict identity and organizational standards.
A. Tagging Standards

Every resource (including Kubernetes Namespaces) must mandatory contain:

    team: martech, data-engineering, data-science, dataops, mlops, data-analytics.

    project: Standardized name according to the Project Dictionary.

B. Identity and Access (IAM Roles)

Each project must operate under an exclusive IAM Role with clear nomenclature:

    Pattern: [service-name]-[project-name]

    Example: airflow-churn-prediction

    This is fundamental for breaking down Athena and S3 costs.

C. QuickSight Organization

QuickSight Datasets must be grouped and named by project to allow traceability of Athena query consumption.
D. Athena Workgroups

Segregation of Athena Workgroups:

    New Projects/High-Cost Projects: Must have an exclusive Athena Workgroup. This ensures the cost is already separated in the AWS invoice by project.

    Migration: Existing projects identified as high-cost must be evaluated for immediate migration to a dedicated Workgroup.

    primary Workgroup: Will be maintained exclusively for QuickSight traffic, avoiding mass reconfiguration rework and allowing allocation via Dataset/Role within this group only.

    [!IMPORTANT]
    GOLDEN RULES (Cleanup Rules):

        Resources created without mandatory tags will have their costs distributed proportionally among all active projects.

        Executions via non-standard Roles and Users will follow the same proportional allocation rule, penalizing the lack of governance.

4. Cost Allocation Methodology
A. Allocation Options for S3 (Data Lake Buckets)

Storage and request costs for the Data Lake can be calculated in three ways:

    Option 1 (Proportional to Athena): Allocates total S3 Data Lake costs based on each project's Athena spending percentage.

    Option 2 (Proportional to Resource Mix): Allocates S3 costs based on the project's total weight in the account (Athena + K8s + EMR + Tagged Resources).

    Option 3 (Based on Actual Consumption - Recommended): Focused on shared buckets.

        Metric: Uses Access Logs to identify the volume of GET operations (the main cost driver).

        Logic: The total bucket invoice value is divided proportionally among projects based solely on the volume of GETs performed. This represents the bulk of the cost, corresponding to 80-85% of a bucket's total expense.

        Log Efficiency: Retention of only 1 day for raw logs. Processing consolidates figures into a separate bucket for historical data, optimizing log storage costs.

B. Compute (Kubernetes and EMR)

    K8s VMs (Kubecost): Total allocation via Namespaces, which must follow the team and project tagging standard.

    EMR on EKS: Mandatory segregation of clusters/jobs into project-specific Namespaces to ensure computational costs are isolated.

5. Cost Center Categorization
Category	Cost Composition
Core Infrastructure	All DataOps, MLOps costs, and resources with system tags (e.g., Kardan). Includes: Route53, ELB, EKS, EFS, VPC, Data Transfer, Config, SSM, CloudWatch.
Data Science	Bedrock and SageMaker.
Data Analytics	QuickSight (Licensing and SPICE).
Projects	Resources with direct tagging (Lambda, CloudTrail, ECR, Step Functions, API Gateway, Secrets Manager, ElastiCache, ECS, Firehose, Kinesis, SQS, SNS, OpenSearch, DMS, Redshift, DynamoDB, Glue, etc.) and allocated costs (S3, Athena, EMR).

6. Next Steps

    Definition of the Project Dictionary: Formally list permitted names for the project tag to prevent billing fragmentation.

    Tag Implementation: Execute retroactive tagging and configure enforcement (via Service Control Policies or Terraform) for team and project keys on all resources.

    Athena Cost Breakdown by Origin: Map and extract Athena costs by cross-referencing the executing IAM Role with the source QuickSight Dataset to identify the project driving the expense.

    EMR Job Isolation: Ensure every EMR on EKS execution uses the namespace corresponding to its respective project/team for accurate reading via Kubecost.

    Access Logs Audit: Configure metric extraction from S3 logs for the allocation engine, linking data traffic to the respective project.

    Kubecost Configuration: Implement namespace monitoring in the EKS cluster to capture real instance costs, including those used by EMR on EKS.
