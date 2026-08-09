[← Remote shuffle](../README.md)

# Apache Uniffle

<https://github.com/apache/uniffle>
<https://uniffle.apache.org/>

---

## What it is

A remote shuffle service, from Tencent, solving the same problem as
[Celeborn](../celeborn/README.md) — moving shuffle data off executor local disk so that executors become
disposable.

Its distinguishing property is **pluggable storage**: shuffle data can land on local disk, HDFS,
or object storage, rather than only on dedicated shuffle workers.

That matters on Kubernetes. Object storage as the shuffle backend removes the need to size and
operate stateful shuffle nodes at all — at the cost of higher latency than local disk.

| | Celeborn | Uniffle |
|---|---|---|
| Adoption | wider | smaller |
| Storage | its own workers | pluggable — disk, HDFS, object storage |
| Engines | Spark, Flink | Spark, MapReduce, Tez |

## When to use it

- object storage as the shuffle backend is attractive — no stateful tier to operate
- the estate includes MapReduce or Tez alongside Spark
- [Celeborn](../celeborn/README.md)'s deployment friction is a blocker

## When not to use it

- shuffles are small, or the cluster is fixed-size — neither service is needed
- you want the option with the most community and material behind it

## Evaluate both, on the deployment path

The two are close in what they do. The decision is usually made on **how hard each is to
actually run** — and Celeborn's README records real problems there.

Worth testing the deployment before comparing the features, because that is where the
difference actually shows up.

---

[← Remote shuffle](../README.md)
