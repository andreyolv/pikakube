# Azure Event Hubs for Data Lake Access Auditing

## Problem:

- Delayed Security Insights: Relying on static storage logs for auditing caused a significant gap between unauthorized access events and their detection.
- Audit Fragmentation: Difficulty in centralizing access logs from multiple Data Lake (ADLS Gen2) containers for a unified view of User and Service Principal activity.
- Lack of Real-Time Monitoring: No native mechanism to trigger immediate alerts or streaming analysis for suspicious patterns (e.g., mass data deletion or unauthorized credential use).
- Storage Governance Gaps: High complexity in identifying which specific Service Principals were accessing sensitive data partitions in a multi-tenant environment.

# Solution:

- Streaming Audit Pipeline: Configured Azure Event Hubs as the centralized ingestion engine for all Data Lake diagnostic logs, enabling real-time stream processing.
- Diagnostic Settings Integration: Enabled Diagnostic Settings on the ADLS Gen2 storage accounts to automatically forward StorageRead, StorageWrite, and StorageDelete events to the Event Hub.
- Service Principal Activity Tracking: Structured the log ingestion to capture and isolate actions performed by Service Principals vs. Managed Identities, ensuring clear accountability.
- Identity-Based Security: Secured the Event Hub namespace using Azure RBAC and Shared Access Policies (SAS), restricting log consumption to authorized security tools only.
- Scalable Throughput Units: Optimized the Event Hub with Auto-Inflate enabled to handle sudden bursts of audit logs during high-volume data processing windows.
- Integration with Downstream Tools: Enabled the integration with Splunk/Microsoft Sentinel or custom consumers to analyze "Who, When, and How" data was accessed at the object level.
