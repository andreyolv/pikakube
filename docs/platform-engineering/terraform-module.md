# Terraform Module: Automated IAM for Airflow via EKS Pod Identity

## Project Objectives:
- Modern Identity Management: Implement EKS Pod Identity as the native solution to map AWS IAM roles to Kubernetes Service Accounts, bypassing OIDC trust policy complexity.
- Automated Namespace Provisioning: Scale Airflow projects by automatically linking IAM permissions to specific Kubernetes namespaces during the Terraform apply.
- Standardized Data Access: Define a reusable baseline of permissions for Athena, S3, and Glue for data engineering workloads.

## Solution:
- EKS Pod Identity Association: Utilized the aws_eks_pod_identity_association resource to simplify the mapping between IAM and Kubernetes Service Accounts.
- Reusable Terraform Module: Created a single module that provisions the IAM Role and the Pod Identity association in one execution.
- Unified Resource Lifecycle: Managed the creation of the Kubernetes Namespace, Service Account, and AWS IAM Role within the same Terraform state for atomic deployments.
- Dynamic IAM Policy Attachment: Automated the attachment of predefined policies (S3, Glue, Athena) to the role created for each Airflow worker.
