[← Cassandra](../README.md)

# cassandra — the Helm deployment

<https://github.com/apache/cassandra>

---

## What this shape is

Cassandra deployed from a Helm chart as a `HelmRelease`, with its values in Git. A StatefulSet,
persistent volumes, and a seed configuration — enough to have a running cluster.

## When it fits

- **development and evaluation**, where the goal is a working CQL endpoint
- a fixed, small cluster whose topology will not change
- learning the data model without operating the failure cases

## When it does not

- production, or anything where nodes will be added, replaced or repaired —
  [`k8ssandra-operator/`](../k8ssandra-operator/README.md)
- multi-datacentre replication, which is one of the main reasons to choose Cassandra at all
- backups and repair as scheduled operations rather than manual ones

## Why the chart is usually not enough

Cassandra's operational work is not deployment, it is the ongoing procedures — and a chart does
none of them:

| Procedure | Why a StatefulSet does not cover it |
|---|---|
| **Anti-entropy repair** | replicas drift apart silently; repair must run on a schedule or reads return stale data |
| **Node replacement** | a dead node is replaced with a specific flag and a streaming rebuild, in order |
| Adding nodes | token ranges are redistributed, and this is a streaming operation |
| Compaction strategy | chosen per table according to the workload; the wrong one degrades reads badly |
| Backups | snapshots plus commit-log archiving, not a volume copy |
| Rolling restarts | one node at a time, with each confirmed healthy first |

**Repair is the one that catches people.** Cassandra's consistency model tolerates replicas
diverging and repairs them lazily. If anti-entropy repair never runs, deleted data can reappear
once tombstones expire — a failure that is silent, delayed, and very confusing when it arrives.

That single requirement is most of the argument for an operator.

## What to set deliberately

| Setting | Why |
|---|---|
| **Replication factor and strategy** | per keyspace; `NetworkTopologyStrategy` even for one datacentre, so adding a second later is possible |
| **Consistency levels** | `R + W > RF`, decided per query — see [`../../README.md`](../../README.md#3-consistency-is-a-per-query-setting) |
| Heap and GC | JVM tuning is not optional at any real scale |
| Compaction strategy | `STCS`, `LCS` or `TWCS` according to the write and read shape |
| Anti-affinity | replicas on the same node is not replication |
| Storage class | local SSD if possible; Cassandra is sensitive to disk latency |

The replication-strategy row is a small decision with a long tail: `SimpleStrategy` works on one
datacentre and cannot be extended cleanly, so starting with `NetworkTopologyStrategy` costs
nothing and keeps the option open.

## Notes

Kept alongside [`k8ssandra-operator/`](../k8ssandra-operator/README.md) as the two ways to run
Cassandra here, and the split is the same one that appears throughout this repository: a chart
gives you the software, an operator gives you the operations.

For Cassandra the gap between those two is unusually wide, because the software runs fine and the
operations are where the data is lost.

The alternative in the sibling folder: [ScyllaDB](../../scylladb/README.md) is
protocol-compatible and C++, so the drivers and the data model transfer unchanged — see
[`../../README.md`](../../README.md#4-the-tools).

---

[← Cassandra](../README.md)
