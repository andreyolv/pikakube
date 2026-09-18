# Software Delivery Performance Metrics (DORA) with Apache DevLake

## Problem:
- Fragmented Delivery Data: Engineering delivery information is scattered across GitHub, issue trackers, CI pipelines and deployment tooling, with no common model to join them.

- No Objective DORA Metrics: Lead time for changes, deployment frequency, change failure rate and time to restore were estimated from perception or surveys instead of being derived from real events.

- Invisible Delivery Bottlenecks: Slow code reviews, long-lived pull requests and queued deployments were felt by the team but could not be quantified or prioritized.

- Platform Value Hard to Justify: Platform and automation work was argued in technical terms only, without evidence of its impact on how fast and how safely the organization ships software.

- Manual and Inconsistent Reporting: Delivery reports were built by hand from ad-hoc queries, making them inconsistent over time and impossible to compare across teams or repositories.

- Disconnected from Platform Observability: Infrastructure dashboards showed whether the system was healthy, but nothing showed whether the engineering process itself was healthy.

## Solution:
- Apache DevLake on Kubernetes: Deployed Apache DevLake with its official Helm chart, managed declaratively through GitOps in a dedicated namespace alongside the other dashboard tooling.

- Multi-Source Ingestion: Configured connections to source systems (GitHub as the first connector via GitHub App authentication) to collect commits, pull requests, reviews, issues, pipelines and deployments.

- Normalized Delivery Domain Model: Relied on the DevLake domain layer to normalize heterogeneous source data into a common schema, allowing consistent metrics regardless of the tool of origin.

- Out-of-the-Box DORA Dashboards: Used the bundled Grafana instance and DORA dashboards to expose lead time for changes, deployment frequency, change failure rate and time to restore service.

- Historical Trend Analysis: Persisted collected data so delivery performance is analyzed as a trend over months rather than as a point-in-time snapshot.

- Team and Repository Segmentation: Scoped collection per project and repository, supporting both an organization-wide view and drill-down into specific services.

- Evidence for Platform Investment: Turned platform initiatives into measurable outcomes by correlating changes in tooling and process with movement in delivery metrics.

- Healthy Metrics Culture: Positioned DORA metrics as a signal about the system and the process, explicitly not as individual performance targets, avoiding gaming and misuse.

## Skills:
- DevOps
- Platform Engineering
- Observability
- Engineering Management

## Tools:
- Apache DevLake
- Grafana
- GitHub
- Kubernetes
- Helm
- Flux
