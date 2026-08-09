[← Data quality](../README.md)

# Deequ

<https://github.com/awslabs/deequ>
<https://github.com/awslabs/python-deequ>

---

## The problem it solves

Data quality **on Spark, at volume**, from AWS Labs. Its distinguishing property is how it
computes:

**All metrics in a single pass.** Deequ compiles a set of constraints into one aggregation over
the data, so checking twenty things costs one scan rather than twenty. On a table large enough to
matter, that is the difference between a check that runs and one that gets removed for being too
slow.

| Capability | Detail |
|---|---|
| **Single-pass metrics** | the whole constraint set in one scan |
| **Anomaly detection** | compares today's metrics against history, rather than a fixed threshold |
| Constraint suggestion | profiles the data and proposes constraints |
| **Metrics repository** | metric history persisted, which is what makes anomaly detection possible |
| Native Spark | it is a Spark library, not a wrapper around one |
| PyDeequ | the Python binding |

## Anomaly detection is the real differentiator

Every other tool in [`quality/`](../README.md) checks against a value someone chose: `row_count >
1000`, `null_percent < 5`.

Those thresholds are wrong on the first day of unusual traffic, and they are the reason quality
alerts get muted.

Deequ persists metrics over time and compares the current run against that history — a relative
change, a rate of change, or a value outside the recent distribution:

```
row count is 40% below the trailing average  →  fail
```

That catches the failure nothing else does: **the pipeline that ran successfully and produced
half the usual data.** Row count above zero, no nulls, every fixed threshold satisfied, and the
data is wrong.

## When to use it

- **Spark is the processing engine**, and the data is large enough that scan count matters
- checking many constraints, where single-pass execution is a real saving
- **anomaly detection against history** is wanted rather than fixed thresholds
- the checks belong inside the Spark job that produces the data

## When not to use it

- the data is in a warehouse, queried with SQL — [Soda](../soda/README.md) runs there directly
- checks should be readable by analysts — this is Scala, or PyDeequ's Python API
- pandas — [Pandera](../pandera/README.md)
- there is no Spark; adding it for quality checks would be absurd
- unit-testing transformations — [chispa](../chispa/README.md)

## The practical caveats

| Concern | Detail |
|---|---|
| **JVM library** | PyDeequ wraps it; version alignment between Spark, Deequ and PyDeequ is a real friction point |
| **Metrics repository** | anomaly detection needs somewhere to persist history — a file system or object storage |
| Spark version coupling | Deequ releases track specific Spark versions closely |
| Verbosity | the constraint API is more code than a YAML equivalent |
| Maintenance | an AWS Labs project; active, and not a product with a roadmap |

The version-alignment row is the one that costs time in practice. A Spark upgrade can require a
Deequ upgrade, and PyDeequ's compatibility matrix is the thing to check before either.

## Notes

Reference kept here:
[a practical walkthrough with Spark and Deequ](https://medium.com/data-hackers/qualidade-de-dados-na-pr%C3%A1tica-com-spark-e-aws-deequ-ec8127979ee).

For this platform it is the **Spark-side** answer, alongside [Soda](../soda/README.md) for the
warehouse side —
[Spark is genuinely deployed here](../../../data-engineering/processing/spark/README.md), with the
Kubernetes operator and the performance tooling mapped.

The division worth keeping clear, since three tools in this folder touch Spark:

| Tool | Job |
|---|---|
| **Deequ** | validating **data**, at scale, inside the job |
| [chispa](../chispa/README.md) | unit-testing the **transformation**, on fixtures |
| [Soda](../soda/README.md) | validating data in the **warehouse**, after it lands |

And the capability worth borrowing regardless of tool: **anomaly detection against history beats
fixed thresholds**, because the thresholds are what get muted.

---

[← Data quality](../README.md)
