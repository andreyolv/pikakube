# Intelligent Resource Scheduling with Apache YuniKorn on Kubernetes

## Problem:
- Inefficient Resource Allocation: Kubernetes' default scheduler lacks fine-grained control over resource fairness, leading to suboptimal distribution in multi-tenant clusters.
- Big Data Workload Contention: Data-intensive applications like Apache Spark, Flink, and Jupyter often compete for resources, causing unpredictable job performance and long wait times.
- Lack of Multi-Tenant Isolation: Different teams and projects running on the same cluster face resource starvation and scheduling conflicts due to the absence of queue-based isolation.

## Solution:
- Advanced Scheduling with YuniKorn: Integrated Apache YuniKorn as the resource scheduler in the Kubernetes cluster, enabling intelligent, fair, and quota-aware scheduling for all data workloads.
- Multi-Tenant Queue System: Configured hierarchical queues to ensure resource guarantees and isolation for different teams and applications, aligning with organizational priorities.
- Optimized Big Data Execution: Improved throughput and reduced job startup times for Apache Spark and other batch workloads by leveraging YuniKorn’s native support for batch scheduling.
- Enhanced Fairness and Preemption: Implemented policies to ensure fair resource sharing across users and enabled preemption for high-priority jobs to meet SLAs.
- Seamless Integration: Maintained compatibility with existing Kubernetes-native tools and Helm charts, ensuring a non-disruptive transition to YuniKorn while improving cluster efficiency.

## Skills:
- 

## Tools:
- 

