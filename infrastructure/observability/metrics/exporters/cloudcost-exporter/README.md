[← Exporters](../README.md)

# Cloud Cost Exporter

<https://github.com/grafana/cloudcost-exporter>
<https://github.com/grafana/helm-charts/blob/main/charts/cloudcost-exporter/values.yaml>

---

## The problem it solves

Cost lives in a billing console, updated daily, disconnected from everything else. Nobody
correlates a deploy with the bill, because the two live in different tools on different
timescales.

This exports cloud pricing and cost data into Prometheus, so cost becomes a series like any
other — graphable next to the workload that caused it, and alertable when it moves.

## When to use it

- cost should appear on the same dashboards as the metrics that explain it
- you want to alert on **cost anomalies** rather than discover them in the monthly invoice
- correlating a change in spend with the deploy or scaling event that caused it

## When not to use it

- full FinOps attribution by namespace, team or project — that is
  [OpenCost/Kubecost](../../../../finops/README.md) and it is a different tool for a different question
- cloud provider metrics rather than cost — [AWS](../aws-exporter/README.md) or [Azure](../azure-exporter/README.md)

## Where it sits against FinOps

| Question | Where |
|---|---|
| What does this cloud resource cost? | **here** |
| What does this namespace or team cost? | [`finops/`](../../../../finops/README.md) |
| Why did cost change at 14:00 yesterday? | **here**, correlated with metrics |

The third row is what this adds and the FinOps tools do not: cost on the same timeline as
deploys, scaling events and traffic, in the same query language.

## Related

Spot pricing has its own exporters: [spot-price](../spot-price-exporter/README.md) and
[spot-termination](../spot-termination-exporter/README.md).

---

[← Exporters](../README.md)
