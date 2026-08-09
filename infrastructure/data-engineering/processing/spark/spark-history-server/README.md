[← Spark](../README.md)

# History server

Tools covered: [`spark-history-server`](spark-history-server/README.md) · [`delight`](delight/README.md)

---

## The problem it solves

The Spark UI exists while the driver is running. The moment the job finishes, the driver pod
terminates and **everything is gone** — stages, tasks, shuffle sizes, the DAG, the skew that
caused the problem.

Which means the only jobs you can diagnose are the ones still running, and the question people
actually ask is "why was last night's run slow".

The history server reads **event logs** written to durable storage and reconstructs that UI
after the fact.

## The prerequisite

Event logging has to be enabled and pointed somewhere that outlives the pod:

```
spark.eventLog.enabled           true
spark.eventLog.dir               s3a://bucket/spark-history
spark.history.fs.logDirectory    s3a://bucket/spark-history
```

On HDFS the directory has to exist and be writable — see
[spark-history-server](spark-history-server/README.md).

This is the piece to configure **before** the first job runs. Retrofitting it does not recover
the history you wanted.

## The tools

| Tool | Notes | Detail |
|---|---|---|
| **Spark History Server** | the standard, part of Spark | [→](spark-history-server/README.md) |
| **Delight** | a hosted alternative UI with CPU and memory metrics overlaid | [→](delight/README.md) |

**Delight adds resource metrics** to the picture — the standard UI shows what Spark did, not
how much CPU and memory it actually used, which is what you need for right-sizing. See its
README for the caveat about authentication.

## Related

For the question "**why** is this slow" rather than "what happened", see
[`spark-performance/`](../spark-performance/README.md) — DataFlint and sparkMeasure analyse the
same event data and point at causes.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| No event logs | finished jobs are undiagnosable | enable them before production |
| Event logs on ephemeral storage | they disappear with the pod, which defeats the purpose | object storage |
| No retention policy on the log directory | it grows without bound | lifecycle policy on the bucket |
| Reading the UI without knowing what to look for | the data is there and the insight is not | [`spark-performance/`](../spark-performance/README.md) |

---

[← Spark](../README.md)
