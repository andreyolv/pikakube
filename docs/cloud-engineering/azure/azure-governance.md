# Cloud Governance in Azure (Resource Naming, Cost Allocation Tags, and Ownership)

## Problem:
- Inconsistent Resource Naming: Lack of standardized naming conventions across Azure resources, leading to confusion and difficulties in identifying resources by purpose, environment, or owner.
- Ineffective Cost Management: Absence of proper tagging strategies for resource ownership and cost allocation, making it challenging to track expenses and optimize spending.
- Lack of Visibility and Control: Difficulty in maintaining governance standards and ensuring compliance with organizational policies, especially when multiple teams are provisioning resources.
- Operational Overhead: Increased complexity in managing resources without proper governance, leading to inefficiencies in cloud resource usage.

## Solution:
- Standardized Naming Convention:
-- Defined a clear, consistent naming standard for Azure resources, ensuring names include details such as environment, resource type, project, and region.
-- Implemented naming policies using Azure Policy to enforce adherence across all subscriptions.

- Cost Allocation via Tagging:
-- Established a comprehensive tagging strategy focused on cost allocation and resource ownership.
-- Mandatory tags include: Environment (e.g., Dev, Test, Prod), CostCenter, Owner, Project, and BusinessUnit.
-- Automated tag application through Azure Policy and Azure Functions to ensure compliance.

- Documentation and Guidelines:
-- Developed detailed guidelines for resource naming, tagging, and ownership standards.
-- Provided training and documentation to onboard teams to the governance framework.

- Improved Governance and Security:
-- Enhanced security by ensuring resources are properly classified and attributed to responsible parties.
-- Achieved cost optimization by providing detailed cost reports based on tags, allowing better budgeting and forecasting.

## Skills:
- 

## Tools:
- 

https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
tags recursos cloud
atrelar centro de custo por recurso ou RG