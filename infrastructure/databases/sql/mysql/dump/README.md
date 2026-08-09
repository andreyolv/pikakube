[← MySQL](../README.md)

# Logical dump

Tools covered: [`mydumper`](mydumper/README.md) · [`mysql-client`](mysql-client/README.md)

---

## When a logical dump is the right tool

Not for routine backup — [XtraBackup](../mysql/README.md) is faster for that, in both
directions. Logical dumps matter when the output has to be **portable**:

| Situation | Why logical |
|---|---|
| **Major version upgrade** | physical backups are not portable across versions |
| Migrating to another host, cloud or provider | data files assume the same environment |
| Restoring **one table** | physical restores are whole-instance |
| Moving into a different engine | SQL is the common denominator |
| Seeding a development environment | a subset, sanitised |

The first row is the common one, and it is the same constraint recorded for
[PostgreSQL](../../postgresql/postgresql/README.md#dump-and-restore--migrating-to-a-new-version):
the old data files cannot simply be mounted into the new version.

## The tools

| Tool | Notes | Detail |
|---|---|---|
| **mydumper** | **parallel** dump and restore — substantially faster than `mysqldump` on anything large | [→](mydumper/README.md) |
| **mysql-client** | `mysqldump` and `mysql`, the standard tools | [→](mysql-client/README.md) |

`mysqldump` is single-threaded and writes one large file. On a database of any size that is the
bottleneck — mydumper parallelises across tables and chunks, and restores in parallel too,
which usually turns hours into minutes.

## The thing that catches people

**A logical restore is slow.** The dump may take twenty minutes and the restore four hours,
because every statement is replayed and every index rebuilt.

Plan the downtime around the **restore**, not the dump. That asymmetry is why physical backup
exists for operational recovery, and why logical dumps are a migration tool rather than a
backup strategy.

## Related

- Physical backup: [XtraBackup](../mysql/README.md)
- Near-zero-downtime migration: replication into the new version, then cut over — the same pattern as [PostgreSQL logical replication](../../postgresql/postgresql/README.md)
- Volume-level alternatives: [`backup/`](../../../../site-reliability-engineering/backup/README.md)

---

[← MySQL](../README.md)
