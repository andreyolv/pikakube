[← Spark accelerators](../README.md)

# Apache Gluten

<https://github.com/apache/incubator-gluten>
<https://gluten.apache.org/>

---

## What it is

A Spark plugin that offloads execution to a **native engine** — Velox or ClickHouse — while
keeping Spark's API, optimiser and ecosystem. Same PySpark code, executed natively underneath.

## Why it is the practical choice here

**It supports Delta and Iceberg**, which the DataFusion-based alternatives do not yet:

- [Delta support](https://gluten.apache.org/docs/velox/getting-started#deltalake-support)
- [Iceberg support](https://gluten.apache.org/docs/velox/getting-started#iceberg-support)

For a lakehouse that decides it. An accelerator that cannot read the table format the platform
is built on is not a candidate, whatever its benchmarks say.

## When to use it

- Spark jobs are CPU-bound and the workload is stable enough to justify tuning
- the lakehouse uses Delta or Iceberg
- you can measure the fallback rate on real jobs before committing

## When not to use it

- jobs are small — [DuckDB](../../../duckdb/README.md) is the better answer
- the workload is IO-bound; native execution does not help
- the plan falls back constantly, which is measured rather than assumed

## Getting started

[Using the released JAR](https://github.com/apache/incubator-gluten?tab=readme-ov-file#31-use-released-jar)
— the fastest path to testing it, without building from source.

## How to evaluate

Read the physical plan and count what runs natively versus what falls back to the JVM. A plan
with frequent fallbacks performs **worse** than plain Spark, because it pays conversion costs
between the two representations at every boundary.

That number is the whole evaluation. Benchmarks avoid the operators that fall back; your jobs
will not.

---

[← Spark accelerators](../README.md)
