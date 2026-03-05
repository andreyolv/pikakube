# Orchestrated dbt Transformations with Airflow on Kubernetes

## Problem:
- Fragmented Transformation Orchestration: Running dbt models manually or via ad-hoc scripts lacks proper orchestration, dependency management, and observability.
- Limited Production Readiness: dbt executions without a robust scheduler make retries, SLAs, and failure handling difficult in production data pipelines.
- Environment Inconsistency: Managing dbt runs across development, staging, and production environments often leads to configuration drift.
- Scalability Constraints: Local or static dbt execution does not scale well with growing data volumes and parallel model execution.
- Poor Operational Visibility: Without centralized orchestration, tracking execution status, failures, and historical runs becomes challenging.
- Weak Integration with Data Platform Workflows: dbt transformations need to be coordinated with ingestion, validation, and downstream analytics jobs.

## Solution:
- dbt Orchestration with Airflow: Integrated dbt into Apache Airflow workflows to manage model execution, dependencies, retries, and SLAs in a production-grade scheduler.
- Astronomer on Kubernetes: Deployed Airflow using Astronomer on Kubernetes, providing a scalable, resilient, and cloud-agnostic orchestration platform.
- Isolated and Scalable dbt Execution: Executed dbt runs in Kubernetes pods, enabling horizontal scaling, resource isolation, and parallel execution of models.
- Environment-Aware Pipelines: Managed dbt profiles and configurations per environment, ensuring consistent behavior across dev, staging, and production.
- End-to-End Pipeline Coordination: Orchestrated dbt transformations alongside upstream ingestion and downstream analytics tasks within the same Airflow DAGs.
- Observability and Reliability: Leveraged Airflow logging, task retries, and failure alerts to improve operational visibility and reliability of dbt workloads.
- Git-Driven Workflows: Versioned dbt projects and Airflow DAGs in Git, enabling traceability, reviews, and reproducible data transformations.


elementary

https://docs.getdbt.com/guides/building-packages?step=1

Discovery macros, doc para estrutura descentralizada de repositório
