[← Performance analysis](../README.md)

# DataFlint

<https://github.com/dataflint/spark>
<https://dataflint.gitbook.io/dataflint-for-spark>
<https://mvnrepository.com/artifact/io.dataflint/spark>

---

## What it does

An open-source Spark UI plugin that **identifies problems** rather than only displaying data.

The standard UI shows that a stage took twenty minutes. DataFlint says the job read 40,000
files averaging 200 KB, or that one task processed forty times the median, and explains what
that means.

| Detects | Which is |
|---|---|
| **Small files** | the most common lakehouse performance problem |
| **Skew** | one partition doing most of the work |
| Spill | memory pressure forcing shuffle to disk |
| Wasted resources | executors requested and not used |
| Inefficient queries | plans with avoidable shuffles or scans |

## When to use it

- a job is slow and the Spark UI has not made the reason obvious
- teaching people to read Spark performance — the explanations are genuinely instructive
- routine review of important jobs, rather than only during incidents

## When not to use it

- you need programmatic measurement for benchmarking — [sparkMeasure](../spark-measure/README.md)
- you need continuous metrics across all jobs — [spark-dashboard](../spark-dashboard/README.md)

## Installation

Added as a Spark plugin via the JAR from
[Maven Central](https://mvnrepository.com/artifact/io.dataflint/spark), then enabled in the
Spark configuration. No change to job code.

## On small files

The problem it is best at surfacing, and the one worth understanding:

[Fixing small files performance issues in Apache Spark, using DataFlint](https://www.youtube.com/watch?v=BqnI39c8GKc) ·
[author's writing](https://medium.com/@menishmueli)

The cause is almost never Spark. It is how the data was written — usually a streaming job
producing one file per micro-batch. The fix is compaction and table maintenance, which lives
with [file formats](../../../../file-formats.md) and the table formats in
[`data-governance/`](../../../../../data-governance/).

DataFlint's value is making that visible from the consuming side, where the pain is felt.

---

[← Performance analysis](../README.md)
