# Kubernetes Metrics Collection and Storage with Prometheus

## Problem:
- High Volume of Infrastructure Metrics: Kubernetes clusters and workloads continuously emit large amounts of metrics, making raw metric collection and storage complex without a dedicated system.
- Lack of Centralized Metrics Backend: Without a standardized metrics platform, teams struggle to query, correlate, and analyze infrastructure behavior over time.
- Limited Visibility into Cluster Internals: Core components such as kubelet, API server, scheduler, and controller manager expose critical metrics that are often underutilized or inconsistently collected.
- Inconsistent Metric Definitions: Different teams and workloads expose metrics in varying formats, complicating aggregation and long-term analysis.
- Scalability Challenges: As clusters and workloads grow, metrics systems must scale efficiently without impacting cluster performance.

## Solution:
- Prometheus Operator Deployment: Deployed Prometheus using the Prometheus Operator to manage lifecycle, configuration, and upgrades declaratively through Kubernetes CRDs.
- Standardized Metrics Scraping: Defined ServiceMonitors and PodMonitors to consistently collect metrics from Kubernetes core components and workloads.
- Infrastructure Metrics Coverage: Collected metrics from kube-state-metrics, node-exporter, and Kubernetes control plane components to provide full infrastructure visibility.
- Efficient Metrics Storage: Tuned retention policies, scrape intervals, and resource allocation to balance metric granularity with storage and performance requirements.
- Multi-Environment Consistency: Applied the same Prometheus configuration patterns across development, staging, and production clusters using GitOps practices.
- Secure Metrics Access: Scoped metric scraping and access using RBAC and namespace isolation to ensure least-privilege observability.
- Extensible Architecture: Enabled easy onboarding of new workloads and exporters by following standardized labeling and metric conventions.

## Skills:
- DevOps
- Site Reliability Engineering
- Observability

## Tools:
- Prometheus
- Grafana
- Kubernetes

armazenar apenas métricas importantes, o resto dropar com justificativa. malha fina, porém sem muito valor agregado, mas o ideal
