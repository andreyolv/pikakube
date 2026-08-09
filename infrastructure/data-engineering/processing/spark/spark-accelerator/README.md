[← Spark](../README.md)

# Spark accelerators

Replacing Spark's JVM execution path with native engines.

Tools covered: [`gluten`](gluten/README.md) · [`datafusion-comet`](datafusion-comet/README.md) ·
[`blaze`](blaze/README.md) · [`lakesail`](lakesail/README.md)

---

## The problem they solve

Spark's execution runs on the JVM, row-by-row through generated Java code. That is portable and
leaves performance on the table: no SIMD, garbage collection pauses, and memory layouts that do
not suit columnar data.

Accelerators intercept the physical plan and execute it in a **native, vectorised engine** —
usually Velox or DataFusion — while keeping Spark's API, catalyst optimiser and ecosystem.

The promise is a substantial speedup with **no application change**: the same PySpark code,
executed differently underneath.

## The catch that decides adoption

**Not every operator is supported.** When the native engine cannot handle part of the plan, it
falls back to the JVM — and a plan that falls back constantly performs worse than plain Spark,
because it pays for conversion between the two representations.

So the real question is never "how fast is it" — it is **"how much of my actual workload runs
natively?"** That is measured, not read from a benchmark.

The second question is **table format support**, and it is where these currently differ most:

| Accelerator | Delta and Iceberg |
|---|---|
| [Gluten](gluten/README.md) | **supported** |
| [DataFusion Comet](datafusion-comet/README.md) | **not yet** — [#174](https://github.com/apache/datafusion-comet/issues/174) · [#329](https://github.com/apache/datafusion-comet/issues/329) |

For a lakehouse that is decisive rather than a detail.

## The tools

| Tool | Engine | Notes | Detail |
|---|---|---|---|
| **Apache Gluten** | Velox / ClickHouse | supports Delta and Iceberg — the practical choice for a lakehouse | [→](gluten/README.md) |
| **DataFusion Comet** | DataFusion (Rust) | Apache, promising, no Delta or Iceberg yet | [→](datafusion-comet/README.md) |
| **Blaze** | DataFusion (Rust) | from Kuaishou, same approach | [→](blaze/README.md) |
| **LakeSail** | its own engine | **not an accelerator** — a separate engine with a Spark-compatible API | [→](lakesail/README.md) |

**LakeSail is the odd one.** It is not accelerating Spark; it is a replacement that speaks the
same API. That is a different bet, with a different risk profile — see its README.

## How to evaluate one

1. take a **real** job, not a benchmark
2. run it with the accelerator, and read the plan
3. count the fallbacks — that number is the actual answer
4. verify the table format works, before anything else

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Adopting from a benchmark | benchmarks avoid the operators that fall back | test your own plans |
| Ignoring the fallback rate | constant conversion is slower than plain Spark | read the plan |
| Assuming Delta/Iceberg works | it does not, for some of these | check first |
| Accelerating a job that should not be distributed | making the wrong tool faster | [DuckDB](../../duckdb/README.md) |

---

[← Spark](../README.md)
