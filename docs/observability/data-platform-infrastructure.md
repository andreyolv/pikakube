# Data Infrastructure Monitoring with Synthetic Baseline Workload

## Problem:
- Data Infrastructure Monitoring: With complex data applications running on kubernetes environments, it's crucial to have a reliable method to monitor the health and performance of the data infrastructure. The challenge lies in creating realistic, reproducible workloads that can serve as benchmarks for the system’s stability and performance.
- Lack of Baseline Workloads: There were no predefined, standardized workloads to simulate data applications like Airflow DAGs, Kafka producers, and consumers. Without these mock workloads, it was difficult to assess the system’s capacity and response under varying loads and conditions.

## Solution:
- Mock Workloads for Baseline Monitoring: Developed mock workloads simulating real-world scenarios for Airflow DAGs, Kafka producers, and consumers. These workloads were designed to mimic typical processing tasks, allowing for performance benchmarking and health checks.
- Airflow DAGs for Health Checks: Created specific DAGs within Airflow that simulate regular tasks, including data processing pipelines and system integrations. These DAGs ran in intervals to simulate job execution, providing a clear performance baseline for DAG execution times and failure rates.
- Kafka Producer and Consumer Simulation: Developed mock Kafka producers and consumers to simulate high-throughput message generation and consumption, enabling the assessment of Kafka broker performance, message throughput, and latency under various load conditions.
- Automated Performance and Health Monitoring: Integrated the mock workloads with automated monitoring systems to continuously track performance metrics such as resource utilization, response times, and failure rates. This data helped identify infrastructure weaknesses and predict potential issues.

## Skills:
- Data Engineering
- Data Streaming
- DevOps
- Site Reliability Engineering
- Observability

## Tools:
- Airflow
- Kafka
- Prometheus
- Grafana
- Kubernetes

alerta vm status notready
https://github.com/prometheus-community/yet-another-cloudwatch-exporter
