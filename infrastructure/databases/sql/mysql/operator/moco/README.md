[← MySQL operators](../README.md)

# MOCO

<https://github.com/cybozu-go/moco>

---

## What it is

A MySQL operator from Cybozu, built around **semi-synchronous replication** with explicit, legible
failover semantics.

It is Apache 2.0, it does one thing, and its documentation is unusually clear about what happens
during a failure — which for an operator whose job is failover is the property that matters most.

| Capability | Detail |
|---|---|
| `MySQLCluster` CRD | the cluster, its size and its configuration |
| **Semi-synchronous replication** | a committed transaction exists on at least one replica |
| **Automatic failover** | with defined, documented rules about when it will and will not act |
| Backups | to object storage, with point-in-time recovery |
| Clone and rejoin | a replica too far behind is re-cloned automatically |
| Services per role | separate endpoints for primary and replicas |

## Why semi-synchronous is the right default

The replication model decides the failure behaviour far more than the operator does, and MOCO's
choice is the pragmatic middle:

| Model | On failover |
|---|---|
| Asynchronous | the last transactions **may be lost** |
| **Semi-synchronous** | at least one replica has them, so a promoted replica is not behind |
| Group Replication / Galera | multiple writers, and write conflicts become a concern |

Asynchronous is faster and loses data on failover, which is the trade most people accept without
choosing it. Multi-primary avoids that and introduces conflict handling that applications must
then deal with.

Semi-synchronous keeps exactly one writer and guarantees the promoted replica has the committed
data. The cost is a small write latency — the primary waits for one acknowledgement — and for most
workloads that is the right exchange.

## When to use it

- MySQL is being **run** here rather than read from elsewhere
- one writer, with failover that does not silently lose transactions
- Apache licensing, with backups and PITR included
- a clear, small operator is preferable to a large one

## When not to use it

- MySQL is a **source system** the platform reads from — which is the position here; the operator
  question is then academic
- multi-primary writes are the requirement — the Percona XtraDB Cluster Operator uses Galera
- sharding is the actual problem — [Vitess](../../../../distributed/newsql/vitess/README.md)
- a single instance for development, where plain manifests are less to read

## The setting that matters most here

Regardless of operator, and stated in both [`../README.md`](../README.md) and
[`../../README.md`](../../README.md) because it is the one that breaks a data platform:

**`binlog_format = ROW`.**

CDC does not work properly without it. An operator will cheerfully run a healthy, well-replicated
cluster that cannot be used as a change-data-capture source, and the discovery comes after the
pipeline is built.

Also worth setting deliberately: `innodb_buffer_pool_size` (the default assumes a small machine),
`sql_mode` (permissive defaults silently truncate and coerce), and `utf8mb4` as the character set
— `utf8` in MySQL is not UTF-8.

## Notes

Mapped as the MySQL operator here.

Nothing is deployed, and the reason is the framing in
[`sql/mysql/`](../../README.md): MySQL appears in this repository on the **left** of the pipeline
— the application database that data is extracted *from*, not the warehouse it goes *into*. In
that position the operator belongs to whoever owns the application.

MOCO is catalogued as the answer if that changes, and because its replication model is the one
worth defaulting to. The reasoning generalises beyond this operator: **choose the replication
model first, then the operator that implements it well**, because the failure behaviour is the
model's and not the controller's.

---

[← MySQL operators](../README.md)
