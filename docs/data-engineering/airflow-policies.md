# Airflow DAGs Quality and Governance Policies

## Problem:
- DAG and Task Timeout: Prevent DAGs and tasks from running for excessive time in Airflow.
- Owner Allocation: Ensure DAG owners are assigned correctly according to business areas, enabling role-based access control for each department.
- Namespace Allocation: Ensure tasks are allocated to valid namespaces, preventing performance degradation due to incorrect namespace allocation.
- Project Cost Allocation: Guarantee tasks are deployed to the correct project namespace to link Kubernetes cluster costs accurately to projects.
- Governance and Quality Standards: Enforce mandatory parameters across 1000+ production Airflow DAGs for standardized deployment and compliance.

## Solution:
- Policy Violation Handling: Non-compliant DAGs are blocked from deployment with an error message (AirflowClusterPolicyViolation on ImportError).
- Executor Support: Policies apply to both KubernetesExecutor (legacy) and pod_override (new method).
- Timeout Policy: DAG must include a dagrun_timeout (less than 24 hours).
- Tagging Policy: Each DAG should have at least one tag representing data layers or sensitivity.
- Owner Policy: The owner parameter must be defined in default_args, except for EmptyOperator.
- Email Policy: The email parameter must be included in default_args for alerting, except for EmptyOperator.
- Project Metadata Policy: Include project metadata (project name, namespace, GitHub repository) in the DAG’s description.
- Namespace Policy: Tasks must have a valid executor_config with the correct project namespace.
- Resource Request Policy: Ensure request_cpu and request_memory are defined in executor_config for tasks.
- Access Control Mutation: Implement access_control based on the owner parameter for role-based Entra ID authentication.
- .airflowignore Recommendation: Use .airflowignore to avoid unnecessary task imports and reduce DAG processor load.

## Skills:
- Data Engineering
- Data Governance
- Data Quality
- Platform Engineering

## Tools:
- Python
- Apache Airflow
- Kubernetes