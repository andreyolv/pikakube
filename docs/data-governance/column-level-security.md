# Column-Level Security for Fine-Grained Data Access Control

## Problem:
- Overexposed Sensitive Data: In analytical platforms and data warehouses, users often require access to datasets but should not see sensitive columns such as PII, financial values, or confidential business metrics.
- Coarse-Grained Access Control: Traditional access control mechanisms usually operate at table or schema level, making it difficult to enforce least-privilege principles.
- Operational Complexity: Duplicating tables or creating multiple views to hide sensitive columns increases maintenance overhead and risk of misconfiguration.
- Compliance & Governance Risks: Regulations and internal policies require strict control over who can access specific data fields, with auditability and consistency across tools.

## Solution:
- Column-Level Security (CLS) Enforcement: Implemented column-level security to restrict access to specific columns based on user identity, role, or group, ensuring sensitive fields are only visible to authorized consumers.
- Policy-Driven Access Control: Defined declarative security policies that map users and roles to allowed columns, enabling consistent enforcement across queries and workloads.
- Transparent Query Execution: Security rules are applied automatically at query time, without requiring changes to application logic or data models.
- Reduced Data Duplication: Eliminated the need for multiple sanitized datasets or views, simplifying data architecture and reducing operational overhead.
- Auditability & Compliance: Enabled clear visibility into which users can access which columns, supporting compliance requirements and simplifying security audits.
- Scalable for Analytics Use Cases: Designed the solution to work efficiently with large analytical datasets and concurrent users, maintaining performance while enforcing fine-grained controls.

## Skills:
- 

## Tools:
- 

static data masking (SDM) and dynamic data masking (DDM)
CLS https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/column-level-security