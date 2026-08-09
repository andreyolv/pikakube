[← Interoperability](../README.md)

# Delta UniForm

<https://github.com/delta-io/delta>

---

## The problem it solves

**Universal Format** — a Delta table that Iceberg readers can also read.

The insight it is built on is that the formats are less different than they look. Delta, Iceberg
and Hudi all store the same thing underneath: **Parquet files**. What differs is the metadata that
says which of those files constitute the table and what the schema is. The data does not need
converting; only the metadata does.

UniForm takes that literally. When enabled on a table, the Delta writer generates **Iceberg
metadata alongside the Delta transaction log**, as part of the commit. One set of Parquet files,
two metadata layers over it, both current.

| | Without UniForm | With it |
|---|---|---|
| Data files | Parquet | **the same Parquet** |
| Metadata | `_delta_log/` | `_delta_log/` **and** Iceberg metadata |
| Iceberg readers | cannot see the table | read it directly |
| Extra job to run | a conversion pipeline | **none** |
| Freshness of the second view | as stale as the last run | **current at every commit** |

The freshness row is the reason to prefer this over a translation job like
[XTable](../xtable/README.md) whenever it is available. A converted view that lags looks exactly
like a correct view; a commit-time write either succeeds or fails visibly.

## When to use it

- [Delta](../../table-formats/delta/README.md) is the writer and cannot change — Databricks, or an
  existing Delta estate
- a consumer requires [Iceberg](../../table-formats/iceberg/README.md) specifically, and cannot be
  pointed at Delta
- during a **migration**, where both must be readable for a bounded period
- the alternative on the table is copying the data into a second format, which is worse

## When not to use it

- the format decision is still open — decide it; see
  [`table-formats/`](../../table-formats/README.md)
- Iceberg is already the writer; this runs in the other direction
- Iceberg-specific write features are wanted — the Iceberg view is **read-only**, and the Delta
  side remains the writer
- the consumer could read Delta with a small change; that is less machinery than a second metadata
  layer on every commit

## What it does not give you

| | Reality |
|---|---|
| **Direction** | Delta is the writer. The Iceberg view is for reading, and writing to it is not the model |
| **Feature parity** | an Iceberg reader sees a table, not Delta's change data feed or Delta-specific behaviour |
| **Iceberg's own features** | hidden partitioning and partition evolution belong to tables Iceberg wrote; they are not conferred by the metadata |
| **The catalog** | the Iceberg view still has to be registered somewhere engines look — see [`metadata-catalog/`](../../../metadata-catalog/README.md) |
| **Commit cost** | writing two metadata layers is not free, and it is on the write path |
| Version coupling | which Delta and Iceberg versions interoperate is version-specific; verify against the engines in use |

## Notes

Recorded reference:

- [Delta UniForm documentation](https://docs.delta.io/latest/delta-uniform.html)

The state of it here: [Delta](../../table-formats/delta/README.md) records UniForm testing as
**partially done**. That is worth reading as what it is — a feature that was tried, not one that is
relied on.

**Where it fits in the argument this folder makes.** UniForm is the least-bad shape an
interoperability tool can take, because the second metadata layer is written by the same commit
that writes the data. There is no separate job, no lag, and no window in which the two views
disagree. Compare [XTable](../xtable/README.md), which is a job you schedule and therefore a job
that can silently fall behind.

That does not make it a strategy. It makes it a **good bridge**, and bridges should have an end
date — see [`../README.md`](../README.md). The reason to reach for it is that Delta is already the
writer and something needs Iceberg; the reason not to is that neither of those is true here.

For pikakube the recorded position is Iceberg as the primary format on
[MinIO](../../storage/minio/README.md), which puts this in the wrong direction — this platform
would need Iceberg tables readable as Delta, not the reverse. It stays mapped because the Delta
notes reference it and because the mechanism is the one worth understanding.

---

[← Interoperability](../README.md)
