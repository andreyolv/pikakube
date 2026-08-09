[← Table formats](../README.md)

# Delta Lake

<https://github.com/delta-io/delta>
<https://github.com/delta-io/delta-rs>
<https://github.com/delta-io/kafka-delta-ingest>

---

## The problem it solves

ACID tables on object storage, originally from Databricks and now a Linux Foundation project. It
is the format with the **deepest Spark integration** and the largest installed base, because it
arrived first and because Databricks is built on it.

The mechanism is a transaction log: an ordered set of JSON commit files in `_delta_log/`,
periodically checkpointed to Parquet. A reader reconstructs the current file list from the log
rather than by listing the directory — which is what gives it atomicity and consistent reads.

| Capability | Detail |
|---|---|
| ACID transactions | via the ordered transaction log |
| **Spark integration** | the deepest of any format; `MERGE INTO` is first-class |
| Time travel | by version number or timestamp |
| Schema evolution and enforcement | including rejecting non-conforming writes |
| **`delta-rs`** | read and write **without a JVM** — Rust, with Python bindings |
| Change data feed | row-level changes between versions |
| Liquid clustering | an alternative to partitioning, on newer versions |

## `delta-rs` is the part worth knowing about

[delta-rs](https://github.com/delta-io/delta-rs) implements Delta in Rust, with Python bindings.
That means Delta tables can be read and written from a Python process with no Spark, no JVM and no
cluster — which changes what the format is useful for.

Paired with [DuckDB](../../../../data-engineering/processing/duckdb/README.md) or Polars, it makes
Delta a reasonable choice for work that would otherwise need Spark purely to touch the table. It
is the same argument [PyIceberg](../iceberg/README.md) makes on the Iceberg side.

## When to use it

- **Databricks is the platform** — this is the native format, and the argument ends there
- Spark is the primary engine and `MERGE INTO` is used heavily
- `delta-rs` opens up non-JVM access that matters for the workload
- an existing Delta estate

## When not to use it

- **multiple engines** read the same tables — [Iceberg](../iceberg/README.md) has broader and more
  mature support outside Spark
- partition evolution matters; Delta has no equivalent, and repartitioning means a rewrite
- Flink-first streaming — [Paimon](../paimon/README.md)
- record-level upsert indexes for CDC — [Hudi](../hudi/README.md)

## Delta or Iceberg

The comparison that matters, since both are credible and the choice is usually between them:

| | Delta | [Iceberg](../iceberg/README.md) |
|---|---|---|
| Spark integration | **deepest** | very good |
| Engine support beyond Spark | good, improving | **broadest** |
| **Hidden partitioning** | no | **yes** |
| **Partition evolution** | no | **yes** |
| Non-JVM access | **`delta-rs`** | PyIceberg |
| Governance | Linux Foundation, Databricks-led | Apache, vendor-neutral in practice |
| Catalog requirement | optional; the log is self-describing | **required** |

The last row is a genuine difference in operating model. A Delta table can be read from a path
alone, which is simpler; Iceberg requires a catalog, which is more infrastructure and is what makes
concurrent multi-engine writes safe.

**Iceberg for a multi-engine platform; Delta when Spark or Databricks is the centre of gravity.**

## Notes

Recorded from working through the integrations:

- Integration with **AWS S3 / MinIO**
- Integration with **Hive Metastore** —
  [how to register Delta files into HMS](https://atwong.medium.com/how-to-register-delta-lake-open-table-format-files-into-apache-hive-metastore-hms-2e6b886add93)
- Integration with the Spark Operator — noted as partially done
- Universal Format (UniForm) testing — noted as partially done; see
  [`interoperability/uniform/`](../../interoperability/uniform/README.md)

[kafka-delta-ingest](https://github.com/delta-io/kafka-delta-ingest) is worth singling out: it
writes from Kafka directly into Delta, in Rust, without Spark. For a platform that already runs
[Kafka or Redpanda](../../../../data-streaming/README.md), that removes a processing engine from
the ingestion path entirely — the same argument
[GlassFlow](../../../../data-streaming/processing/glassflow/README.md) makes for ClickHouse.

The [`notebooks/`](notebooks/README.md) folder holds a hands-on Delta walkthrough with Jupyter and Spark.

The recurring finding across this whole folder applies here too, and Delta comes off comparatively
well: the format is straightforward, and the **storage and catalog integration is where the time
goes**. [Hudi](../hudi/README.md) and [Paimon](../paimon/README.md) both have recorded
documentation failures at exactly that step; Delta's are documented.

---

[← Table formats](../README.md)
