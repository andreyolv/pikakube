[← Spark](../README.md)

# Performance analysis

Finding out **why** a job is slow, rather than guessing.

Tools covered: [`dataflint`](dataflint/README.md) · [`spark-measure`](spark-measure/README.md) ·
[`spark-dashboard`](spark-dashboard/README.md)

---

## The gap these fill

The [history server](../spark-history-server/README.md) shows what happened. It does not say
what was wrong, and reading a Spark UI usefully is a skill — most people can see that a stage
took twenty minutes, and not why.

The recurring causes are a short list, and each has a signature:

| Problem | Signature in the UI |
|---|---|
| **Small files** | thousands of tasks, each reading almost nothing |
| **Skew** | one task in a stage takes far longer than the median |
| **Spill** | shuffle spill to disk, and memory pressure |
| Wrong partition count | too few tasks (no parallelism) or too many (scheduling overhead) |
| Cartesian join | task count and shuffle size explode without explanation |
| Over-provisioning | executors idle, memory unused — invisible in the standard UI |

These tools recognise those signatures automatically, which is the difference between "the job
is slow" and "there are 40,000 files averaging 200 KB".

## The tools

| Tool | What it does | Detail |
|---|---|---|
| **DataFlint** | a UI plugin that **flags problems** — small files, skew, spill — with explanations | [→](dataflint/README.md) |
| **sparkMeasure** | measures a job's metrics from code, for benchmarking and comparison | [→](spark-measure/README.md) |
| **spark-dashboard** | exports Spark metrics to Prometheus and Grafana | [→](spark-dashboard/README.md) |

They answer different questions:

- **DataFlint** — "what is wrong with this job?" Interactive, and the fastest route to a cause
- **sparkMeasure** — "is version B faster than version A?" Programmatic, for measurement rather than diagnosis
- **spark-dashboard** — "how do all jobs behave over time?" Continuous, and lands in the same [observability](../../../../observability/README.md) stack as everything else

## The order to use them

1. **spark-dashboard** running continuously, so trends and regressions are visible
2. **DataFlint** when a specific job is slow — it names the cause
3. **sparkMeasure** when changing something and needing to prove the change helped

## The one that matters most

**Small files.** It is the most common performance problem in a lakehouse, and it originates
outside Spark — in how data was written, usually by a streaming job.

Fixing it is compaction and table maintenance, not Spark tuning. See
[file formats](../../../file-formats.md) and the table formats in
[`data-governance/`](../../../../data-governance/).

---

[← Spark](../README.md)
