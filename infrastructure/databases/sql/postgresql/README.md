[← SQL databases](../README.md)

# PostgreSQL

The default relational database, and the one that absorbs most reasons to pick another.

Subfolders: [`postgresql/`](postgresql/README.md) — the engine, extensions and operations ·
[`operator/`](operator/README.md) — running it on Kubernetes

---

## Why it is the default

Not preference — coverage. Postgres handles, adequately, most of the workloads people leave
relational databases for:

| Requirement | How |
|---|---|
| Documents | `JSONB`, with GIN indexes |
| Full-text search | built in, to a real scale |
| Geospatial | PostGIS, the reference implementation |
| Vectors | [pgvector](postgresql/README.md) |
| Time-series | TimescaleDB, or native partitioning |
| Distributed | [Citus](postgresql/README.md), when one node is genuinely not enough |
| Queues | `SKIP LOCKED` |
| Cron | `pg_cron` |
| Parquet | `pg_parquet` |

None beats a specialist at its specialty. The point is that they are good enough often enough
that a second database usually costs more than it returns — see
[`../README.md`](../README.md#2-postgresql-is-usually-the-answer).

## The two folders

| Folder | Question |
|---|---|
| [`postgresql/`](postgresql/README.md) | the engine itself — extensions, tuning, users, dumps, migration |
| [`operator/`](operator/README.md) | how it runs on Kubernetes — failover, backup, upgrades |

On Kubernetes the operator choice matters more than the engine configuration, because it
decides what happens when a node dies.

## The three things that decide whether it survives

**Connection pooling.** Postgres allocates a process per connection and exhausts long before it
exhausts CPU. The symptom is a database that appears slow while idle. A pooler is a
requirement, not a tuning step — see [`tooling/pooler/`](../../tooling/pooler/).

**Storage.** An RWO volume pins the pod to a node, and a node failure means waiting for detach —
see [`storage/`](../../../site-reliability-engineering/storage/README.md).

**Tested restores.** With the operator scaled to zero first, or it recreates an empty volume
before the restore lands — see
[Velero](../../../site-reliability-engineering/backup/velero/README.md).

## Monitoring it

| Tool | What it gives |
|---|---|
| [postgres-exporter](../../../observability/metrics/exporters/postgres-exporter/README.md) | Prometheus metrics — connections, replication lag, cache hit ratio |
| [pghero](../../tooling/monitoring/pghero/README.md) | slow queries, missing indexes, bloat |
| [PMM](../../tooling/monitoring/pmm/README.md) | Percona's full monitoring stack |
| [pgbadger](../../tooling/monitoring/pgbadger/README.md) | log analysis |

The four metrics that actually matter: **connections against `max_connections`**, replication
lag, long-running transactions, and cache hit ratio. The first is the most common outage.

---

[← SQL databases](../README.md)
