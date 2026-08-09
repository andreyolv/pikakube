[← Notebooks](../README.md)

# Hue

<https://github.com/cloudera/hue>
<https://gethue.com/>

---

> **A SQL workbench, not a notebook.** It is in this folder because it serves the same audience
> — people exploring data — through a different interface.

## The problem it solves

Analysts who work in SQL do not want a Python environment. They want to browse tables, read the
schema, write a query, see the result, and export it.

Hue is that: a web workbench for querying and browsing a data platform, with an editor,
autocomplete against the catalogue, result export, and a file browser for object storage.

| Feature | Detail |
|---|---|
| SQL editor | autocomplete driven by the actual catalogue, and query history |
| **Table browser** | schemas, columns, partitions and sample data without writing SQL |
| Multi-engine | Hive, Impala, Trino, Spark SQL, and JDBC sources |
| File browser | HDFS and S3-compatible storage |
| Job browser | query and job status |

The table browser is what people actually use it for. "What columns does this table have and
what is in it" is the most common question on a data platform, and answering it without writing
SQL removes a lot of friction.

## When to use it

- **SQL-only analysts** need access to a lakehouse or warehouse
- schema discovery is a real problem — people cannot find what exists
- Hadoop-ecosystem engines are in use, where it is the native tool

## When not to use it

- Python exploration is the workflow — [Jupyter](../jupyter/README.md)
- dashboards are what people want — [`viz/`](../../viz/README.md)
- the platform is not Hadoop-adjacent; the tooling assumes that ecosystem

## Where it overlaps

Superset's SQL Lab covers much of the same ground, and if [Superset](../../viz/superset/README.md) is
already deployed it is usually the simpler answer — one tool for querying and dashboards.

Hue's advantage is the **browsing** experience: it is better at exploring what exists, which is
a different question from querying what you already know about.

For discovery as a governed capability rather than a UI feature, see
[`data-governance/`](../../../data-governance/) — a catalogue answers "what exists and who owns
it" more durably than a browser does.

---

[← Notebooks](../README.md)
