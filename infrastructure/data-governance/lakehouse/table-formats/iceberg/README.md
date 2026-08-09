[← Table formats](../README.md)

# Apache Iceberg

<https://github.com/apache/iceberg>
<https://github.com/apache/iceberg-python>

---

## The problem it solves

The emerging default table format, and the reason is not performance — it is that Iceberg removed
two classes of expensive mistake that the Hive-style layout made permanent.

**Hidden partitioning.** In a Hive-style table a query must filter on the partition column
explicitly, in exactly the right form, or it scans everything — and that requirement leaks into
every query anyone writes. Iceberg records the partition *transform* in metadata and applies it
automatically: filter on the timestamp, and the right partitions are pruned.

**Partition evolution.** Changing partitioning from daily to hourly normally means rewriting the
table. Iceberg applies the new scheme to new data and keeps reading the old, which turns an
irreversible decision into a reversible one.

Between them, those two remove the most costly design errors in lakehouse work — the ones you
cannot undo.

| Capability | Detail |
|---|---|
| ACID transactions | via atomic metadata pointer swaps, serialised by the catalog |
| **Hidden partitioning** | the transform is metadata; queries do not encode it |
| **Partition evolution** | change it without rewriting history |
| Schema evolution | add, drop, rename and reorder, by column ID rather than by position |
| **Time travel** | query as of a snapshot or a timestamp |
| **Branching and tagging** | see [`version-control/iceberg/`](../../version-control/iceberg/README.md) |
| Broad engine support | Spark, Trino, Flink, DuckDB, ClickHouse, Snowflake, and more |

Schema evolution by **column ID** is the underrated detail: renaming a column does not break
readers, because the identity is the ID rather than the name or the position.

## When to use it

- **the default** for analytical tables on object storage
- more than one engine reads the same data — this is where its support is widest
- the partitioning scheme is not certain, which it rarely is at the start
- time travel or branching is useful

## When not to use it

- heavy CDC upserts with record-level indexes — [Hudi](../hudi/README.md)
- Flink-first streaming with a changelog as a first-class concept —
  [Paimon](../paimon/README.md)
- the platform is Databricks — [Delta](../delta/README.md) is the native path
- **there is no catalog** — see below; this is not optional

## The catalog is part of the decision

Iceberg without a catalog is a set of files that different engines will disagree about.

The catalog holds the pointer to the current metadata file and makes swapping it atomic — which is
what serialises concurrent writers and prevents a corrupted table. It is a **production dependency
of every query**, not a convenience.

The options are in [`metadata-catalog/`](../../../metadata-catalog/README.md):
[HMS](../../../metadata-catalog/hms/README.md) works and carries Hive's assumptions, and the
Iceberg REST catalog — [Polaris](../../../metadata-catalog/iceberg/polaris/README.md),
[Lakekeeper](../../../metadata-catalog/iceberg/lakekeeper/README.md),
[Gravitino](../../../metadata-catalog/iceberg/gravitino/README.md) — is the direction of travel.

Decide both together.

## Maintenance that must be scheduled

The features are adopted and the operations frequently are not:

| Job | Without it |
|---|---|
| **Compaction** | thousands of small files; planning takes longer than the scan |
| **Snapshot expiry** | history grows forever, and storage cost with it |
| Orphan file cleanup | files from failed writes never referenced and never deleted |
| Manifest rewriting | the metadata itself becomes slow to read |

Iceberg exposes these as callable procedures — `rewrite_data_files`, `expire_snapshots`,
`remove_orphan_files` — so they are a scheduled job rather than a script to write.

The **small-files problem** is the one that degrades platforms gradually: a streaming write
committing every minute produces 1,440 files a day per partition, and query time becomes dominated
by opening files rather than reading them.

## Notes

Reference material recorded here:

- [registering Iceberg files into Hive Metastore](https://atwong.medium.com/how-to-register-apache-iceberg-files-into-apache-hive-metastore-hms-5a4509da8224)
- [Iceberg branching](https://iceberg.apache.org/docs/latest/branching/#overview) — the basis of
  the write-audit-publish pattern in [`version-control/`](../../version-control/README.md)
- [a video series on Iceberg](https://www.youtube.com/watch?v=tsdApb3cEoE&list=PL-gIUf9e9CCskP6wP-NKRU9VhofMHYjcd&index=14)
- Iceberg CDC — an open thread in the original notes; incremental reads between snapshots are the
  mechanism, and the tooling around it is less settled than the feature

[iceberg-python](https://github.com/apache/iceberg-python) — PyIceberg — is worth knowing about
separately: it reads and writes Iceberg tables **without Spark or a JVM**, which pairs well with
[DuckDB](../../../../data-engineering/processing/duckdb/README.md) for work that does not justify
a cluster.

**This is the right default for pikakube.** The supporting pieces already exist:
[MinIO](../../storage/minio/README.md) for storage, three REST catalog options mapped, and
branching in [`version-control/iceberg/`](../../version-control/iceberg/README.md). The recorded
difficulty across this folder is consistent — the format is the easy part, and the storage and
catalog integration is where the time goes.

---

[← Table formats](../README.md)
