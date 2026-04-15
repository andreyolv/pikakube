# Cross-Cluster PVC/PV Migration on Kubernetes with Velero

## Problem:
- Stateful Application Portability: Migrating stateful workloads between Kubernetes clusters is complex due to tight coupling between PVCs, StorageClasses, and underlying cloud storage.
- Risk of Data Loss: Manual copy processes increase the risk of partial restores, corrupted data, or inconsistent application state.
- Cluster Lifecycle Events: Cluster upgrades, re-creations, or cloud migrations often require moving persistent data across clusters with minimal downtime.
- StorageClass Incompatibilities: Source and target clusters frequently use different StorageClasses, CSI drivers, or storage backends.
- Operational Downtime: Traditional migration approaches require long maintenance windows and manual intervention.
- GitOps Conflicts: Restoring PVCs without coordinating GitOps tools can lead to resource drift or unintended deletions.

## Solution:
- Velero-Based Cross-Cluster Migration: Implemented PVC migration using Velero backups and restores, enabling reliable data transfer between independent Kubernetes clusters.
- StorageClass Remapping: Applied restore-time StorageClass mapping to adapt PVCs to the target cluster’s storage backend without changing application manifests.
- Snapshot and File-Level Strategies: Used CSI snapshots where supported and filesystem-level backups where snapshots were unavailable, ensuring broad compatibility.
- GitOps-Aware Restore Flow: Temporarily paused GitOps reconciliation (Flux/ArgoCD) during restore operations to prevent conflicts and ensure a clean migration process.
- Pre-Migration Validation: Enforced manual backup validation before restore, including checksum verification and test pod mounts.
- Minimal Downtime Approach: Coordinated application scaling and restore sequencing to minimize service disruption during migration.
- Observability and Auditing: Integrated Prometheus metrics and alerts for backup and restore operations, providing visibility and traceability across environments.
- Cloud-Agnostic Design: Supported migrations across clusters running on different cloud providers or on-prem environments.

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
