[← Exporters](../README.md)

# YACE — Yet Another CloudWatch Exporter

<https://github.com/prometheus-community/yet-another-cloudwatch-exporter>
<https://github.com/prometheus-community/helm-charts/blob/main/charts/prometheus-yet-another-cloudwatch-exporter/values.yaml>

---

## The problem it solves

Managed AWS services — RDS, S3, SQS, ALB, MSK — publish metrics to **CloudWatch**, not to a
Prometheus endpoint. So half the platform is observable in one system and the other half in
another, with no way to alert on both together.

YACE pulls CloudWatch metrics into Prometheus. Its advantage over the older CloudWatch
exporter is **tag-based discovery**: instead of listing every resource, you declare a service
and a tag filter, and it finds them — including resources created after the exporter was
configured.

## When to use it

- managed AWS services need to appear in the same dashboards and alerts as the cluster
- RDS, SQS, MSK or ALB are part of the critical path
- you want one alerting stack rather than CloudWatch alarms alongside Alertmanager

## When not to use it

- cost data is what you want — that is [cloudcost-exporter](../cloudcost-exporter/README.md), and CloudWatch is not where billing lives
- everything already runs in the cluster with native metrics

## The two things that bite

**CloudWatch API calls cost money.** Charged per request, and a naive configuration scraping
many resources frequently produces a bill that surprises people. Scrape slowly — CloudWatch
metrics are typically minute-granularity anyway, so a fast interval buys nothing.

**Delay is inherent.** CloudWatch data lags by minutes. Alerting on it needs thresholds that
account for that, or the alerts arrive late and look flaky.

---

[← Exporters](../README.md)
