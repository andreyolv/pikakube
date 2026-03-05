# Descheduler of Airflow Stuck Pods for Kubernetes Resource and Cost Optimization

## Problem:
- Scheduled Images by Airflow: Project teams schedule container images via Airflow workflows, but these images can contain syntax errors, incorrect tags.
- Lack of Policy Enforcement: Without proper evaluation through policies enforced by tools like Kyverno or Gatekeeper, there is no validation to ensure the correctness or availability of images before deployment. 
- Node Locking: Pods with invalid images consume resources and block nodes unnecessarily, preventing other workloads from utilizing the capacity and leading to increased costs and inefficient cluster usage.
- Resource Wastage: Pods with erroneous images remain in states like ImagePullBackOff or ErrImagePull, holding node resources without performing any useful work. This issue becomes especially critical when multiple parallel jobs are scheduled, amplifying the problem.
- High DAG Run Timeouts: Airflow DAGs can have long hour timeout periods, delaying the deprovisioning of stuck pods by Airflow.

## Solution:
- Automated Pod Eviction: Use the Kubernetes Descheduler with the PodLifeTime plugin to automatically evict pods stuck in undesirable states (ImagePullBackOff, ErrImagePull, InvalidImageName) after a defined period (e.g., 30 minutes).
- Namespace and Label Filtering: Configure exclusions for critical namespaces and use label selectors (e.g., dag_id) to target only Airflow-managed pods, ensuring controlled and precise eviction processes.
- Resource Reallocation: By removing stuck pods, free up node resources for valid workloads, ensuring that resources are utilized efficiently and reducing unnecessary costs.

# Skills:
- DevOps
- Platform Engineering

# Tools:
- Kubernetes
- Descheduler