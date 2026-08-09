[← History server](../README.md)

# Spark History Server

Part of Apache Spark — <https://spark.apache.org/docs/latest/monitoring.html>

---

## What it does

Reads the event logs Spark writes during execution and reconstructs the Spark UI for **finished**
jobs: stages, tasks, shuffle read and write sizes, the DAG, and where the time went.

Without it, a job that has ended leaves nothing behind — see
[`../README.md`](../README.md#the-problem-it-solves).

## Configuration

```
spark.eventLog.enabled           true
spark.eventLog.dir               <path>
spark.history.fs.logDirectory    <path>
```

The two paths must match. On object storage they are usually `s3a://` URIs, which is the
arrangement that survives losing the cluster.

---

## Notes

### HDFS setup

The log directory has to exist and be writable before any job runs:

```bash
hadoop fs -mkdir /spark-history
hadoop fs -chmod -R 777 /spark-history
```

`777` is fine for a lab. On a shared cluster, scope it to the identity Spark runs as instead —
the event logs contain the full plan and configuration of every job, which is more than a
casual reader should see.

## Operational notes

**Log volume grows quickly.** A large job produces a large event log, and there is no automatic
cleanup unless configured — set `spark.history.fs.cleaner.enabled` and a retention period, plus
a lifecycle policy on the bucket.

**Startup can be slow.** The server replays logs on start, so a directory with thousands of
applications takes time to become useful. Retention keeps that manageable.

---

[← History server](../README.md)
