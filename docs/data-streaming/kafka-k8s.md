# Event Streaming Platform on Kubernetes with Apache Kafka and Strimzi

## Problem:
- Complex Kafka Operations: Deploying and operating Apache Kafka manually is complex, requiring deep knowledge of brokers, Zookeeper/KRaft, scaling, upgrades, and fault tolerance.
- Operational Risk: Manual configuration changes and upgrades can easily lead to downtime, data loss, or unstable clusters.
- Lack of Kubernetes-Native Management: Traditional Kafka deployments do not integrate well with Kubernetes primitives such as declarative configuration, reconciliation, and self-healing.
- Scaling Challenges: Dynamically scaling brokers, topics, and partitions while maintaining performance and availability is difficult without automation.
- Security and Access Control Complexity: Managing TLS, authentication, authorization (ACLs), and secrets across Kafka components is error-prone at scale.
- Environment Inconsistency: Maintaining consistent Kafka configurations across development, staging, and production environments is challenging.

## Solution:
- Kafka on Kubernetes with Strimzi: Deployed Apache Kafka using Strimzi, a Kubernetes-native operator that manages the full Kafka lifecycle via Custom Resource Definitions (CRDs).
- Declarative Kafka Management: Defined Kafka clusters, brokers, topics, users, and ACLs as Kubernetes manifests, enabling GitOps-friendly, versioned, and auditable configurations.
- Automated Scaling and Self-Healing: Leveraged Strimzi’s reconciliation loop to automatically handle broker restarts, pod failures, and configuration drift.
- Safe Upgrades and Rolling Updates: Performed Kafka and configuration upgrades using controlled rolling updates, minimizing downtime and operational risk.
- Integrated Security by Default: Implemented TLS encryption, authentication mechanisms, and fine-grained authorization policies declaratively using KafkaUser and KafkaTopic CRDs.
- Storage and Reliability: Configured persistent storage for Kafka brokers using PersistentVolumes to ensure data durability across pod restarts and node failures.
- Multi-Environment Standardization: Reused the same Kafka definitions across environments with environment-specific overrides, ensuring consistency and reliability.
- Operational Visibility: Integrated Kafka metrics with Prometheus for monitoring broker health, throughput, lag, and cluster performance.





## Solution:
automação certificados strimzi jks

## Skills:
- Data Engineering
- Data Streaming
- Site Reliability Engineering
- DevOps
- Platform Engineering

## Tools:
- Apache Kafka
- Debezium
- Schema Registry
- Python
- Apache Spark
- Docker
- Kubernetes
- Kafka UI

migration topic and cluster, update cluster and connectors
