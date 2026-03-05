# Standardized Monitoring and Alerting for Airflow & Kafka Applications

## Problem:
- Lack of Monitoring Standardization: Lack of standardization among data platform users in monitoring data applications such as Airflow DAGs and Kafka producers/consumers.
- Custom Metric Requirements: The need for business-specific metrics and tailored alerts to monitor critical scenarios was not adequately addressed, leading to missed insights and delayed responses.

## Solution:
- Standardized Monitoring and Alerting Guidelines: Developed guidelines to establish consistent monitoring and alerting practices across the data platform. These guidelines targeted Apache Airflow DAGs and Kafka producers/consumers, helping users integrate monitoring as a critical component of their data solutions to enhance reliability and visibility.
- Prometheus PushGateway Integration: Introduced Prometheus PushGateway to empower users to push custom metrics directly from their data applications. Additionally, leveraged Prometheus SDK for code instrumentation, enabling the creation of business-specific metrics for greater flexibility in monitoring and alerting.
- Enablement and Adoption: Actively encouraged monitoring adoption by providing detailed documentation, practical examples, and hands-on support. This approach fostered a culture of observability among platform users, simplifying the integration of monitoring into their workflows.

## Skills:
- Data Engineering
- Observability

## Tools:
- Airflow
- Kafka
- Prometheus
