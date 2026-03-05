# Memory & CPU Resources Advisor for Kubernetes Workloads with Grafana Dashboards

## Problem:
- Lack of Visibility into Resource Utilization: Kubernetes users often struggle to monitor resource allocation versus actual usage, leading to inefficiencies such as over-provisioning or underutilization.
- Resource Waste: Disparities between requested and utilized resources can result in unused capacity, leading to increased operational costs and inefficiencies.
- Risk of Overuse: Workloads consuming more resources than requested can lead to interruptions, especially in environments like using VMs (Virtual Machines) Spot, where VMs sizes are dynamically provisioned based on the requested resources.

## Solution:
- Custom Grafana Dashboards: Designed and implemented Grafana dashboards to visualize key metrics such as CPU and memory usage, requests, and limits across nodes, pods, and namespaces. These dashboards offer real-time insights into resource allocation and utilization.
- Highlighting Resource Discrepancies: The dashboards provide clear visibility into the disparities between requested and utilized resources, enabling users to identify and address inefficiencies. This allows users to adjust resource requests better aligned with actual usage, reducing waste and optimizing costs.
- Preventing Overuse and Interruptions: By exposing workloads that consistently exceed their requested resources, the dashboards help mitigate risks of interruptions, particularly in environments using VMs Spot. This allows users adjust resource requests to avoid.potential disruptions.

## Skills:
- DevOps
- FinOps

## Tools:
- Kubernetes
- Grafana
- Prometheus

gerar indicador de eficiencia de namespace