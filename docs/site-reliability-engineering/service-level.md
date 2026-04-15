# Service Level Indicators for Data Platforms on Kubernetes and Cloud
## Problem:
- Lack of Reliability Metrics: Data pipelines and data services had no clear, measurable indicators to define what “healthy” or “reliable” meant.
- Reactive Incident Handling: Issues in data ingestion, processing, and availability were detected only after downstream consumers were impacted.
- Misalignment Between Teams: Data engineers, platform teams, and stakeholders had different expectations of data freshness, availability, and correctness.
- Hidden Infrastructure Bottlenecks: Performance issues in Kubernetes workloads, storage, or networking were hard to correlate with data pipeline failures.
- No Error Budget Awareness: Teams lacked visibility into how much unreliability was acceptable before changes became risky.

## Solution:
- Defined SLIs by Infrastructure Component: Established explicit SLIs per layer of the data platform.
- Standardized SLI Templates: Created reusable SLI definitions per component type, ensuring consistency across clusters and environments.
- Proactive Monitoring and Alerting: Built alerts based on SLI degradation instead of raw infrastructure metrics, enabling earlier and more meaningful incident detection.
- Error Budget Visibility: Used SLI data to calculate error budgets and guide operational decisions, balancing reliability and delivery speed.
- Improved Root Cause Analysis: Correlated SLI breaches with infrastructure-level metrics to quickly identify whether failures originated in compute, storage, or networking.
- Declarative and Versioned Configuration: Managed SLI definitions and thresholds as code, aligned with Kubernetes and GitOps practices.
- Better Stakeholder Communication: Provided clear, objective reliability signals to data consumers and business teams.
- Increased Platform Reliability: Reduced unexpected data incidents and improved trust in the data platform through measurable reliability guarantees.

## Skills:


## Tools:

Definir Indicadores de Nível de Serviço para componentes de Infraestrutura
