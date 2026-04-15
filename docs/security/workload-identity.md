# Secretless Workload Authentication in Kubernetes with Workload Identity

## Problem:
- Secret-Based Authentication Risks: Applications running in Kubernetes often rely on static secrets (tokens, keys, credentials), increasing the risk of leaks and credential sprawl.
- Credential Rotation Overhead: Manually rotating secrets across multiple workloads and namespaces is operationally complex and error-prone.
- Over-Privileged Access: Shared credentials make it difficult to enforce least-privilege access at the workload level.
- Poor Auditability: Mapping cloud or infrastructure access back to specific Kubernetes workloads is difficult when using shared service accounts or static - credentials.
- Security Gaps in Multi-Cluster Environments: Managing credentials consistently across multiple clusters increases complexity and security risk.

## Solution:
- Workload Identity for Kubernetes: Implemented workload identity to allow Kubernetes workloads to authenticate using their native ServiceAccount identity, - eliminating the need for static secrets.
- Pod-Level Identity Mapping: Bound Kubernetes ServiceAccounts directly to infrastructure or platform identities, enabling fine-grained, least-privilege - access per workload.
- Short-Lived Credentials: Leveraged token exchange mechanisms to issue short-lived credentials dynamically, reducing the blast radius of compromised - identities.
- Improved Security Posture: Removed long-lived secrets from manifests, ConfigMaps, and CI/CD pipelines.
- Audit and Traceability: Enabled clear traceability between infrastructure access and the originating Kubernetes workload for auditing and compliance.
- Multi-Cluster Ready: Standardized identity patterns across clusters to ensure consistent security controls and simplified operations.
- Seamless Application Integration: Applications authenticate transparently without code changes, relying on Kubernetes-native identity mechanisms.

## Tools:

solicitação de criação de projeto por backstage
automação backstage cria managed identity ia crossplane
output do client-id do managed identity insere no label de service account default do namespace
  labels: 
    azure.workload.identity/client-id:

bug, task não tá pegando o client id do service account, ta precisando passar como variavel no pod
testar passar serviceaccount default no executor config

ver alguma forma de passar via mutation label            labels={"azure.workload.identity/use": "true"}) em todos as tasks, mutation policy talvez

AZURE_TENANT_ID e AZURE_FEDERATED_TOKEN_FILE são montados automaticamente quando usa os labels
AZURE_CLIENT_ID deveria montar automatico tbm, mas ta bugado

esperar spark 4.0 pra funcionar workload identity, pra atualizarem a versão do hadoop azure com esse pacote.

RFC: AWS Identity Standardization for Airflow via EKS Pod Identity

Status: Proposed

Author: Andrey Gustavo de Oliveira

Scope: Airflow projects running on Kubernetes (EKS)

Version: 1.0
1. Abstract

This document proposes replacing IAM Users and manual Airflow connections with EKS Pod Identity. The standard establishes the use of IAM Roles named airflow-[project], which will be automatically injected into Pods. This allows application code (boto3) to function seamlessly without the need for static access keys.
2. Context and Motivation

Currently, managing access to AWS resources (S3, Athena, Redshift) often relies on IAM Users and static keys configured within Airflow Connections. This creates security risks (key leakage) and operational overhead for password rotation.

EKS Pod Identity simplifies this workflow by linking a Kubernetes Service Account (SA) directly to an IAM Role, eliminating the need for complex OIDC provider management or manual secret handling.
3. Proposed Architecture
3.1 Naming and Environment Scope

To balance governance and agility, we adopt the following:

    Naming Pattern: airflow-[project-name]

    Environment Policy: The same Role will be used for both DEV and PRD.

    Rationale: Facilitates DAG migration between environments, reduces the overhead of creating multiple Roles, and simplifies infrastructure templates, as access permissions to buckets and services are typically mirrored.

3.2 Why IAM Roles instead of IAM Users?

    Ephemeral Credentials: Roles generate temporary tokens (STS). Users use permanent keys.

    Zero Secret Management: No need to create or store passwords in Airflow.

    Native Security: Access is revoked automatically if the Pod is deleted.

    Auditability: CloudTrail identifies which specific Pod performed an action via sts:TagSession.

4. Technical Mechanics

Using Pod Identity eliminates the need to configure Airflow Connections. The process occurs via environment injection:

    Credential Injection: The EKS agent mounts environment variables (AWS_CONTAINER_CREDENTIALS_FULL_URI) and a token inside the container.

    Automatic Detection (Boto3): The AWS SDK (boto3, aws-cli) checks these variables by default before looking for any other keys.

    Zero Extra Code: Developers must not pass aws_access_key_id or aws_secret_access_key in the code.

Standardized Code Example:
Python

import boto3

# Boto3 automatically detects the 'airflow-project' Role injected into the Pod
s3 = boto3.client('s3') 
s3.list_objects_v2(Bucket='project-bucket')

5. Trust Policy Structure

Every airflow-[project] Role must trust the EKS Pod Identity service to allow identity assumption:
JSON

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": { "Service": "pods.eks.amazonaws.com" },
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ]
        }
    ]
}

6. DBT Connection Standardization (profiles.yml)

The primary advantage of Pod Identity for dbt is the elimination of local profiles or keys in the configuration file. dbt will use the AWS environment authentication method.
6.1 Redshift (Serverless or Cluster)

For Redshift, we will use the iam method. The driver will fetch credentials from Pod Identity to generate a temporary database token.
YAML

name_redshift_dbt:
  outputs:
    hom:
      dbname: hom
      host: name.0123456789.us-east-1.redshift-serverless.amazonaws.com
      method: iam
      port: 5439
      schema: public
      threads: 5
      type: redshift
      user: user
      region: us-east-1
    prd:
      dbname: prd
      host: name.0123456789.us-east-1.redshift-serverless.amazonaws.com
      method: iam
      port: 5439
      schema: public
      threads: 5
      type: redshift
      user: user
      region: us-east-1
  target: hom

6.2 Athena

For Athena, dbt uses the AWS SDK under the hood. By commenting out or removing aws_profile_name, the driver automatically uses the Role injected by EKS.
YAML

fipe_dbt:
  outputs:
    dev:
      database: awsdatacatalog
      region_name: us-east-1
      s3_staging_dir: s3://abcd
      work_group: primary
      seed_s3_upload_args:
        ACL: bucket-owner-full-control
      schema: dev
      threads: 8
      # aws_profile_name: default
      type: athena
  target: dev

7. Next Steps (Automation Roadmap)
7.1 Terraform Module Creation

Develop a reusable module that handles:

    Creation of the airflow-[project-name] Role.

    Attachment of common permissions (S3 Read/Write, Athena execution).

    aws_eks_pod_identity_association resource to link the Role to the ServiceAccount in the cluster.

7.2 Project Template Update (GitHub)

Add to the cookiecutter or new data project templates:

    Terraform code example using the module with baseline permissions.

    Python code examples using boto3 without manual credential instantiation.