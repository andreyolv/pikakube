[← OpenTelemetry platforms](../README.md)

# SigLens

<https://github.com/siglens/siglens>
<https://github.com/siglens/charts>

---

## What it is

An observability platform positioned almost entirely on **ingest efficiency** — the claim
being an order-of-magnitude reduction in the compute needed to ingest and query the same
telemetry compared to Elasticsearch or Splunk.

Metrics, logs and traces in one system, with OTLP ingestion.

## When to use it

- **ingest cost is the constraint** and the volume is large enough for efficiency claims to matter in currency
- you want to evaluate a smaller, newer entrant against the established options
- a lean footprint is more important than feature breadth

## When not to use it

- you want the most complete open-source platform — [SigNoz](../signoz/) covers more and has a larger community
- production dependence without evaluation; this is a younger project than the alternatives

## How to evaluate it honestly

Efficiency claims are the entire pitch, so test the claim rather than the feature list. The
[OpenTelemetry Collector](../../../tracing/collector/opentelemetry/) makes that
straightforward: add a second exporter, send the same production telemetry to both, and compare
resource use and query behaviour on identical data.

That is the cheap way to make this decision with evidence instead of benchmarks published by
the vendor — and it works for every platform in this folder.

---

[← OpenTelemetry platforms](../README.md)
