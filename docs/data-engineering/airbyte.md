# Data Ingestion with Airbyte for Small Distributed Teams

## Problem:
- Fragmented Data Ownership: Small data teams operated in silos, each managing their own data pipelines with custom scripts and tools, resulting in duplicated work and inconsistent practices.
- High Technical Barrier: Non-technical data analysts were unable to create or maintain data ingestion pipelines without help from engineers, slowing down experimentation and access to new datasets.
- Lack of Standardization: No shared platform for managing connectors, scheduling syncs, or monitoring failures — leading to poor observability and hard-to-trace data issues.
- Delayed Insights: Time spent on manual ingestion and troubleshooting reduced the speed of delivering business insights and hindered collaboration between teams.

## Solution:
- Self-Hosted Airbyte Deployment: Implemented a centralized Airbyte instance within the organization’s infrastructure, allowing teams to manage data connectors through a simple, user-friendly interface.
- No-Code Data Ingestion: Empowered data analysts to set up and manage connectors themselves — selecting sources, destinations, and sync schedules directly from the Airbyte UI, with no need for scripting or Git knowledge.
- Role-Based Access Control (RBAC): Enabled fine-grained access within the Airbyte UI so analysts could operate within their own workspaces without impacting other teams or requiring elevated permissions.
- Faster Time to Insight: Reduced the average time to onboard new data sources from days to hours, enabling analysts to iterate faster and collaborate across teams using a shared ingestion layer.

## Future Improvements:
SSO Integration: Plan to integrate Single Sign-On (SSO) using providers like OAuth2, Entra ID, simplifying access management and ensuring seamless and secure authentication for users across the organization. Não possível não versão OpenSource.
