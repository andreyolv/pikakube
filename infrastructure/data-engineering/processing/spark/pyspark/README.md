[← Spark](../README.md)

# PySpark

The Python API for Spark — and the one almost everyone actually uses.

Examples: [`notebooks/`](notebooks/README.md)

---

## What to know

PySpark is a wrapper over the JVM engine. Understanding that explains most of its performance
characteristics:

| Concept | Consequence |
|---|---|
| **DataFrame API** | operations are translated to JVM plans — no Python runs per row |
| **Python UDFs** | serialise every row to Python and back. This is the main performance trap |
| **Pandas UDFs** | vectorised via Arrow — often an order of magnitude faster than a plain UDF |
| Lazy evaluation | nothing executes until an action; the plan is optimised first |
| `collect()` | brings data to the driver, and OOMs it if the data is large |

The UDF rule is the one worth internalising: **anything expressible in the DataFrame API or SQL
should be**. A Python UDF breaks the optimiser's view of the plan and pays serialisation on
every row.

When a UDF is genuinely necessary, use a Pandas UDF.

## Style

[Palantir's PySpark style guide](https://github.com/palantir/pyspark-style-guide) is the best
reference on writing PySpark that is readable and reviewable — chained transformations, naming,
and the patterns that keep a job comprehensible six months later.

Worth adopting as a convention rather than leaving to preference, because PySpark permits
several very different styles of writing the same thing.

## Understanding what it does underneath

[Apache Spark internals](https://github.com/japila-books/apache-spark-internals) — for reading
a physical plan and understanding *why* a job behaves the way it does, rather than only what it
did.

That knowledge is what makes [performance analysis](../spark-performance/README.md) actionable:
the tools point at a symptom, and the plan explains it.

## The question worth asking first

Before writing PySpark at all: **does this need Spark?**

For tens of gigabytes, [DuckDB](../../duckdb/README.md) is usually faster and needs no cluster — see
[`processing/`](../../README.md#1-the-question-to-ask-first). PySpark is the right tool when
the data genuinely does not fit, and an expensive one when it does.

---

[← Spark](../README.md)
