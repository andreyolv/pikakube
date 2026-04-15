# StorageClass Migration for Persistent Volumes on Kubernetes with Velero

## Problem:
- Storage Technology Evolution: Kubernetes environments often need to migrate PersistentVolumeClaims (PVCs) when adopting new StorageClasses, such as moving from single-zone to multi-zone, or from legacy storage backends to more resilient and cost-effective options.
- Application Downtime Risk: Changing a StorageClass for existing PVCs is not natively supported by Kubernetes and typically requires data recreation, which can introduce downtime and operational risk.
- Data Integrity and Consistency: Migrating stateful workloads increases the risk of data loss or corruption if backups and restores are not carefully managed.

## Solution:
- Velero-Based PVC Migration: Implemented StorageClass migration using Velero backups and restores, enabling safe and controlled data movement between StorageClasses without manual volume manipulation.
- Snapshot and Restore Strategy: Leveraged Velero volume snapshots to capture consistent backups of PVCs and restore them using a target StorageClass, ensuring data integrity throughout the migration process.
- Minimal Downtime Approach: Coordinated application scaling and restore execution to minimize service disruption during migration of stateful workloads.
- GitOps Alignment: Integrated the migration process with GitOps workflows, temporarily pausing reconciliation to avoid conflicts while PVCs were being restored with the new StorageClass.
- Validation and Observability: Verified restored volumes through application-level checks and monitored Velero operations and failures using Prometheus and Grafana.

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

