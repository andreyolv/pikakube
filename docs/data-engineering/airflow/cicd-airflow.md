# CI/CD Pipelines for Airflow Projects: DAG Code Releases and Image Build with GitHub Actions
## Problem:
- Lack of CI/CD Workflows: Without automated CI/CD pipelines, Airflow DAG updates were managed manually, leading to inconsistent deployments and added complexity in tracking and deploying code across multiple repositories.
- Manual Image Builds: Airflow project images were built manually using tags and commits, which introduced errors and delays in the deployment process.

## Solution:
- Automated DAG Deployment with GitHub Actions: Configured CI pipelines to automatically push Airflow DAG files to an Azure File Share, which is mounted as a volume in Kubernetes. This ensures Airflow instances always access the latest DAGs without manual intervention.
- Automated Image Builds: Set up GitHub Actions workflows to automatically build and deploy Airflow project images based on GitHub tags, pushing them to a private Azure Container Registry, streamlining the process and ensuring consistency across deployments.

## Skills:
- DevOps
- Cloud Computing

## Tools:
- Github Actions
- Airflow
- Docker
- Azure File Share
- Azure Container Registry
