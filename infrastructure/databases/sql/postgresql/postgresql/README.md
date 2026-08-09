[← PostgreSQL](../README.md)

# PostgreSQL — engine, extensions and operations

<https://github.com/postgres/postgres>
<https://www.postgresql.org/docs/current/>

---

## Extensions worth knowing

The reason Postgres absorbs so many use cases:

| Extension | What it adds |
|---|---|
| [pgvector](https://github.com/pgvector/pgvector) | vector similarity search — embeddings without a separate vector database |
| [Citus](https://github.com/citusdata/citus) | distributed Postgres, sharding across nodes |
| [pg_cron](https://github.com/citusdata/pg_cron) | scheduled jobs inside the database |
| [pg_parquet](https://github.com/CrunchyData/pg_parquet) | read and write Parquet directly — a bridge to the lakehouse |
| [pgaudit](https://github.com/pgaudit/pgaudit) | detailed audit logging, usually a compliance requirement |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | richer query statistics than `pg_stat_statements` |

**pgvector** and **pg_parquet** are the two that most change what a second database would be
for: embeddings and lakehouse interchange, without leaving Postgres.

## Tuning

- [Resource configuration](https://www.postgresql.org/docs/current/runtime-config-resource.html)
- [pgtune](https://github.com/le0pard/pgtune) — sensible starting values from hardware and workload

The defaults assume a small machine. `shared_buffers`, `work_mem`, `maintenance_work_mem` and
`effective_cache_size` are the ones that matter, and leaving them at default is the most common
reason a database "is slow" on generous hardware.

## Clients

- [psycopg2](https://github.com/psycopg/psycopg2) — the standard Python driver
- [asyncpg](https://github.com/MagicStack/asyncpg) — async, and substantially faster

## Backup

- [pgBackRest](https://github.com/pgbackrest/pgbackrest) — full, incremental and PITR
- [Barman](https://github.com/EnterpriseDB/barman) — what [CloudNativePG](../operator/cnpg/README.md) uses underneath

---

## Notes

### Creating a user for a specific database

```sql
CREATE USER my_user WITH PASSWORD 'my_password';
GRANT ALL PRIVILEGES ON DATABASE my_database TO my_user;
```

Validating what exists:

```sql
SELECT usename FROM pg_catalog.pg_user;
SELECT datname, datacl FROM pg_database;
```

### Dump and restore — migrating to a new version

`pg_dumpall` for every logical database, `pg_dump` for a specific one.

```bash
# 1. dump from the running instance
kubectl exec postgres-65bcfbb67f-vrbgf -- pg_dump -U andreyolv -d teste > dbbackup.sql

# 2. stop it and discard the old volume
kubectl scale deploy postgres --replicas=0
kubectl delete pvc <pvc>
```

> The old data **cannot** be mounted into the new version — this is equivalent to migrating to
> a new database, not upgrading in place.

```bash
# 3. update the image in the Deployment, then bring it back
kubectl scale deploy postgres --replicas=1

# 4. restore
kubectl cp dbbackup.sql postgres-5f48985dbd-lfkcb:/tmp/dbbackup.sql
kubectl exec -it postgres-5f48985dbd-lfkcb -- psql -U andreyolv -d teste -f /tmp/dbbackup.sql
```

Verify:

```sql
SELECT version();
\dt myschema.*
SELECT schema_name FROM information_schema.schemata;
SELECT * FROM myschema.employees;
```

### The alternative for large databases

Dump and restore requires downtime proportional to the data size. For anything where that is
unacceptable, [logical replication](https://www.postgresql.org/docs/current/logical-replication-subscription.html)
allows replicating into the new version and cutting over — downtime measured in seconds rather
than hours.

---

[← PostgreSQL](../README.md)
