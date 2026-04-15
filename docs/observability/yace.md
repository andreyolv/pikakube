# AWS Infrastructure Observability with YACE and Prometheus

## Problem

- Tooling Fragmentation: The team uses a Kubernetes-native stack (Prometheus/Grafana), but AWS managed services (RDS, SQS, ELB) are "locked" in CloudWatch, forcing engineers to jump between different UIs and query languages (PromQL vs. CloudWatch Logs Insights).

- Manual Dashboard Toil: Creating dashboards manually in the AWS Console is slow, hard to version control, and impossible to scale across multiple environments (Dev/Staging/Prod) using GitOps.

- Alerting Silos: Managing alerts in two different places (CloudWatch Alarms and Alertmanager) creates inconsistent notification flows and increases the risk of "missing" a production incident due to fragmented routing.

- API Throttling & Costs: Standard exporters often hit AWS API limits when discovery is not optimized, causing gaps in metrics and increasing infrastructure overhead.

- Static Configuration: Lack of automated discovery for AWS resources means monitoring often lags behind new infrastructure deployments, requiring manual intervention to update scrapers.

## Solution

- YACE Implementation: Deployed "Yet Another Cloudwatch Exporter" to bridge the gap between AWS CloudWatch and Prometheus using a declarative configuration.

- Optimized Metrics Scrapping: Configured YACE's resource discovery and scraping intervals to balance metric freshness with AWS API cost optimization.

- Multi-Service Coverage: Standardized the collection of metrics for RDS (Performance), SQS (Queue Depth), ELB (Latency/Error Rates), and Lambda (Invocations/Errors).

- Dynamic Resource Discovery: Leveraged AWS Tags to automatically discover and monitor new resources without manual configuration updates.

- Unified Alerting with Alertmanager: Integrated CloudWatch metrics into the Prometheus Alertmanager pipeline, ensuring consistent notification routing (Slack) for both EKS and AWS managed services.

- Enhanced Grafana Dashboards: Built unified dashboards that correlate Kubernetes application performance with the underlying AWS managed resources.
