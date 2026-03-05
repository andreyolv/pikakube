# Monitoring Software Delivery and Security Signals using Git Data

## Problem:
- Limited Visibility into Engineering Activity: Commits, pull requests, and review activity are often spread across repositories, making it difficult to understand team throughput and collaboration patterns.
- Lack of Engineering Health Signals: Without aggregated Git data, it’s hard to identify bottlenecks such as long PR cycle times, low review participation, or uneven workload distribution.
- Security Signal Fragmentation: GitHub Advanced Security findings (secret scanning, dependency vulnerabilities, code scanning) are usually analyzed in isolation, reducing their operational value.
- Delayed Risk Detection: Vulnerabilities, leaked secrets, or risky changes may go unnoticed without centralized tracking and historical context.
- Manual and Reactive Analysis: Engineering and security insights often rely on ad-hoc queries or manual dashboards, limiting consistency and scalability.
- Disconnected from Platform Observability: Git activity and security signals are rarely correlated with platform incidents or delivery performance.

## Solution:
- Centralized Git Data Ingestion: Collected and normalized Git metadata including commits, pull requests, reviews, merges, and contributors across multiple repositories.
- Engineering Activity Metrics: Derived metrics such as commit frequency, PR lead time, review latency, merge rates, and contributor activity to understand delivery flow and collaboration health.
- GitHub Advanced Security Integration: Ingested security signals from secret scanning, dependency alerts, and code scanning to track security posture over time.
- Historical Trend Analysis: Stored Git and security data to enable trend analysis, anomaly detection, and long-term insights rather than point-in-time views.
- Team and Repository Segmentation: Enabled filtering by team, repository, and service to support both platform-wide visibility and team-level ownership.
- Operational and Security Alignment: Correlated engineering activity data with security findings to highlight high-risk repositories, critical paths, and areas requiring attention.
- Declarative and Automatable Pipelines: Built repeatable ingestion and transformation pipelines, allowing easy onboarding of new repositories and organizations.
- Actionable Insights: Provided clear signals to support engineering leadership, platform teams, and security teams without turning metrics into performance micromanagement.

## Skills:
- 

## Tools:
- 

git exporter prometheus 
https://github.com/githubexporter/github-exporter
https://github.com/promhippie/github_exporter
n tem métrica de vulnerabilidade

plugin grafana tbm não https://github.com/grafana/github-datasource/issues/157
sem muita alternativa a não ser burrice

api do github direto no grafana
https://github.com/grafana/grafana-infinity-datasource

porém não tem autenticação para github app
https://github.com/grafana/grafana-infinity-datasource/discussions/1266