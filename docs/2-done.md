## Cloud
- [Cloud Infrastructure as Code Provisioning with Terraform](cloud/iac-terraform.md)
- [Cloud Resource Tag Standardization and Governance](cloud/tag-policy.md)

### AWS
- [Athena Cost Auditing via CloudTrail](cloud/aws/athena.md)
- [Shared Storage for Airflow & OpenMetadata via Amazon EFS](cloud/aws/efs.md)
- [Kubernetes Cluster Provisioning in Cloud Environments](cloud/aws/eks.md)
- [Scalable Event-Driven Architecture for Data Enrichment and Integration](cloud/aws/event-driven-enrichment.md)
- [AWS IAM Governance: Tag-Based Access Control (ABAC) & Security Enforcement](cloud/aws/iam-core.md)
- [AWS Credential Governance and Standardization](cloud/aws/iam-security.md)
- [Cloud Network Architecture for Kubernetes Clusters](cloud/aws/network.md)
- [VPC Peering Cross-Account Connectivity for Data & Tech Networks](cloud/aws/peering.md)
- [Provisioning Amazon Redshift Serverless with Public Access Control](cloud/aws/redshift.md)
- [S3 Inventory: Data Lake Audit and Cost Allocation]((cloud/aws/s3-inventory.md))
- [Secure S3 Bucket Data Sharing via Partner IP Whitelisting](cloud/aws/s3-public-audit.md)

---

## Data Engineering
- [Data Ingestion with Airbyte for Small Distributed Teams](data-engineering/airbyte.md)
- [Data Batch Workflow Orchestration with Apache Airflow on Kubernetes](data-engineering/airflow.md)
- [Airflow DAG Migration & Pipeline Modernization](data-engineering/airflow-dags-migration.md)
- [Airflow DAGs Quality and Governance Policies](data-engineering/airflow-policies.md)
- [Orchestrated dbt Transformations with Airflow on Kubernetes](data-engineering/dbt.md)
- [Cost-Effective Open-Source Data Visualization with Metabase](data-engineering/metabase.md)
- [Small Files Monitoring and Optimization for Data Lakes Cost Performance](data-engineering/small-files.md)
- [EMR on EKS](cloud/aws/emr-k8s.md)
- [Scalable Big Data Processing Batch Workloads on Kubernetes with Apache Spark](data-engineering/spark-k8s.md)
- [Distributed Analytics Query Engine with Trino on Kubernetes](data-engineering/trino.md)
- [Lightweight Cost-Effective Data Processing for Analytics with DuckDB](data-engineering/duckdb.md)
- [Centralized Query Routing Across Multiple Trino Clusters with Trino Gateway](data-engineering/trino-gateway.md)

---

## Data Governance

- [Data Governance and Data Metadata Platform with OpenMetadata](data-governance/openmetadata.md)

---

## Databases
- [PostgreSQL on Kubernetes with CloudNativePG](databases/cnpg.md)

---

## DevOps
- [Reusable GitHub Actions Workflow Templates for Multi-Repository CI/CD Projects](devops/actions-centralization.md)
- [Automated Infrastructure Terraform Deployment with Github Actions](devops/cicd-terraform.md)
- [CI/CD Pipelines for Airflow Projects: DAG Code Releases and Image Build with GitHub Actions](devops/cicd-airflow.md)
- [Automated Lambda Deployment via GitHub Actions](devops/cicd-lambda.md)
- [Descheduler of Airflow Stuck Pods for Kubernetes Resource and Cost Optimization](devops/descheduler.md)
- [Kubernetes Image Update Automation with Flux](devops/flux-image-update.md)
- [Automated Pod Rollouts Triggered by ConfigMap and Secret Changes](devops/reloader/1-resume.md)
- [GitHub Repository Templating for Automated Project Setup](devops/repositories-templates.md)
- [Self-Hosted GitHub Actions on Kubernetes for Secure CI/CD](devops/self-hosted-actions.md)
- [Github Repository Governance and Compliance with GitHub Rulesets](devops/github-rulesets.md)

---

## FinOps
- [Memory & CPU Resources Advisor for Kubernetes Workloads with Grafana Dashboards](finops/grafana-resource-advisor.md)
- [Kubernetes Cost Savings with Dynamic NodePools Autoscaling and Right-Sizing with Karpenter](finops/karpenter.md)
- [Event-Driven Autoscaling in Kubernetes Using KEDA for Resource and Cost Optimization](finops/keda/keda.md)
- [Kubernetes Cost Optimization with Spot Instances](finops/spot.md)
- [Cost-Effective Kubernetes Compute Optimization with ARM-Based Nodes](finops/arm.md)
- [Cloud Cost Savings with SavingPlans & Instance Reservation](finops/cloud-reservations.md)
- [Kubernetes Cost Allocation by Project with Opencost](finops/kubecost.md)
- [Dynamic Kubernetes Resource Optimization with Vertical Pod Autoscaler](finops/vpa.md)

---

## Network
- [Automated DNS Records Management in Kubernetes with ExternalDNS](network/external-dns.md)
- [Kubernetes Network Ingress Traffic with NGINX Ingress Controller](network/ingress-controller.md)
- [Kubernetes Network Ingress Traffic with Gateway API and Envoy Gateway](network/gateway-api.md)
- [Network Isolation and Traffic Control in Kubernetes with Network Policies](network/network-policies.md)

---

## Observability
- [Alerting Kubernetes Infrastructure and Critical Applications Issues with Alertmanager](observability/alertmanager.md)
- [Kubernetes Log Collection with Fluent Bit and Loki Ingestion](observability/fluentbit.md)
- [Declarative Monitoring and Observability Dashboards with Grafana Operator](observability/grafana.md)
- [Kubernetes Log Centralized Storage with Loki](observability/logs.md)
- [Kubernetes Metrics Collection and Storage with Prometheus](observability/metrics.md)
- [Federated Prometheus for Long-Term Metrics Retention](observability/federated-prometheus.md)
- [Observability for Kubernetes with OpenTelemetry](observability/open-telemetry.md)
- [Long-Term Prometheus Metrics Retention with Thanos](observability/thanos.md)
- [Distributed Tracing of Microservice Request Flows on Kubernetes with Grafana Tempo](observability/tracing.md)
---

## Platform Engineering
- [Cost-Efficient Local Development Environment for Data Engineering Teams](platform-engineering/dev-env-local.md)
- [Declarative GitOps Infrastructure Delivery on Kubernetes with Flux](platform-engineering/gitops.md)
- [Terraform Module: Automated IAM for Airflow via EKS Pod Identity](platform-engineering/terraform-module.md)
- [Service Catalog and Internal Developer Portal for Kubernetes with Backstage](platform-engineering/idp-backstage.md)

---

## Security
- [Kubernetes Secret Synchronization between Azure Key Vault and External Secrets Operator](security/external-secrets-vault.md)
- [Docker Image Internalization from Public Container Registry to Private Container Registry](security/image-internalization.md)
- [Secretless Workload Authentication in Kubernetes with Workload Identity](security/workload-identity.md)
- [Centralizing Authentication Across Data and DevOps Tools with Entra ID Single Sign-On (SSO)](security/sso.md)
- [Cloud Security & Compliance Auditing with Prowler](security/prowler.md)
- [Code Security with SAST Open Source Tools](security/sast-open.md)

---

## Site Reliability Engineering
- [Resilient Persistent Volume Backup and Recovery for Kubernetes with Velero](sre/backup-k8s.md)
- [Kubernetes Node Pools Segmentation by Infrastructure Criticality](sre/node-pools.md)
- [Disaster Recovery Strategy for Kubernetes and Cloud Infrastructure](sre/disaster-recovery.md)
- [Service Level Indicators for Data Platforms on Kubernetes and Cloud](sre/service-level.md)
- [Kubernetes Resilience using Chaos Engineering Experiments with Litmus](sre/chaos-engineering.md)
- [Cross-Cluster PVC/PV Migration on Kubernetes with Velero](sre/pvc-cluster-migration.md)
