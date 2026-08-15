[← MariaDB operators](../README.md)

# mariadb-operator

<https://github.com/mariadb-operator/mariadb-operator>

<https://mariadb-operator.github.io/mariadb-operator>

The community operator for MariaDB on Kubernetes: Galera or replication, MaxScale in front, physical
and logical backups, and point-in-time recovery. MIT.

---

## The problem it solves

A MariaDB StatefulSet gives you pods with disks. Everything that makes it a *database service* —
which node is writable, what happens when one dies, where backups go, whether you can recover to
last Tuesday, which application has which grants — is a runbook, a CronJob, and somebody's memory.

This operator turns that surface into resources:

| CRD | What it declares |
|---|---|
| **`MariaDB`** | the server itself — topology (Galera or replication), version, storage, resources, `my.cnf` |
| **`MaxScale`** | the MariaDB proxy in front of it: routing, load balancing, automated failover and switchover |
| **`Backup`** / **`PhysicalBackup`** | scheduled logical (`mariadb-dump`) or physical (`mariadb-backup`) backups to S3, Azure Blob, a PVC or a VolumeSnapshot |
| **`Restore`** | bootstrap a new instance from a backup — including point in time |
| **`Database`**, **`User`**, **`Grant`** | schemas and access as Kubernetes objects instead of SQL run by hand |
| **`Connection`** | a `Secret` holding a ready-made DSN for an application to consume |
| **`SqlJob`** | scheduled SQL — migrations, maintenance — as a resource |

Two of these are worth more than the list suggests.

**`PhysicalBackup` with binlog archiving is what makes PITR real.** A nightly `mariadb-dump` is a
backup; it is not recovery. Physical backups plus archived binary logs are what turn *"restore last
night"* into *"restore to 14:32, before the migration"*, and that is the difference between an RPO of
24 hours and one of minutes. It is also the part teams most often postpone until they need it.

**`MaxScale` is the differentiator against the MySQL operators.** [MOCO](../../../mysql/operator/moco/README.md)
gives you correct semi-synchronous replication and leaves routing to Services. MaxScale is a real
database proxy — read/write splitting, connection routing that follows the primary, query-aware
behaviour, and coordinated switchover — managed by the same operator. If clients must always reach
the current primary without knowing which pod that is, this is the piece that does it.

## When to use it

- **MariaDB is genuinely being run on Kubernetes**, not consumed as a managed service or a VM
- **Galera** is the topology, and cluster bootstrap and recovery should be automated rather than
  documented — see [`../README.md`](../README.md#what-an-operator-has-to-solve-here)
- **PITR is a requirement**, and a `mariadb-dump` CronJob is being called a backup strategy
- routing must follow the primary automatically → MaxScale
- databases, users and grants belong in Git alongside the applications that need them, with
  credentials delivered as `Secret`s rather than created by hand
- the platform is GitOps-reconciled, so a database expressed as objects fits the existing model

## When not to use it

- **the cloud offers it** — a managed MariaDB or MySQL-compatible service is less work and someone
  else's pager. The [`databases/README.md`](../../../../README.md) position on running databases
  yourself applies here first
- **a new service that could use PostgreSQL.** [`sql/README.md`](../../../README.md#2-postgresql-is-usually-the-answer)
  is unambiguous, and the operator ecosystem is a further argument for it: CloudNativePG is more
  mature than anything in the MariaDB or MySQL column
- for a **single throwaway instance** in a dev namespace — a chart and a PVC is less machinery
- when you want **Galera without owning Galera**. The operator automates the procedures; it does not
  remove SST load, quorum arithmetic, or DDL behaviour from your problem list
- when the estate is MySQL. Not interchangeable — see
  [`../../README.md`](../../README.md#where-it-has-diverged)

## Notes

**Galera is still Galera.** The operator handles bootstrap, recovery and node replacement, which is
the majority of the pain, but three properties belong to the replication technology and survive any
operator: **quorum** means an even node count or a split network can leave you without a writable
cluster; **SST** means a joining node pulls a full state transfer from a donor, which is heavy on
both nodes and slow on a large dataset; and **schema changes** replicate under rules that make some
DDL disruptive. Read Galera's operational documentation before the operator's — the operator is the
easy half.

**Storage decides the outcome.** As with every stateful workload here, the operator can only be as
good as the volumes underneath it. Local-path storage on a single node is a lab; real deployments
want replicated block storage from [`site-reliability-engineering/storage/block-storage/`](../../../../../site-reliability-engineering/storage/block-storage/README.md),
and the VolumeSnapshot backup path additionally needs a CSI driver that supports snapshots
([external-snapshotter](../../../../../site-reliability-engineering/backup/external-snapshotter/README.md)).

**Set `binlog_format = ROW` from the start, in the CR.** [`../../README.md`](../../README.md#the-cdc-question)
records that MariaDB's realistic role in a data platform is as a **source to extract from**, and that
CDC does not work properly without row-based binary logging. The operator makes this a field in the
`MariaDB` object rather than a file somebody edits on a pod, which is the correct place for it — but
it has to be set. Configuring it after a pipeline exists means a restart of the database at the
least convenient moment.

**MIT, with a commercial cousin.** This operator is community-developed and MIT-licensed; MariaDB plc
separately ships an Enterprise Operator for MariaDB Enterprise Server. They are different products
with similar names, and evaluations should establish which one a piece of documentation is
describing. As with any single-vendor-adjacent project, check release cadence and maintainer breadth
before it becomes load-bearing.

**Where this fits in pikakube.** Nothing here runs MariaDB, and
[`../../README.md`](../../README.md#notes) is explicit that it is mapped as a *source system* —
something an application team chose, that a data platform reads from. This operator is the answer to
the narrower question that follows: **if that application ends up on this cluster, what runs the
database?** It is also, honestly, the strongest argument in the folder for not putting it there —
Galera on Kubernetes is a real operational commitment, and the recorded advice is that a new service
should have been PostgreSQL.

---

[← MariaDB operators](../README.md)
