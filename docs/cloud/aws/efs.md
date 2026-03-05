# Shared Storage for Airflow & OpenMetadata via Amazon EFS

## Problem:

- Storage Synchronization: Difficulty in keeping DAG files synchronized across multiple Airflow Workers and Schedulers running in a distributed Kubernetes cluster.
- Distributed Access Constraints: Traditional block storage (EBS) could not be mounted simultaneously by multiple nodes (ReadWriteMany), limiting the scalability of the metadata platform.
- Risk of Data Loss in DAGs: Lack of an automated recovery mechanism for the DAG repository, leaving the orchestration layer vulnerable to accidental deletions or file corruption.

## Solution:

- Elastic File System (EFS) Provisioning: Implemented Amazon EFS as a ReadWriteMany (RWX) storage solution, allowing multiple Airflow and OpenMetadata pods to access shared resources concurrently.
- Centralized DAG Management: Established a single EFS volume for Airflow DAGs, ensuring that code updates are immediately reflected across all schedulers and workers.
- Automated Backup Policy: Integrated with AWS Backup to perform daily snapshots of the EFS volume, ensuring a 30-day retention period and quick recovery of DAGs in case of failure.
- Persistent Log Repository: Configured a dedicated EFS directory for execution logs, preserving historical task data regardless of the lifecycle of the Kubernetes pods.
- EFS Access Points: Deployed EFS Access Points to enforce specific POSIX users and permissions, ensuring secure and isolated access for different application service accounts.
- High Availability & Durability: Leveraged the regional nature of EFS to ensure that DAGs and metadata remain available even in the event of an Availability Zone (AZ) failure.
