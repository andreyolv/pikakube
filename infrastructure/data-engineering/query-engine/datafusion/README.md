[← Query engine](../README.md)

# Apache DataFusion

<https://github.com/apache/datafusion>
<https://github.com/apache/datafusion-python>
<https://github.com/apache/datafusion-ballista>

---

> **A library, not a service.** DataFusion is an embeddable query engine — you build tools with
> it, you do not deploy it.

## What it is

A fast, extensible query engine written in Rust, built on Arrow: SQL parsing, a logical and
physical planner, and vectorised execution — as a **library**.

That is why it matters far beyond its own name: an increasing share of the tools in this
repository are built on it.

| Built on DataFusion | Where |
|---|---|
| [DataFusion Comet](../../processing/spark/spark-accelerator/datafusion-comet/README.md) | Spark accelerator |
| [Blaze](../../processing/spark/spark-accelerator/blaze/README.md) | Spark accelerator |
| [Arroyo](../../../data-streaming/processing/arroyo/README.md) | stream processing |
| A growing set of databases and query tools | |

Knowing that explains their shared behaviour — the same execution characteristics, the same
Arrow memory model, and often the same gaps.

## The related projects

| Project | What it is |
|---|---|
| [datafusion-python](https://github.com/apache/datafusion-python) | Python bindings — query Parquet and Arrow without a server |
| [Ballista](https://github.com/apache/datafusion-ballista) | **distributed** DataFusion, the closest thing here to a deployable cluster |

## When it is relevant

- **building** a data tool that needs SQL, rather than deploying one
- understanding why the tools above behave as they do
- Python-side embedded querying, where [DuckDB](../../processing/duckdb/README.md) is the more mature alternative

## When it is not

- you need a query engine to run — [Trino](../trino-gateway/README.md) is the deployable answer
- single-node analytics in Python — DuckDB has more features and far more material

---

## Notes

> No Helm chart — <https://github.com/apache/datafusion/issues/2397>

Which follows from what it is: a library does not have a deployment. Ballista is the part that
would, and it is much earlier than Trino for that role.

## Why it is worth tracking

The interesting question is not whether to deploy DataFusion. It is that **the execution layer
of the data ecosystem is converging on Rust and Arrow**, and this is where a large part of that
is happening.

Tools adopting it inherit its performance characteristics and its limitations at the same time —
which is useful to know when [evaluating an accelerator](../../processing/spark/spark-accelerator/README.md)
and finding the same operators unsupported in two of them.

---

[← Query engine](../README.md)
