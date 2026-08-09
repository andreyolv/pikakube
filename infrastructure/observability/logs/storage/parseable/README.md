[← Log storage](../README.md)

# Parseable

<https://github.com/parseablehq/parseable>

---

## The problem it solves

A log store written in Rust that stores data as **Parquet on object storage** — a single
binary, no cluster, no index to maintain.

Parquet is the detail that makes it different from everything else here. Logs stored in a
columnar analytics format are queryable by anything that reads Parquet — DuckDB, Spark, Trino
— not only by the log tool that wrote them.

For a data platform that is an unusually good fit: logs stop being a separate silo and become
another dataset in the lakehouse.

## When to use it

- a very small footprint matters — one binary, object storage, nothing else
- you want to **analyse** logs with data tooling rather than only search them
- the platform already has Parquet and object storage as first-class concepts

## When not to use it

- rich search features are the requirement — [Quickwit](../quickwit/README.md) or [OpenSearch](../opensearch/README.md)
- you want the largest community and the most examples; this is a smaller project than the alternatives
- Grafana-native log exploration is the workflow — [Loki](../loki/README.md) integrates more tightly

## The angle worth remembering

Most log tools optimise for **finding one line**. This one keeps the data in a format built
for **aggregating across many** — which is a different and often unmet need: error rates by
tenant over a quarter, request patterns by endpoint, anything that is really an analytics
question wearing a logging costume.

---

[← Log storage](../README.md)
