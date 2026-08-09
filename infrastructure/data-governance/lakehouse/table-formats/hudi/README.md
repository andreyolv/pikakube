[← Table formats](../README.md)

# Apache Hudi

<https://github.com/apache/hudi>

---

## The problem it solves

Hudi came from Uber, and it was built for a specific shape that the other formats handle less
directly: **high-volume upserts from CDC**, with incremental consumption downstream.

Its distinguishing capabilities follow from that origin:

| Capability | Why it matters for CDC |
|---|---|
| **Record-level index** | find the file containing a given key without scanning — this is what makes upserts efficient |
| **Incremental queries** | read only what changed since a commit, so downstream jobs are incremental by construction |
| **Merge-on-Read** | writes go to delta logs and are merged at read time — fast ingest, slower reads |
| Copy-on-Write | files rewritten on write — slower ingest, faster reads |
| Automatic file sizing | compaction and clustering managed as table services |
| Concurrency control | optimistic, with configurable conflict resolution |

## Copy-on-Write vs Merge-on-Read

The decision that shapes everything else, and it is Hudi's most distinctive design choice:

| | **Copy-on-Write** | **Merge-on-Read** |
|---|---|---|
| A write | rewrites the affected Parquet files | appends to a row-based delta log |
| Write latency | **higher** | **lower** |
| Read cost | plain Parquet, fast | merge log with base at read time |
| Compaction | not needed | **required**, on a schedule |
| Fits | read-heavy, batch-updated tables | **streaming ingest, frequent upserts** |

Merge-on-Read is the mode that makes near-real-time CDC ingestion practical, and it is also the
mode that fails quietly when compaction is not scheduled — the delta logs grow and read
performance degrades gradually.

## When to use it

- **CDC ingestion with heavy upserts**, where the record-level index earns its cost
- downstream pipelines should consume **incrementally** rather than rescanning
- near-real-time ingest with Merge-on-Read
- an existing Hudi estate

## When not to use it

- general analytical tables — [Iceberg](../iceberg/README.md) is simpler and more widely supported
- **many engines** read the same data; Hudi's support outside Spark and Flink is thinner
- the operational surface is a concern — table services, compaction and clustering are real
  ongoing work
- **the documentation is a blocker for your integration** — see the notes

## Notes

Recorded from working through it:

> Integration with AWS S3 / MinIO — **partially done**
>
> Integration with Hive Metastore — **partially done**
>
> **The documentation for those cases is very poor.**

That verdict is worth taking at face value and is consistent with the pattern across this whole
folder: **the format is the easy part, and the storage and catalog integration is where the time
goes.** Three of the five formats here have recorded documentation failures at exactly the step of
connecting to S3-compatible storage — which is not a coincidence, it is the least-tested path in
most of these projects.

Reference material that filled the gap:

- [Hudi with S3 and Spark SQL](https://github.com/dipankarmazumdar/HudiCodeExamples/blob/main/Hudi_S3_SparkSQL.ipynb)
- [MinIO's write-up on Hudi with HMS](https://blog.min.io/datalakes-with-hudi-and-hms/)

Both are third-party, which is itself the finding: the useful material for the integration this
platform needs was not the project's own documentation.

## The honest position

Hudi solves a real problem well, and it is the narrowest of the formats in this folder.

If the workload genuinely is **CDC upserts at volume with incremental downstream consumption**, the
record-level index and incremental queries are capabilities the others do not match directly.

If it is not — and for most analytical work it is not —
[Iceberg](../iceberg/README.md) is the better default: broader engine support, hidden partitioning,
partition evolution, and integration paths that are documented.

For this platform, [`../README.md`](../README.md#7-how-this-applies-to-pikakube) recommends
Iceberg for exactly that reason. Hudi is catalogued as the answer to a specific question, with the
recorded caveat that getting it connected to object storage cost more than it should have.

---

[← Table formats](../README.md)
