# Optimizing Kubernetes Resource Allocation to VMs with Custom Kubernetes Scheduler

## Problem:
- Default Scheduling Strategies: Kubernetes' default scheduler employs algorithms like LeastAllocated, which may not always align with specific goals for optimizing resource usage and cost efficiency.
- Operational Inefficiency: Workloads are often distributed unevenly across nodes, leading to increased operational costs due to underutilized capacity. This uneven distribution also complicates scaling down nodes, reducing the potential for infrastructure cost savings.
- Resource Waste: Since Kubernetes costs are tied to the number of virtual machines (VMs) in use, underutilized nodes or excessive resource fragmentation result in unnecessary expenses.
- Managed Kubernetes Constraints: In managed Kubernetes services like Azure Kubernetes Service (AKS), the default scheduler is part of the control plane and cannot be modified, limiting flexibility to implement custom scheduling strategies directly.

## Solution:
- Custom Kubernetes Scheduler: A custom scheduler was developed using the MostAllocated strategy, prioritizing nodes with higher current resource utilization. This strategy helps consolidate workloads onto fewer nodes, making it easier to scale down underutilized nodes when their workloads finish.
- Enhanced Resource Optimization: By reducing resource fragmentation and maximizing node utilization, the MostAllocated strategy minimizes waste and ensures the available infrastructure is used efficiently, resulting in cost savings.
- Seamless Integration with AKS: The custom scheduler was deployed as a workload within the cluster to ensure compatibility with AKS, bypassing the limitations of modifying the default scheduler in a managed service.
- Automated Scheduling with Gatekeeper: Gatekeeper was configured to mutate all pods within the cluster, automatically injecting the custom scheduler field into pod specifications. This ensures that all workloads are scheduled using the custom strategy without requiring manual intervention.

## Skills:
- DevOps
- FinOps

## Tools:
- Kubernetes
- Gatekeeper
