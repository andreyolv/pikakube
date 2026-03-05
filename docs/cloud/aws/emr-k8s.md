# EMR on EKS

## Problem:
- Infrastructure Cost Reduction: Shift from dedicated EC2 clusters to a shared Kubernetes environment to eliminate idle resource waste.
- Efficient Resource Utilization: Implement a multi-tenant architecture where Spark workloads share the same compute nodes with other microservices.
- Rapid Cluster Provisioning: Reduce the time required to spin up data processing environments by leveraging the pre-warmed capacity of an existing EKS cluster.
- Granular Scaling: Enable fine-grained auto-scaling of Spark executors to match the exact demands of the job, avoiding over-provisioning.

## Solution:
- EMR on EKS Deployment: Configured EMR virtual clusters to run Spark jobs directly on Amazon EKS, leveraging the efficiency of containerized workloads.
- Spot Instance Integration: Optimized compute costs by up to 70% by utilizing AWS Spot Instances for Spark executors, managed via Kubernetes node groups.
- Dynamic Resource Allocation: Implemented Spark’s dynamic allocation to automatically adjust the number of executors based on the workload queue.
- Compute Isolation with Namespaces: Utilized Kubernetes namespaces and RBAC to isolate different data projects, ensuring security and cost-center tracking.
- Karpenter / Cluster Autoscaler Integration: Integrated advanced autoscalers to rapidly provision and terminate nodes, ensuring the cluster only costs what is strictly necessary during job execution.
- Centralized Job Observability: Configured Prometheus to monitor job performance and resource consumption, providing a clear ROI on infrastructure spend.
