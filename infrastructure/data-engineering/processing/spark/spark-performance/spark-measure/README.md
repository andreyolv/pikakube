[← Performance analysis](../README.md)

# sparkMeasure

<https://github.com/LucaCanali/sparkMeasure>

---

## What it does

Measures Spark job metrics **from code** — task and stage durations, shuffle read and write,
spill, GC time, CPU time — and returns them as a dataframe you can compare.

Where [DataFlint](../dataflint/README.md) is interactive and diagnostic, this is programmatic and
comparative. It answers *"is this version faster, and by how much"* rather than *"what is
wrong"*.

```python
from sparkmeasure import StageMetrics
sm = StageMetrics(spark)

sm.begin()
# the job
sm.end()
sm.print_report()
```

## When to use it

- **benchmarking a change** — a new join strategy, a partition count, an accelerator
- proving a tuning change actually helped, with numbers rather than impressions
- regression testing performance in CI, where a job that got 40% slower should fail
- teaching, because the metrics are explicit rather than buried in a UI

## When not to use it

- diagnosing an unfamiliar slow job — DataFlint names causes, this reports numbers
- continuous monitoring across all jobs — [spark-dashboard](../spark-dashboard/README.md)

## Where it fits best

Evaluating a [Spark accelerator](../../spark-accelerator/README.md). The honest way to compare
Gluten, Comet or Blaze is the same real job measured with and without — and this is the tool
that produces that comparison rather than an impression.

Same for shuffle services, partition tuning, and any change where "it feels faster" is the
alternative evidence.

---

[← Performance analysis](../README.md)
