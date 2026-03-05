# Custom Metrics for Crossplane Composite Resources with Kube Metrics Server

## Problem:
- Lack of Visibility into Composite Resources: Crossplane manages infrastructure through Composite Resources (XRs), but Kubernetes' default metrics did not expose custom health or readiness statuses for these resources. This made it difficult to monitor infrastructure at a high level.
- Limited Observability for Platform Teams: Without custom metrics, platform engineers had to rely on manual inspection or ad-hoc scripts to track XR status, increasing operational overhead and decreasing reliability.
- Inefficient Alerting and Scaling: Due to the absence of metric-based monitoring, it was not possible to configure alerting or auto-scaling based on the state of the infrastructure defined via Crossplane.

## Solution:
- Custom Metrics via Kube Metrics Server Extension: Implemented a custom metrics pipeline that exposes status and condition fields from Composite Resources (XRs) through the Kubernetes Metrics API. This allowed metrics like Ready, Synced, or Healthy to be queried programmatically.
- Metric Adapter for Composite Resource Monitoring: Built and deployed a custom metrics adapter to convert XR status conditions into Prometheus-compatible metrics. These were exposed via the Kubernetes API for seamless integration with monitoring tools.
- Enhanced Observability and Alerting with Prometheus & Grafana: Integrated the custom metrics with Prometheus and Grafana to visualize the health of infrastructure resources in real time. Enabled teams to set alerts for failing or degraded XRs, improving response time and reliability.
- Improved Platform Reliability: The visibility into Crossplane resources helped the platform team proactively monitor infrastructure changes and ensure successful provisioning, leading to more stable and transparent operations.

## Skills:
- 

## Tools:
- 

