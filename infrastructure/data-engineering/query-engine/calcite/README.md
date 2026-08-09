[← Query engine](../README.md)

# Apache Calcite

<https://github.com/apache/calcite>
<https://calcite.apache.org/>

---

> **A framework, not an engine.** Calcite parses, plans and optimises SQL. It does not execute
> it and does not store anything.

## What it is

The SQL front end that a large part of the JVM data ecosystem is built on: a parser, a
validator, a relational algebra representation, and a cost-based optimiser — provided as a
library.

Systems built with it include Flink SQL, Hive, Druid, Beam SQL and many others. When two
unrelated tools accept the same slightly-unusual SQL dialect, this is usually why.

| Component | What it does |
|---|---|
| Parser | SQL text to an abstract syntax tree |
| Validator | resolves names and types against a schema |
| **RelNode** | relational algebra — the intermediate representation |
| Optimiser | rule-based and cost-based plan rewriting |
| Adapters | expose an external system as a queryable source |

## When it is relevant

- **building** a system that needs SQL — a query layer over something custom
- adding SQL to a database or engine that does not have it
- understanding why Flink SQL, Hive and Druid share dialect quirks

## When it is not

- you need a query engine to deploy — [Trino](../trino-gateway/README.md) or [Dremio](../dremio/README.md)
- embedded analytics in a program — [DataFusion](../datafusion/README.md) or [DuckDB](../../processing/duckdb/README.md) are the modern equivalents

---

## Notes

> No Helm chart, and the documentation is poor.

The first is expected — it is a library, and libraries do not deploy.

The second is a genuine obstacle. Calcite is powerful and its documentation assumes substantial
prior knowledge of query planning, which makes the learning curve steep in a way that is not
about the concepts themselves.

## Why it is mapped here

Alongside [DataFusion](../datafusion/README.md), it explains a structural fact about this ecosystem:
**most query engines are assembled from a small number of shared components**.

Calcite is the JVM answer, DataFusion the Rust one, and knowing which a tool is built on
predicts a surprising amount — its SQL dialect, its optimiser behaviour, and which operators it
will and will not support.

---

[← Query engine](../README.md)
