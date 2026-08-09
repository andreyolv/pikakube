[← Stream processing](../README.md)

# Apache Fluss

<https://github.com/apache/fluss>

---

## What it is

**Streaming storage** built for real-time analytics — not a processor, and not quite a message
log either.

The problem it targets: Kafka stores an append-only log, which is ideal for streaming and poor
for querying. Getting a queryable current view means projecting into an
[OLAP engine](../../olap/README.md), which is another system and another copy.

Fluss stores streaming data in a **columnar, updatable** form — so it serves both as the stream
source and as a queryable table, with column pruning and primary-key lookups.

| | Kafka | Fluss |
|---|---|---|
| Storage | row-based log | **columnar** |
| Updates | append only | primary-key updates |
| Read a few columns | reads the whole message | column pruning |
| Point lookup by key | scan | indexed |

Donated to Apache by Alibaba, and designed to sit under Flink.

## When it is interesting

- the same data is consumed **as a stream and queried as a table**, and maintaining both is the current cost
- streaming with frequent updates by key, where an append-only log means constant compaction downstream
- Flink is the processing engine, which is what it is built for

## When it is not

- Kafka works and the projection into an OLAP store is not painful
- production dependence today — see below
- the requirement is a message broker; this is storage for analytics, not a general-purpose log

---

## Notes

> No Helm chart — <https://github.com/apache/fluss/issues/779>

Which for a GitOps setup means deploying it outside the pattern everything else follows.

## Why it is worth tracking

It addresses a genuine architectural awkwardness: the streaming layer and the serving layer
store the same data twice, in different shapes, kept in sync by a pipeline that can fail.

Whether the unified approach wins is not yet clear, and the idea is worth understanding
regardless — it is the same instinct as [AutoMQ](../../event-streaming/automq/README.md) reconsidering
where the log lives, one layer up.

---

[← Stream processing](../README.md)
