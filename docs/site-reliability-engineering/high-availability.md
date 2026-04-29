# Kubernetes High Availability: Topology Spread, Anti-Affinity, and Disruption Budgets

## Problem

- Concentrated Failure Points: Without distribution rules, Kubernetes may schedule multiple pod replicas on the same node or availability zone, leading to a total service outage if that single infrastructure component fails.

- Involuntary Downtime During Maintenance: Routine operations (such as node upgrades or cluster autoscaling) can evict too many pods simultaneously, dropping the application below the minimum capacity required to handle traffic.

- Resource Imbalance: The scheduler may cluster workloads on a subset of nodes, creating performance hotspots while other hardware remains underutilized.

- Multi-Zone Resilience Risks: A lack of geographical dispersion prevents applications from surviving a complete data center outage (zone failure), impacting high-availability SLAs.

## Solution

- Topology Spread Constraints: Implemented scheduling rules using topologySpreadConstraints to ensure pods are evenly distributed across failure domains (nodes, zones, and regions) using the maxSkew parameter.

- Pod Anti-Affinity: Applied negative affinity rules to prevent instances of the same microservice from co-existing on the same physical host, enforcing hardware-level redundancy.

- Pod Disruption Budgets (PDB): Defined "interruption budgets" (using minAvailable or maxUnavailable) to guarantee that a minimum number of replicas remain operational during voluntary disruptions like node drains or cluster updates.

- Skew & Quorum Management: Balanced strict dispersion with operational flexibility, ensuring the cluster maintains quorum for stateful applications and critical services during scaling events.

- Topology-Aware Scheduling: Configured the scheduler to recognize standard topology labels (e.g., topology.kubernetes.io/zone), making the distribution logic cloud-agnostic.

- Lifecycle Resilience: Protected the application layer against aggressive evictions from the Cluster Autoscaler or Descheduler, maintaining a consistent performance baseline.
