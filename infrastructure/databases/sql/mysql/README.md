[← SQL databases](../README.md)

# MySQL

The other relational default — and in most estates, a **source** rather than a target.

Subfolders: [`mysql/`](mysql/README.md) — the engine and Percona tooling ·
[`operator/`](operator/README.md) — running it on Kubernetes ·
[`dump/`](dump/README.md) — logical backup and migration

---

## Where it sits

MySQL is enormously deployed, and for a data platform it usually appears on the **left** of the
pipeline: the application database that data is extracted *from*, not the warehouse it goes
*into*.

That framing decides what matters about it here:

| Concern | Why |
|---|---|
| **CDC and replication** | how data leaves it — see [Debezium](../../../data-streaming/README.md) and [Airbyte](../../../analytics-engineering/integration/airbyte/README.md) |
| **Logical dumps** | migration, and the [`dump/`](dump/README.md) tooling |
| Binlog configuration | what makes CDC possible at all |
| Read replicas | so analytical reads never touch the primary |

## MySQL or PostgreSQL

For a new service, [PostgreSQL](../postgresql/README.md) is usually the answer — richer types,
better extensions, stricter defaults.

MySQL earns its place when:

- it is **already there**, which is the common case
- the team knows it and operates it well
- replication topologies are familiar, and its model fits the deployment

Neither is a mistake. Choosing MySQL *for a new service without a reason* is the thing worth
questioning, since the extension ecosystem is where Postgres pulls away.

## The configuration that bites

| Setting | Why |
|---|---|
| **Character set** | `latin1` defaults cause encoding problems that surface years later. UTF-8, explicitly, always |
| `binlog_format = ROW` | required for reliable CDC. `STATEMENT` produces changes that cannot be replayed correctly |
| `sql_mode` | permissive defaults silently truncate and coerce data |
| `innodb_buffer_pool_size` | the single most important performance setting, and the default assumes a small machine |

The second row matters specifically for a data platform: **CDC does not work properly without
row-based binlogs**, and discovering that after building the pipeline is expensive.

## Percona

Much of the tooling in these folders is Percona's — [XtraBackup](mysql/README.md),
[mydumper](dump/README.md), PMM. Percona Server is a MySQL distribution with additional
instrumentation and tooling, and its ecosystem is where most serious MySQL operations knowledge
lives.

---

[← SQL databases](../README.md)
