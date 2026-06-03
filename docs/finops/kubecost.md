# Kubernetes Cost Allocation by Project with Opencost

## Problem:
- Cost Visibility in Kubernetes: Azure billing only provides aggregated costs for AKS, without detailing consumption by workloads and namespaces running within the Kubernetes cluster. This makes it difficult to allocate costs accurately by projects and namespaces.
- Project-to-Namespace Relationship: Each namespace belongs to a specific project (1:n project:namespace relationship). Therefore, having a clear view of costs by namespace is essential for accurately dividing costs among projects.

## Solution:
- Implementation of Opencost: Deployed Opencost, an open-source tool designed to provide insights into Kubernetes resource costs. It was integrated into the cluster to monitor resource usage and calculate associated costs by namespace, deployment, and workloads.
- Cost Allocation and Optimization: Configured Opencost to provide granular cost allocation reports, enabling better budgeting and resource planning. Utilized its cost-saving recommendations to identify overprovisioned workloads and optimize resource requests and limits.
- Data Extraction for Historical Analysis: Configured daily data extraction through the Opencost API to store historical cost and usage data for future analysis and reporting.
- System Namespaces Allocation: For system namespaces not tied to specific projects, costs are proportionally distributed to project namespaces.
- Alerts and Budgets: Set up cost thresholds and alerts to notify teams of potential budget breaches, fostering proactive cost management.

## Skills:
- DevOps
- FinOps

## Tools:
- Kubernetes
- Opencost
