[← Wide-column stores](../README.md)

# Cassandra

<https://github.com/apache/cassandra>
<https://github.com/k8ssandra/k8ssandra-operator>

Deployment shapes: [`cassandra/`](cassandra/README.md) — the Helm chart ·
[`k8ssandra-operator/`](k8ssandra-operator/README.md) — the operator

---

## The problem it solves

Writes at a volume and with an availability profile that a single-primary relational database
cannot match, scaling roughly linearly with nodes.

There is **no primary**. Every node accepts writes, data is distributed by a hash of the
partition key, and replicas are reconciled continuously. Losing a node reduces the quorum rather
than causing an outage — there is no failover window, because there is nothing to fail over.

That is the capability, and it is genuinely not available from
[PostgreSQL](../../../sql/postgresql/README.md) at any configuration.

## When to use it

- a **measured** write ceiling on one machine
- availability that must not have a gap, including during maintenance
- multi-datacentre replication as a configuration rather than a project
- query patterns that are known and stable

## When not to use it

- the write volume has not been measured, and the ceiling is anticipated rather than observed
- **the queries are not yet known** — the partition key is permanent and derived from them
- joins, ad-hoc querying, or aggregation across the dataset
- analytics — see [`data-streaming/olap/`](../../../../data-streaming/olap/README.md), which
  answers a different question
- lower latency and a smaller cluster matter more than ecosystem —
  [ScyllaDB](../scylladb/README.md)

## The three things that decide success

Covered fully in [`../README.md`](../README.md); the short form, because each is permanent or
silent:

**The partition key is the schema.** It determines which node holds the data, queries that do not
specify it are refused, and it cannot be changed later. Model the queries first, then derive the
tables — writing the same data to three tables to serve three queries is the intended design, not
a workaround.

**Consistency is per query.** `R + W > RF` gives strong consistency. Writing at `ONE` and reading
at `ONE` does not, and the resulting bug is intermittent and load-dependent.

**Repair must be scheduled.** Cassandra tolerates replicas diverging and reconciles them lazily.
Without anti-entropy repair, deleted data can reappear once tombstones expire — silent, delayed,
and very confusing on arrival. This single requirement is most of the argument for
[K8ssandra](k8ssandra-operator/README.md).

## The two deployment shapes

| Shape | Use |
|---|---|
| [`cassandra/`](cassandra/README.md) | development and evaluation — a working CQL endpoint |
| [`k8ssandra-operator/`](k8ssandra-operator/README.md) | **anything else** — repair, backups, node replacement, multi-datacentre |

The gap between them is unusually wide for this repository, because Cassandra's software runs
fine unattended and its *operations* are where data is lost.

## Notes

Mapped with both shapes. Nothing is deployed here, and on a single Kind cluster nothing should
be — a masterless multi-node store on one machine demonstrates the API and none of the properties
that justify the data model it demands.

The alternative in the same folder: [ScyllaDB](../scylladb/README.md) is protocol-compatible, so
drivers, CQL and the data model transfer unchanged. Its argument is operational — C++ rather than
a JVM, shard-per-core, lower latency and fewer nodes — against Cassandra's much larger ecosystem
and Apache licence.

---

[← Wide-column stores](../README.md)
