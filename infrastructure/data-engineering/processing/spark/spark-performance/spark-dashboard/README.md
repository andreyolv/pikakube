[← Performance analysis](../README.md)

# spark-dashboard

<https://github.com/cerndb/spark-dashboard>

---

## What it does

Exports Spark metrics — executor CPU and memory, task counts, shuffle, GC — into **Prometheus
and Grafana**, continuously, for every job.

From CERN's database group, and the approach is the pragmatic one: Spark already emits metrics
through its metrics system, and this wires them into the stack the rest of the platform already
uses.

## Why it belongs alongside the other two

They cover different time horizons:

| Question | Tool |
|---|---|
| What is wrong with **this** job? | [DataFlint](../dataflint/README.md) |
| Is version B faster than A? | [sparkMeasure](../spark-measure/README.md) |
| **How do all jobs behave over time?** | this |

The third question is the one nothing else answers. A job that has been getting 5% slower each
week is invisible in a per-run view and obvious in a trend.

## When to use it

- Prometheus and Grafana are already the [observability](../../../../../observability/README.md) stack — this puts Spark metrics next to everything else
- **right-sizing** across many jobs, using real usage rather than requested resources
- catching gradual regressions
- correlating Spark behaviour with cluster events — node pressure, evictions, storage latency

## When not to use it

- diagnosing one job now — DataFlint is faster
- there is no Prometheus, in which case this is a stack to adopt rather than a plugin

## The advantage over hosted alternatives

[Delight](../../spark-history-server/delight/README.md) shows resource usage too, and sends job telemetry
to a hosted service. This keeps everything in the cluster and correlated with the rest of the
platform's metrics — which matters both for data handling and because Spark problems are
frequently cluster problems.

---

[← Performance analysis](../README.md)
