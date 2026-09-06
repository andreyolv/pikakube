[← Log storage](../README.md)

# VictoriaLogs

<https://github.com/VictoriaMetrics/VictoriaLogs>
<https://github.com/VictoriaMetrics/helm-charts>

---

## The problem it solves

[The folder's central trade](../README.md#1-the-one-decision-that-matters) is what gets indexed:
everything (Elasticsearch) or only labels (Loki). VictoriaLogs takes a third position — it
indexes **every field**, but stores logs as a column-oriented structure designed for the shape
logs actually have, rather than as generic documents.

Two consequences follow, and they are the reason to look at it:

- **no label discipline to get right.** High-cardinality fields — `pod`, `request_id`,
  `trace_id` — are ordinary fields, not a design mistake. This removes the single most common
  way a Loki deployment goes wrong
- **no cluster to operate.** A single binary with no external dependency: no object storage, no
  ZooKeeper, no shard allocation, no heap to size

Query language is **LogsQL**, which starts from a filter and pipes through transformations. It
is not PromQL and it is not LogQL, so it is one more syntax for the team to learn.

## When to use it

- Loki's label model is already causing problems, or you would rather not have to think about it
- you want full-text search without operating a search cluster
- resource cost matters — the compression and memory profile are the same argument that makes
  [VictoriaMetrics](../../../metrics/storage/victoria-metrics/README.md) attractive
- you already run VictoriaMetrics, and one operational model for metrics and logs is worth more
  than mixing vendors

## When not to use it

- Grafana is the UI and the stack is otherwise Grafana's — Loki is the native fit, and the
  ecosystem's dashboards and examples assume LogQL
- object storage is the requirement. VictoriaLogs writes to **local disk** (persistent volumes),
  which is a genuine architectural difference from Loki, Quickwit and Parseable, and it changes
  how retention and capacity are planned
- you depend on the Elastic ecosystem's tooling

## The honest position

Technically it answers the folder's trade well: full-text search, high-cardinality fields, and
a fraction of the operational surface of a search cluster. What it does not have is the
ecosystem — Loki is what Grafana documentation, community dashboards and every tutorial assume.

**The clearest case for it is a VictoriaMetrics shop**, where it is not a new vendor but the
same one covering a second signal, with [VictoriaTraces](../../../tracing/storage/victoria-traces/README.md)
covering the third.

Ingestion is not the obstacle: it accepts Elasticsearch bulk, Loki push, OTLP, syslog and
journald, so [Vector](../../collector/vector/README.md), Fluent Bit and Filebeat all reach it
without replacing the collector.

---

[← Log storage](../README.md)
