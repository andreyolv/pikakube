# Kubernetes Log Centralized Storage with Loki

## Problem:
- Fragmented Logging System: Logs were scattered across Kubernetes pods and nodes, making it difficult to centralize and manage them efficiently. This fragmentation led to slower troubleshooting and increased complexity.
- Limited Log Retention: Kubernetes does not persist logs of terminated or old pods by default, making it challenging to store and retrieve logs for debugging purposes. This limited the ability to investigate past issues that could arise from historical logs.
- High Log Storage Costs: Storing logs led to high storage costs and difficulties in long-term retention. There was a need for a scalable and cost-effective storage solution.

## Solution:
- Centralized Logging with Loki and Fluentd: Deployed Fluentd to collect logs from Kubernetes pods and forward them to Loki for centralized storage. This allowed logs from various sources to be aggregated in one place, improving visibility.
- S3 for Log Storage: Configured logs to be stored in S3, offering a scalable and cost-effective solution for long-term log retention. S3 provided flexible storage options, ensuring efficient log organization and retrieval.
- Log Querying with Grafana: Integrated Loki with Grafana to allow for efficient querying and visualization of logs. Teams could now search logs by labels, time ranges, and metadata, streamlining troubleshooting and performance monitoring.

## Skills:
- DevOps
- Site Reliability Engineering
- Observability

## Tools:
- Loki
- Grafana
- Fluentbit
- S3
