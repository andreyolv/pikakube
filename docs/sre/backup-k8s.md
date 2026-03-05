# Resilient Persistent Volume Backup and Recovery for Kubernetes with Velero

## Problem:
- Data Corruption: Addressing potential corruption of SQL or NoSQL database volumes deployed in Kubernetes.
- Upgrade Risks: Managing risks associated with upgrading Helm charts or applications relying on persistent volumes.
- Schema Migrations: Safeguarding data during schema changes in SQL databases.
- PVC Deletion or Corruption: Preventing accidental deletion or intentional corruption of PersistentVolumeClaims (PVCs) by malicious actors.
- StorageClass Changes: Facilitating transitions between different StorageClasses for PVCs.
- Cluster Migration: Supporting seamless migration of PVCs between clusters within the same or across different cloud providers.

## Solution:
- Azure-Based Backup Infrastructure: Deployed backup solutions on Microsoft Azure, organizing snapshots and YAML configurations into Resource Groups and Storage Accounts for each environments.
- Enhanced Security: Implemented Private Endpoints and disabled public network access to Storage Accounts.
- Scheduled Incremental Backups: Configured cost-efficient incremental backups with a 14-day time-to-live (TTL) to optimize storage usage and reduce costs.
- Filtered StorageClass Support: Applied filters to exclude unsupported Azure StorageClasses for Velero restores, ensuring compatibility and reliability.
- Pre-Activity Manual Backups: Mandated manual backups before critical operations, such as database updates, to provide additional protection.
- GitOps-Synchronized Restores: Aligned manual restore operations with GitOps tools to prevent automatic synchronization of PVCs until the Velero restore is completed.
- Flexible StorageClass Migration: Enabled changes to StorageClasses, facilitating migrations from single-region to multi-region setups for improved data availability.
- Integrated Monitoring: Integrated Prometheus to monitor Velero operations, creating custom metrics and alerts for failures (complete or partial) and backup deletion errors when TTL expires.

automatizar teste backup e restore 
processo automatizado teste backup e restore

## Skills:
- Cloud Computing
- DevOps
- Site Reliability Engineering
- Security
- Observability

## Tools:
- Microsoft Azure
- Kubernetes
- Velero
