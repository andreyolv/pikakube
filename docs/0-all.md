# PikaKube Data Platform Portfolio

# Summary
- [Cloud](#cloud)
- [Data Engineering](#data-engineering)
- [Data Governance](#data-governance)
- [Data Streaming](#data-streaming)
- [Databases](#databases)
- [DevOps](#devops)
- [FinOps](#finops)
- [Management](#management)
- [MLOps](#mlops)
- [Network](#network)
- [Observability](#observability)
- [Platform Engineering](#platform-engineering)
- [Security](#security)
- [Software Engineering](#software-engineering)
- [Site Reliability Engineering](#site-reliability-engineering)

---

## Cloud
- [Cloud Infrastructure as Code Provisioning with Terraform](cloud/iac-terraform.md)
- [Cloud Resource Tag Standardization and Governance](cloud/tag-policy.md)

### Azure
- [Azure Cost Optimization and Performance Improvement with Azure Advisor](cloud/azure/azure-advisor.md)
- [Azure Security Visibility and Response with Microsoft Defender for Cloud](cloud/azure/azure-defender.md)
- [Cloud Governance in Azure (Resource Naming, Cost Allocation Tags, and Ownership)](cloud/azure/azure-governance.md)
- [Cloud Infrastructure Provisioning](cloud/azure/cloud-provisioning.md)
- [Provisioning Azure Databricks with Security Best Practices](cloud/azure/databricks.md)
- [Azure Event Hubs for Data Lake Access Auditing](cloud/azure/eventhub.md)
- [Network Security and Private Connectivity with Private Endpoints](cloud/azure/private-endpoints.md)

### AWS
- [Athena Cost Auditing via CloudTrail](cloud/aws/athena.md)
- [Shared Storage for Airflow & OpenMetadata via Amazon EFS](cloud/aws/efs.md)
- [Kubernetes Cluster Provisioning in Cloud Environments](cloud/aws/eks.md)
- [EMR on EKS](cloud/aws/emr-k8s.md)
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
- [Real-Time Data Streaming with Confluent Cloud](data-engineering/confluent.md)
- [Orchestrated dbt Transformations with Airflow on Kubernetes](data-engineering/dbt.md)
- [Lightweight Cost-Effective Data Processing for Analytics with DuckDB](data-engineering/duckdb.md)
- [Cost-Effective Open-Source Data Visualization with Metabase](data-engineering/metabase.md)
- [Small Files Monitoring and Optimization for Data Lakes Cost Performance](data-engineering/small-files.md)
- [Scalable Big Data Processing Batch Workloads on Kubernetes with Apache Spark](data-engineering/spark-k8s.md)
- [Centralized Query Routing Across Multiple Trino Clusters with Trino Gateway](data-engineering/trino-gateway.md)
- [Distributed Analytics Query Engine with Trino on Kubernetes](data-engineering/trino.md)

---

## Data Governance
- [Column-Level Security for Fine-Grained Data Access Control](data-governance/column-level-security.md)
- [Data Catalog GitHub Abstraction Layer](data-governance/data-catalog-agnostic.md)
- [Data Catalog & Data Governance with OpenMetadata](data-governance/data-catalog.md)
- [Data Contracts for Reliable and Scalable Data Products](data-governance/data-contract.md)
- [Data Lake Governance Standardization](data-governance/data-lake-governance.md)
- [Data Lineage for End-to-End Data Visibility and Governance](data-governance/data-lineage.md)
- [Standardization of Data Products for Scalable Analytics Platforms](data-governance/data-products.md)
- [Data Quality Management and Monitoring for Analytics Platforms](data-governance/data-quality.md)
- [Standardization of Apache Iceberg Table Format for Lakehouse](data-governance/iceberg.md)
- [DataLake Access Auditing and Governance](data-governance/lake-audience.md)
- [Data Lake Ownership and Accountability Framework](data-governance/lake-owner.md)
- [Data Lake Policy Lifecycle Management](data-governance/lake-policy-lifecycle.md)
- [REST Iceberg Metadata Catalog with Lakekeeper](data-governance/lakekeeper.md)
- [Unified Metadata Management for Data Products](data-governance/metadata.md)
- [Data Governance and Data Metadata Platform with OpenMetadata](data-governance/openmetadata.md)

---

## Data Streaming
- [Real-Time SQL Server Data Ingestion with Debezium Change Data Capture](data-streaming/cdc-debezium.md)
- [Kafka to Delta Lakehouse: Real-Time Data Ingestion with PySpark Consumer](data-streaming/consumer-delta.md)
- [Streaming Data Ingestion from Kafka into Iceberg Lakehouse with Kafka Connect](data-streaming/consumer-iceberg.md)
- [Real Time Streaming Processing on Kubernetes with Apache Flink](data-streaming/flink.md)
- [Event Streaming Platform on Kubernetes with Apache Kafka and Strimzi](data-streaming/kafka-k8s.md)
- [Spark Streaming for Temporal Data Lake Access Auditing](data-streaming/lake-logs-processing.md)
- [Direct Database CDC to Iceberg Lakehouse without Kafka using OLake](data-streaming/olake.md)
- [Real-Time User-Facing Analytics with StarRocks](data-streaming/user-facing-analytics.md)

---

## Databases
- [PostgreSQL on Kubernetes with CloudNativePG](databases/cnpg.md)
- [Declarative PostgreSQL Operations with Crossplane SQL Provider](databases/db-gitops-manage.md)
- [Standardized MongoDB Deployment on Kubernetes](databases/mongo.md)
- [Standardized Neo4j Database Deployment on Kubernetes](databases/neo4j.md)
- [Performance Dashboard Monitoring for Postgres](databases/pghero.md)
- [PostgreSQL Database Migration Process on Kubernetes](databases/postgres-migration.md)
- [Standardized Redis Deployment on Kubernetes](databases/redis.md)
- [SQL Exporter for Prometheus Metrics](databases/sql-exporter.md)

---

## DevOps
- [Reusable GitHub Actions Workflow Templates for Multi-Repository CI/CD Projects](devops/actions-centralization.md)
- [Automated Infrastructure Terraform Deployment with Github Actions](devops/cicd-terraform.md)
- [CI/CD Pipelines for Airflow Projects: DAG Code Releases and Image Build with GitHub Actions](devops/cicd-airflow.md)
- [Container Registry Insights and Image Lifecycle Management](devops/container-registry.md)
- [Airflow DAG Quality Assurance in CI/CD with Custom GitHub Action](devops/custom-action.md)
- [Automated Lambda Deployment via GitHub Actions](devops/cicd-lambda.md)
- [Descheduler of Airflow Stuck Pods for Kubernetes Resource and Cost Optimization](devops/descheduler.md)
- [Automated Documentation Updates from Github to Confluence with Github Actions](devops/doc-confluence-action.md)
- [Kubernetes Image Update Automation with Flux](devops/flux-image-update.md)
- [GitHub Administration and Security Governance](devops/github-admin.md)
- [Software Development Productivity with GitHub Copilot](devops/github-copilot.md)
- [Github Repository Governance and Compliance with GitHub Rulesets](devops/github-rulesets.md)
- [Automated Release Versioning with GitHub Pull Requests](devops/github-versioning.md)
- [Standardized Technical Documentation Git-Integrated with MkDocs](devops/mkdocs.md)
- [Pull Request Template Standardization](devops/pullrequest-template.md)
- [Automated Pod Rollouts Triggered by ConfigMap and Secret Changes](devops/reloader/1-resume.md)
- [GitHub Repository Templating for Automated Project Setup](devops/repositories-templates.md)
- [Self-Hosted GitHub Actions on Kubernetes for Secure CI/CD](devops/self-hosted-actions.md)

---

## FinOps
- [Cost-Effective Kubernetes Compute Optimization with ARM-Based Nodes](finops/arm.md)
- [Budget-Based Cost Alerting and Governance for Cloud & Data Platform](finops/budges-alerts.md)
- [Cloud Cost Savings with SavingPlans & Instance Reservation](finops/cloud-reservations.md)
- [Optimizing Kubernetes Resource Allocation to VMs with Custom Kubernetes Scheduler](finops/custom-kubernetes-scheduler.md)
- [Data Lake Cost Division by Project](finops/datalake-cost-division.md)
- [Memory & CPU Resources Advisor for Kubernetes Workloads with Grafana Dashboards](finops/grafana-resource-advisor.md)
- [Kubernetes Cost Savings with Dynamic NodePools Autoscaling and Right-Sizing with Karpenter](finops/karpenter.md)
- [Event-Driven Autoscaling in Kubernetes Using KEDA for Resource and Cost Optimization](finops/keda/keda.md)
- [Kubernetes Cost Allocation by Project with Kubecost](finops/kubecost.md)
- [Scheduled Kubernetes Cluster Shutdown for Cost Optimization](finops/kubernetes-shutdown.md)
- [Kubernetes Cost Optimization with Spot Instances](finops/spot.md)
- [Dynamic Kubernetes Resource Optimization with Vertical Pod Autoscaler](finops/vpa.md)
- [Relatório FinOps]

---

## Management
- [Definição de arquitetura de referência](management/documentation/p-arquitetura-ref.md)
- [Definição de ADRs](management/documentation/p-doc-adr.md)
- [Definição de Catalog de Serviço de DataOps](management/documentation/p-service-catalog.md)
- [documentação da infraestrutura de plataforma, operação](management/documentation/p-platform.md)
- [comunicados de incidentes, manutenção que causam impacto](management/documentation/p-comunicados.md)
- [planejamento de atividades e metas em metolodia agil](management/projects/p-agile.md)
- [gestão de vulnerabilidades](management/governance/p-gestao-vulnerabilidades.md)
- [transferencia de conhecimento e apresentações](management/team/knowledge-transfer.md)

---

## MLOps
- [Workflow Orchestration and Automation with LangFlow](mlops/langflow.md)
- [Centralized Pipeline Management and Execution with MCPServer](mlops/mcpserver.md)
- [Machine Learning Lifecycle Management with MLflow](mlops/mlflow.md)
- [Interactive Machine Learning Model Deployment with Streamlit](mlops/streamlit.md)

---

## Network
- [Automated DNS Records Management in Kubernetes with ExternalDNS](network/external-dns.md)
- [Kubernetes Network Ingress Traffic with Gateway API and Envoy Gateway](network/gateway-api.md)
- [User Access Audience Monitoring for Ingress Controller](network/ingress-controller-audience.md)
- [Kubernetes Network Ingress Traffic with NGINX Ingress Controller](network/ingress-controller.md)
- [Load Balancer for On-Prem Kubernetes with MetalLB](network/metallb.md)
- [Network Isolation and Traffic Control in Kubernetes with Network Policies](network/network-policies.md)

---

## Observability
- [Alerting Kubernetes Infrastructure and Critical Applications Issues with Alertmanager](observability/alertmanager.md)
- [Standardized Monitoring and Alerting for Airflow & Kafka Applications](observability/data-platform-applications.md)
- [Data Infrastructure Monitoring with Synthetic Baseline Workload](observability/data-platform-infrastructure.md)
- [Federated Prometheus for Long-Term Metrics Retention](observability/federated-prometheus.md)
- [Kubernetes Log Collection with Fluent Bit and Loki Ingestion](observability/fluentbit.md)
- [Monitoring Software Delivery and Security Signals using Git Data](observability/git-export.md)
- [Declarative Monitoring and Observability Dashboards with Grafana Operator](observability/grafana.md)
- [Custom Metrics for Crossplane Composite Resources with Kube Metrics Server](observability/kube-metrics-server-custom.md)
- [Kubernetes Security and Compliance with Audit Log](observability/kubernetes-audit-logs.md)
- [Kubernetes Log Centralized Storage with Loki](observability/logs.md)
- [Kubernetes Metrics Collection and Storage with Prometheus](observability/metrics.md)
- [Observability for Kubernetes with OpenTelemetry](observability/open-telemetry.md)
- [Network Observability in Kubernetes with Retina and Hubble](observability/retina.md)
- [Query Performance Monitoring for Azure Synapse Analytics using a Custom Prometheus Exporter](observability/synapse-prometheus-exporter.md)
- [Long-Term Prometheus Metrics Retention with Thanos](observability/thanos.md)
- [Distributed Tracing of Microservice Request Flows on Kubernetes with Grafana Tempo](observability/tracing.md)

---

## Platform Engineering
- [Custom Helm Chart for Airflow Deployment Across Multiple Namespaces](platform-engineering/airflow-multinamespace-chart.md)
- [Self-Service Infrastructure Platform Engineering with Crossplane](platform-engineering/crossplane.md)
- [Data Development Environment on Kubernetes with Custom Helm Chart](platform-engineering/dev-env-k8s.md)
- [Cost-Efficient Local Development Environment for Data Engineering Teams](platform-engineering/dev-env-local.md)
- [Multi-Repository GitOps for Safe Team Autonomy in Kubernetes](platform-engineering/gitops-multirepo.md)
- [Declarative GitOps Infrastructure Delivery on Kubernetes with Flux](platform-engineering/gitops.md)
- [User-Friendly Kubernetes UI for Logs and Pod Monitoring with Headlamp](platform-engineering/headlamp.md)
- [Cluster Homepage with Automatic Ingress URL Discovery](platform-engineering/homepage-ingress-discovery.md)
- [Service Catalog and Internal Developer Portal for Kubernetes with Backstage](platform-engineering/idp-backstage.md)
- [Productive Local Kubernetes Cluster with GitOps](platform-engineering/kind-kustomize.md)
- [Virtualized Kubernetes Clusters for Multi-Team Isolation with vCluster](platform-engineering/vcluster.md)
- [Terraform Module: Automated IAM for Airflow via EKS Pod Identity](platform-engineering/terraform-module.md)
- [Intelligent Resource Scheduling with Apache YuniKorn on Kubernetes](platform-engineering/yunikorn.md)
- [Custom Kubernetes Operator for Continuous Secret Synchronization with SenhaSegura](platform-engineering/senhasegura-kubernetes-operator.md)

---

## Security
- [Cloud-Native Security Monitoring and Threat Detection with CNAPP and SIEM](security/cnapp-siem.md)
- [Ensuring Trusted Container Images with Cosign and Kyverno](security/cosign.md)
- [Dynamic Application Security Testing (DAST) with ZAP Proxy](security/dast-api.md)
- [Kubernetes Secret Synchronization between Azure Key Vault and External Secrets Operator](security/external-secrets-vault.md)
- [Docker Image Internalization from Public Container Registry to Private Container Registry](security/image-internalization.md)
- [Kubernetes Security and Compliance with Kubescape](security/kubescape.md)
- [Security and Compliance Policy as Code for Kubernetes with Kyverno](security/verno.md)
- [Rate Limiting in Nginx Ingress Controller for API Security](security/nginx-rate-limit.md)
- [Cloud Security & Compliance Auditing with Prowler](security/prowler.md)
- [Code Security with SAST Open Source Tools](security/sast-open.md)
- [Code Security with SAST and GitHub Advanced Security](security/sast.md)
- [Software Bill of Materials (SBOM) for Supply Chain Security](security/sbom.md)
- [Encrypted Kubernetes Secrets for GitOps Workflows with Sealed Secrets](security/sealed-secrets.md)
- [Centralizing Authentication Across Data and DevOps Tools with Entra ID Single Sign-On (SSO)](security/sso.md)
- [Automated TLS Certificate Management for Ingress Controller](security/tls-certs.md)
- [Container Vulnerability Scanning and Security Compliance with Trivy](security/trivy.md)
- [Secretless Workload Authentication in Kubernetes with Workload Identity](security/workload-identity.md)

---

## Software Engineering
- [Code Quality Standardization with Linters and Pre-Commit](software-engineering/linters.md)
- [Python Artifact Repository for Internal Libraries on Kubernetes](software-engineering/python-artifact-repo.md)
- [RabbitMQ Messaging Topology Kubernetes Operator](software-engineering/rabbitmq.md)
- [Python Dependency and Environment Management with UV](software-engineering/uv.md)

---

## Site Reliability Engineering
- [Resilient Persistent Volume Backup and Recovery for Kubernetes with Velero](sre/backup-k8s.md)
- [Progressive Canary Deployments in Kubernetes with Flagger](sre/canary-flagger.md)
- [Kubernetes Resilience using Chaos Engineering Experiments with Litmus](sre/chaos-engineering.md)
- [Disaster Recovery Strategy for Kubernetes and Cloud Infrastructure](sre/disaster-recovery.md)
- [Kubernetes Node Pools Segmentation by Infrastructure Criticality](sre/node-pools.md)
- [Cross-Cluster PVC/PV Migration on Kubernetes with Velero](sre/pvc-cluster-migration.md)
- [Service Level Indicators for Data Platforms on Kubernetes and Cloud](sre/service-level.md)
- [StorageClass Migration for Persistent Volumes on Kubernetes with Velero](sre/storageclass-migration.md)
