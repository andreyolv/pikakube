# Real-Time Data Streaming with Confluent Cloud

## Problem:
- Data Ingestion Latency: Traditional data pipelines often encounter significant latency, hindering real-time insights and decision-making.
- Operational Complexity: Managing on-premise Kafka clusters introduces high complexity, especially in distributed systems that require high availability and fault tolerance.
- Azure Integration with Confluent Cloud: Integrating Confluent Cloud with Azure in a hub-and-spoke network topology presents a challenge. This network architecture is commonly used to centralize control, simplifies security, traffic management, and isolation between environments.

## Solution:
- Azure VNet Peering Limitation: Azure does not support transitive VNet peering, meaning that when Network A is peered with Network B, and Network B is peered with Confluent Cloud, applications in Network A cannot access Confluent Cloud. This limitation halted the initial integration plan, as Azure was the mandated cloud provider for the project. AWS does not have this restriction, but switching to AWS was not an option.
- Kafka on Kubernetes: To bypass this limitation, Kafka was deployed on Kubernetes using Strimzi, a Kubernetes operator designed to simplify Kafka cluster management. This solution provided an alternative, scalable, and flexible architecture for real-time data streaming, enabling continued operations while avoiding Azure's network constraints.

## Skils:
- Data Engineering
- Data Streaming

## Tools:
- Confluent Cloud
- Microsoft Azure
- Kafka