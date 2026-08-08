[← Log storage](../README.md)

# Loki

<https://github.com/grafana/loki>

---

## The problem it solves

Elasticsearch indexes every word in every log line, which is why it answers full-text queries
quickly and why the index frequently ends up larger than the data.

Loki inverts it: **index only labels**, store the log payload compressed in object storage,
and scan the matching streams at query time. Cost drops substantially, and the operational
burden drops with it.

That trade fits Kubernetes debugging exactly. You almost never arrive without context — an
alert or a trace already told you which service and when, so you are narrowing a stream, not
searching a corpus.

## When to use it

- **the default** for Kubernetes logs, particularly with Grafana already in place
- log storage cost is a concern, or Elasticsearch has become expensive to operate
- logs need to sit next to metrics and traces in one UI, with links between them

## When not to use it

- genuine full-text search across large volumes is the workload — [Quickwit](../quickwit/) or [OpenSearch](../opensearch/)
- logs are a product rather than a debugging aid: security hunting, compliance search, analytics over content

## The mistake everyone makes once

**High-cardinality labels.** A label per pod name, request ID, user ID or trace ID creates a
separate stream for each value, and Loki's performance collapses.

Labels are for **selecting a stream** — namespace, app, level, cluster. Anything identifying
an individual event belongs in the log line, where it is found by filtering after selection.

This is the single most common way a Loki deployment goes wrong, and it is easier to prevent
than to fix.

---

## Notes

Object storage backend: [`minio/`](minio/)

- Kubernetes monitoring Helm chart: <https://github.com/grafana/k8s-monitoring-helm>
- **Meta-monitoring** — monitoring Loki itself: <https://github.com/grafana/loki/tree/main/production/helm/meta-monitoring>
- Prebuilt dashboards: <https://github.com/grafana/loki/tree/main/production/loki-mixin-compiled/dashboards>

Meta-monitoring is worth setting up early: when the log pipeline breaks, the logs that would
tell you are the ones not arriving.

---

[← Log storage](../README.md)
