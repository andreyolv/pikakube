# Kubernetes Log Collection with Fluent Bit and Loki Ingestion

## Problem:
- Fragmented Log Collection: Application, system, and Kubernetes logs were scattered across nodes and containers, making troubleshooting difficult.
- Limited Observability: Difficulty correlating logs with Kubernetes resources such as pods, namespaces, and nodes.
- Operational Blind Spots: Log loss occurred during pod and node failures, reducing incident visibility.

## Solution:
- Deployed Fluent Bit as the Logging Agent: Implemented Fluent Bit as a DaemonSet to collect container, node, and system logs directly from Kubernetes.
- Kubernetes-Aware Log Enrichment: Enriched logs with Kubernetes metadata (namespace, pod, container, labels) to enable precise filtering and correlation.
- Efficient Parsing and Filtering: Applied parsers and filters to normalize log formats, reduce noise, and control ingestion costs.
- Reliable Delivery with Buffering: Configured buffering, retries, and backpressure handling to prevent log loss during backend outages.
- Improved Operational Visibility: Enabled faster troubleshooting, better incident response, and stronger auditability across clusters and environments.

## Skills:
- DevOps
- Site Reliability Engineering
- Observability

## Tools:
- Loki
- Grafana
- Fluentbit
