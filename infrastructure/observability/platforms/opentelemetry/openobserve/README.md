[← OpenTelemetry platforms](../README.md)

# OpenObserve

<https://github.com/openobserve/openobserve>
<https://github.com/openobserve/openobserve-helm-chart>

---

## The problem it solves

An OTLP-native platform built around **storage efficiency**. Its pitch is a very large
reduction in storage cost compared to Elasticsearch for the same log volume, achieved by
writing Parquet to object storage instead of maintaining inverted indexes.

That trade is the whole design: cheaper storage and much lower operational weight, in exchange
for a query model that is scan-oriented rather than index-oriented.

It also runs as a **single binary**, which is a genuine difference from platforms that need
several components before ingesting anything.

## When to use it

- **log volume is the cost problem** and Elasticsearch has become expensive to run and store
- you want object storage as the backend rather than local disks to manage
- a small footprint matters — one binary, no cluster to operate

## When not to use it

- complex full-text search across huge datasets is the primary workload; index-based engines still win there
- you want the broadest feature surface — [SigNoz](../signoz/README.md) covers more
- you need Grafana's ecosystem as the front end

## Related

Compare against [Loki](../../../logs/storage/loki/README.md), which makes a similar bet — index only
labels, store the rest cheaply. The difference is scope: Loki is a log store, this is a
platform for all three signals.

---

[← OpenTelemetry platforms](../README.md)
