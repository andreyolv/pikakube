[← Processing](../README.md)

# Apache Spark

<https://github.com/apache/spark>
<https://github.com/apache/spark-docker>
<https://spark.apache.org/docs/latest/>

Subfolders: [`kubernetes-operator/`](kubernetes-operator/README.md) ·
[`spark-submit/`](spark-submit/README.md) · [`shuffle/`](shuffle/README.md) ·
[`spark-accelerator/`](spark-accelerator/README.md) ·
[`spark-history-server/`](spark-history-server/README.md) ·
[`spark-performance/`](spark-performance/README.md) · [`pyspark/`](pyspark/README.md)

## Contents

1. [When it earns its place](#1-when-it-earns-its-place)
2. [Deployment modes](#2-deployment-modes)
3. [Running it on Kubernetes](#3-running-it-on-kubernetes)
4. [The surrounding pieces](#4-the-surrounding-pieces)
5. [Anti-patterns](#5-anti-patterns)
6. [References](#6-references)

---

## 1. When it earns its place

Spark is the answer when data genuinely does not fit on one machine, or when volume is elastic
enough that fixed capacity is wrong.

It is **not** the answer for tens of gigabytes — see
[`../README.md`](../README.md#1-the-question-to-ask-first). Coordination overhead is real, and
below a certain size it is most of the runtime.

The honest framing: Spark is a large commitment — executors to size, shuffle to tune,
dependencies to package, and failure modes that take time to learn. It pays for itself at
scale, and costs more than it returns below it.

## 2. Deployment modes

The distinction that causes the most confusion, and it decides where the driver runs:

| Mode | Driver runs | Use |
|---|---|---|
| **Cluster** | inside the cluster, as a pod | production — the submitting process can exit |
| **Client** | where you submitted from | interactive work, notebooks, debugging |
| Local | one JVM, no cluster | tests and development |

In cluster mode the driver is a pod like any other, which is what makes it survivable and
schedulable. In client mode the driver is wherever you ran `spark-submit` — so if that is a
laptop or a short-lived pod, the job dies with it.

References:
[deployment modes](https://gaurav98095.medium.com/understanding-deployment-modes-in-pyspark-8031ddf7f5f3) ·
[client, cluster and local](https://blog.stackademic.com/understanding-apache-spark-deployment-modes-client-mode-cluster-mode-and-local-mode-bbfd1c7612fa)

## 3. Running it on Kubernetes

Three ways, in increasing order of how declarative they are:

| Approach | What it is | Folder |
|---|---|---|
| `spark-submit` | submit directly to the API server | [`spark-submit/`](spark-submit/README.md) |
| **Operator** | a `SparkApplication` CRD, reconciled | [`kubernetes-operator/`](kubernetes-operator/README.md) |
| From an orchestrator | Airflow submits and tracks | [`orchestration/`](../../orchestration/README.md) |

The operator is the right default for anything recurring: the job becomes a Kubernetes object,
which means GitOps, status, and a controller handling retries — rather than a script that
submitted something and hoped.

## 4. The surrounding pieces

The parts most catalogues omit, and which decide whether Spark on Kubernetes actually works:

| Concern | Folder | Why |
|---|---|---|
| **Shuffle** | [`shuffle/`](shuffle/README.md) | shuffle data on executor local disk blocks dynamic allocation and dies with the pod |
| **Native execution** | [`spark-accelerator/`](spark-accelerator/README.md) | Gluten, Comet and Blaze replace the JVM execution path with native engines |
| **History** | [`spark-history-server/`](spark-history-server/README.md) | a finished job leaves nothing to diagnose without event logs |
| **Performance analysis** | [`spark-performance/`](spark-performance/README.md) | finding out *why* a job is slow, rather than guessing |

Shuffle is the one that surprises people on Kubernetes. Without a remote shuffle service,
executors cannot be scaled down without losing their shuffle data — which quietly removes the
main cost benefit of running on Kubernetes at all.

## 5. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Spark for data that fits on one node | coordination costs more than the work | [DuckDB](../duckdb/README.md) |
| Client mode in production | the job dies with the submitting process | cluster mode |
| No event logs | a finished job is undiagnosable | [history server](spark-history-server/README.md) |
| Default executor sizing | wasted resources, or shuffle spill and failure | size from the actual shuffle profile |
| Dynamic allocation without remote shuffle | executors cannot scale down safely | [Celeborn or Uniffle](shuffle/README.md) |
| Ignoring small files | thousands of tiny files dominate the runtime | compaction — see [file formats](../../file-formats.md) |
| Logic in Python where SQL would do | harder to test, review and hand over | SQL where possible |

## 6. References

- [Spark configuration](https://spark.apache.org/docs/latest/configuration.html#application-properties) — the parameters that matter
- [Submitting applications](https://spark.apache.org/docs/latest/submitting-applications.html#master-urls) — master URLs
- [PySpark style guide](https://github.com/palantir/pyspark-style-guide) (Palantir)
- [Apache Spark internals](https://github.com/japila-books/apache-spark-internals) — the reference for understanding *why*, not just how
- [Apache Livy](https://github.com/apache/incubator-livy) — REST submission, when a service needs to launch jobs

---

[← Processing](../README.md)
