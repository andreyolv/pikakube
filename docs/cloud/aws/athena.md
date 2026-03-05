# Athena Cost Auditing via CloudTrail

## Problem

- Untraceable Cloud Spend: Athena costs were aggregated at the account level, making it impossible to identify which specific team, query, or application was driving the bill.
- Lack of Granular Visibility: Standard AWS Billing logs do not provide the link between a specific SQL execution and the IAM User/Role that triggered it.
- Hidden Inefficient Queries: High-cost, unoptimized queries were being executed without accountability, leading to budget overruns.
- Audit Gaps: Difficulty in correlating Athena QueryID with the originating IP or service, complicating security and financial audits.

## Solution
- CloudTrail Data Mapping: Integrated AWS CloudTrail logs with Amazon Athena to capture StartQueryExecution events and extract the metadata of every request.
- Query-to-Principal Correlation: Developed a SQL-based analysis that crosses Athena's query history with CloudTrail's userIdentity, mapping every dollar spent to a specific IAM Principal.
- Automated Cost Dashboarding: Created a process to calculate costs based on the dataScannedInBytes field (multiplied by the $5.00 per TB rate) to provide real-time spending insights.
- Usage Attribution by Team: Grouped costs by tags and IAM roles, allowing for accurate "Chargeback" or "Showback" reports for different departments.
- Top-Talker Identification: Identified the most expensive queries and users, enabling targeted optimizations and the implementation of Athena Workgroups quotas to prevent runaway costs.
- Historical Auditing: Built a long-term cost history repository in S3, allowing the finance team to track spending trends and anomalies over time.
