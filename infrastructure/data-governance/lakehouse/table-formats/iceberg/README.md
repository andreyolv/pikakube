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

The features are adopted and the operations frequently are not. Iceberg exposes each as a callable
procedure, so these are a scheduled job rather than a script to write:

| Job | Procedure | Without it |
|---|---|---|
| **Compaction** | `rewrite_data_files` | thousands of small files; planning takes longer than the scan |
| **Snapshot expiry** | `expire_snapshots` | history grows forever, and storage cost with it |
| **Orphan cleanup** | `remove_orphan_files` | files from failed writes never referenced and never deleted |
| **Manifest rewriting** | `rewrite_manifests` | the metadata itself becomes slow to read |
| Old metadata files | `write.metadata.delete-after-commit.enabled` | a table property, not a job — set it once |

The **small-files problem** is the one that degrades platforms gradually: a streaming write
committing every minute produces 1,440 files a day per partition, and query time becomes dominated
by opening files rather than reading them.

### Thresholds worth alerting on

Maintenance on a fixed schedule runs whether or not a table needs it. Measuring first is what turns
it from a cron job into a response:

| Signal | Healthy | Act |
|---|---|---|
| Average file size | **128–256 MB** for selective queries, 256–512 MB for full scans | below ~64 MB |
| File count per partition | — | above ~500 |
| Snapshot count | — | above ~1,000 |
| Manifests per data file | roughly **1 per 50–100 data files** | far denser than that |
| **Delete-file ratio** | — | **above 0.1 is accumulating; above 0.5 is a read emergency** |

The last row is the one most easily missed, and it only applies to **merge-on-read** tables.
Position and equality deletes accumulate alongside the data files, and every read has to merge them.
Nothing fails — reads simply get slower, in proportion to how much has been deleted or updated
since the last compaction. `rewrite_data_files` is what applies them.

### The order to run them in — and the disagreement about it

Published guidance contradicts itself here, and the contradiction is instructive rather than
academic:

| Source | Order |
|---|---|
| [LakeOps](https://lakeops.dev/blog/automating-iceberg-table-maintenance) | expire snapshots → remove orphans → **compact** → rewrite manifests |
| [Conduktor](https://www.conduktor.io/glossary/maintaining-iceberg-tables-compaction-and-cleanup) | **compact** → rewrite manifests → expire snapshots → remove orphans |

Both are internally coherent, and the difference is *when the garbage produced by compaction gets
collected*.

**Compaction creates garbage.** It writes new files and leaves the originals in place, still
referenced by older snapshots. Cleaning up before compacting therefore means the files compaction
just orphaned survive until the next cycle; cleaning up after collects them in the same pass.

That argues for compacting first, and it is the reason to prefer the second order unless there is a
specific reason not to. What matters more than which order is picked is that the operations run **as
one sequence**, close together. Run on separate days, each one misses the window in which its output
would have fed the next — which is the actual failure, not the ordering.

### The safety rules

Two of these operations can destroy data if run carelessly:

**`remove_orphan_files` must use an age threshold longer than your longest-running write.** A file
written by an in-flight transaction is indistinguishable from an orphan until the writer commits.
Deleting it corrupts the table. The guidance across all three sources converges on a **minimum
3-day margin**, with 7 days commonly recommended — and **run it in dry-run mode first**, every time.

**`expire_snapshots` destroys time travel.** Retention is the decision, not a default: roughly
**3–7 days for streaming tables, 14–30 days where batch or compliance requires it**, and always
`retain_last` above zero so a table is never left with a single snapshot. And the point from
[`../README.md`](../README.md#5-the-part-everyone-forgets-maintenance) stands — time travel is not a
backup, and expiry is what makes that concrete.

### What it costs

Compaction is the expensive one: roughly **1–2 minutes of compute per GB** rewritten. Across a
hundred tables on a nightly schedule, the maintenance bill can approach the query bill — which is
the real argument for triggering on the thresholds above rather than on a clock.

Two settings that help: **`partial-progress.enabled`** (Iceberg 1.6+) commits compaction in batches
so a failure part-way does not discard the whole job, and **`use_caching`** on `rewrite_manifests`
(1.3+) avoids re-reading metadata it has already seen.

## Notes

Reference material recorded here:

- [registering Iceberg files into Hive Metastore](https://atwong.medium.com/how-to-register-apache-iceberg-files-into-apache-hive-metastore-hms-5a4509da8224)
**On maintenance specifically**, three references worth reading in this order:

- [Iceberg table health and maintenance](https://lakeops.dev/blog/iceberg-table-health-maintenance)
  — start here. It is the one that turns maintenance from a list of procedures into **measurable
  signals**: what to look at, what a healthy value is, and which procedure each symptom maps to. The
  delete-file ratio framing is the part not covered well elsewhere.
- [Maintaining Iceberg tables: compaction and cleanup](https://www.conduktor.io/glossary/maintaining-iceberg-tables-compaction-and-cleanup)
  — the procedure reference: exact `CALL` syntax, strategies, the version-gated options
  (`partial-progress.enabled`, `use_caching`), and the safety rules around orphan removal.
- [Automating Iceberg table maintenance](https://lakeops.dev/blog/automating-iceberg-table-maintenance)
  — the operational argument: why a nightly cron across every table is wasteful, and what
  threshold-driven triggering looks like instead. Read it knowing that **LakeOps sells the control
  plane it recommends** — the critique of fixed schedules stands on its own, and the conclusion is a
  product pitch. The Airflow DAG it shows first is a perfectly reasonable place to start.

The two LakeOps articles and the Conduktor one **disagree on execution order**, which is discussed
above rather than smoothed over.

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
