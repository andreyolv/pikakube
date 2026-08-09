[← Data Engineering](README.md)

# File formats

How bytes are laid out on disk — the decision underneath every engine in this discipline.

References: [Parquet](https://github.com/apache/parquet-format) ·
[ORC](https://github.com/apache/orc) · [Avro](https://github.com/apache/avro) ·
[Arrow](https://github.com/apache/arrow)

---

## Row or column

The distinction that explains all the others:

| | Row-oriented | Column-oriented |
|---|---|---|
| Stores | one record after another | one column after another |
| Good at | reading or writing **whole records** | reading **a few columns of many records** |
| Compression | limited — adjacent values differ | excellent — adjacent values are the same type and often similar |
| Formats | Avro, JSON, CSV | **Parquet**, ORC |

An analytical query reads three columns out of eighty. Row storage must read all eighty to get
them; columnar reads three. That single fact is why Parquet became the default for analytics.

## The four

| Format | Orientation | Use it for |
|---|---|---|
| **Parquet** | columnar | **the default for analytics** — the lakehouse standard, supported by everything |
| **ORC** | columnar | the Hive ecosystem, where it is the native format |
| **Avro** | row-based | **streaming and interchange** — schema always present, strong evolution rules |
| **Arrow** | columnar, **in memory** | not a storage format — the in-memory representation engines share |

**Arrow is not a file format.** It is the in-memory layout, and its value is that engines can
exchange data without serialising: DuckDB, Spark, pandas and Polars can hand each other the
same buffers. When a tool claims "zero-copy" interoperability, this is what it means.

**Avro's place is the stream**, not the lake. Records are written whole, the schema travels with
the data, and evolution rules are strict — which is exactly what a
[schema registry](../data-streaming/schema-registry/README.md) needs and what analytics does
not.

## What makes Parquet fast

Worth knowing, because it explains how to make it slow:

| Feature | Effect |
|---|---|
| **Row groups** | data split into chunks, each with statistics |
| **Min/max statistics** | a query can skip an entire row group without reading it |
| **Predicate pushdown** | filters are applied during the read, not after |
| **Encoding per column** | dictionary, run-length, delta — chosen per column type |

The statistics are the mechanism behind most performance advice: sorting data by the column you
filter on makes min/max ranges narrow, and narrow ranges mean whole row groups get skipped.

## The small-files problem

The most common performance failure in a lakehouse, and it is a consequence of these formats
rather than of any engine.

Each file carries metadata that must be read and each read is a request. Ten thousand 1 MB
files cost far more than one hundred 100 MB files with identical content — the query spends its
time on metadata and network round trips rather than on data.

Streaming ingestion produces exactly this shape, which is why compaction is a permanent
maintenance job rather than a one-off fix. The table formats in
[`data-governance/`](../data-governance/) — Iceberg, Delta, Hudi — exist partly to manage it.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| CSV or JSON in the lake | no schema, no statistics, no pushdown, poor compression | Parquet |
| Avro for analytical tables | row-based, so every query reads every column | Parquet |
| Ignoring small files | metadata and round trips dominate the query | compaction as scheduled maintenance |
| Unsorted data on the filter column | statistics are useless and no row group can be skipped | sort by what you filter on |
| Over-partitioning | thousands of tiny partitions recreate the small-files problem | partition by cardinality that matters |
| Treating Arrow as a storage format | it is a memory layout | Parquet on disk, Arrow in flight |

---

[← Data Engineering](README.md)
