[← MySQL](../README.md)

# MySQL — engine and Percona tooling

<https://github.com/percona/percona-helm-charts>
<https://dev.mysql.com/doc/>

---

## Percona

Most serious MySQL operations tooling comes from Percona rather than from upstream. Percona
Server is a MySQL distribution with additional instrumentation, and the surrounding tools are
what production MySQL is actually run with.

| Tool | What it does |
|---|---|
| [Percona XtraBackup](https://github.com/percona/percona-xtrabackup) | **hot physical backup** — no locking, no downtime |
| [mydumper](https://github.com/mydumper/mydumper) | parallel logical dump, far faster than `mysqldump` — see [`../dump/`](../dump/README.md) |
| [percona-helm-charts](https://github.com/percona/percona-helm-charts) | Kubernetes deployment |
| PMM | monitoring — see [`tooling/monitoring/pmm/`](../../../tooling/monitoring/pmm/README.md) |

## Physical or logical backup

The distinction that decides the strategy:

| | Physical (XtraBackup) | Logical (mydumper, mysqldump) |
|---|---|---|
| What it copies | the data files | SQL statements |
| Speed | fast, proportional to disk | slower, proportional to rows |
| Restore | fast — copy the files back | slow — replay every statement |
| **Portable across versions** | no | **yes** |
| Selective restore | whole instance | table or schema |
| Locking | none, with XtraBackup | depends on the tool and options |

**Physical for operations, logical for migration.** Restoring a large database from a logical
dump is measured in hours; upgrading across major versions requires one.

## The settings that matter

| Setting | Why |
|---|---|
| `innodb_buffer_pool_size` | the single biggest performance lever; the default assumes a small machine |
| **`binlog_format = ROW`** | required for reliable CDC — see [`../README.md`](../README.md#the-configuration-that-bites) |
| `character_set_server = utf8mb4` | `latin1` defaults produce encoding problems years later |
| `sql_mode` | permissive defaults silently truncate and coerce data |
| `max_connections` | with a [pooler](../../../tooling/pooler/) in front, since MySQL also has a ceiling |

## On Kubernetes

Same three concerns as [PostgreSQL](../../postgresql/README.md): storage that pins the pod to a
node, connection pooling, and a restore that has actually been performed.

Operators are in [`../operator/`](../operator/README.md) — [MOCO](../operator/moco/README.md) is the one
mapped here, and Percona and Oracle both publish operators worth comparing against it.

---

[← MySQL](../README.md)
