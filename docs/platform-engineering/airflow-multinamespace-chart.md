# Custom Helm Chart for Airflow Deployment Across Multiple Namespaces

## Problem:
- Complex Airflow Deployment: Deploying Apache Airflow in multiple Kubernetes namespaces with persistent volumes (PV) and persistent volume claims (PVC) for DAGs and logs requires careful management of resources and configuration for each namespace.
- Manual Configuration Overhead: The manual setup of PVs and PVCs for each namespace can be error-prone and time-consuming, requiring custom scripts and configurations to ensure proper isolation of DAGs and logs across namespaces.

## Solution:
- Custom Helm Chart Creation: Developed a custom Helm Chart to deploy Apache Airflow across multiple Kubernetes namespaces, automating the creation of PV and PVC for DAGs and logs in each namespace.
- Namespace-Specific Configuration: Configured the Helm chart to dynamically create PV and PVC resources for each namespace, ensuring isolation of DAGs and logs while adhering to best practices for persistent storage management.

## Skills:
- Platform Engineering
- DevOps

## Tools:
- Helm
- Kubernetes

