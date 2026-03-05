# Kubernetes Cost Optimization with Spot Instances

## Problem:
- Cost Optimization Potential: Even with reserved instances already in place, there was still potential for cost savings on Kubernetes VM(Virtual Machines) usage.
- Adoption Hesitation: Teams were hesitant to use spot instances due to concerns about their reliability and how to implement them correctly, leading to missed opportunities for cost reduction and inefficient workload management.

## Solution:
- Spot Instance Strategy: Implemented a strategy to use spot instances for Kubernetes clusters, focusing on non-critical workloads. This led to over 50% cost savings by using preemptible VMs at lower prices.
- Guidelines for Adoption: Developed clear documentation and examples to help teams identify which workloads were suitable for spot instances, making it easier for them to adopt this cost-saving approach.
- Automation with Gatekeeper: Set up Gatekeeper to automatically apply nodeSelector and toleration fields to pods based on namespace labels. This ensured that spot instances were used in the appropriate namespaces, simplifying adoption.
- High Availability for Critical Workloads: Kept reserved instances for high-availability workloads, ensuring that critical services remained resilient while non-critical workloads benefited from cost savings.
- Metrics Alerts: Configured Kubernetes metrics-based alerts to detect when regular VMs were provisioned by mistake, helping avoid accidental cost increases.

## Skills:
- DevOps
- FinOps

## Tools:
- Kubernetes
- Gatekeeper
