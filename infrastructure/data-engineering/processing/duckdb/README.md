[← Processing](../README.md)

# DuckDB

<https://github.com/duckdb/duckdb>
<https://duckdb.org/docs/>

---

## The problem it solves

An in-process analytical database — SQLite's model, applied to OLAP. No server, no cluster, no
coordination: a library that reads Parquet, CSV and JSON directly and runs vectorised columnar
queries on one machine.

Its importance in a data platform is not what it does. It is **what it makes unnecessary**:

| Assumed to need a cluster | Actually |
|---|---|
| Aggregating a few hundred GB of Parquet | one machine, minutes |
| Joining files on object storage | `SELECT ... FROM 's3://bucket/*.parquet'` |
| Transforming data in a pipeline step | a library import, no infrastructure |
| Ad-hoc exploration of lake files | faster than submitting a Spark job |

A large share of jobs running on Spark would finish faster here, because coordination overhead
exceeds the work. That is the argument the [processing](../README.md#1-the-question-to-ask-first)
folder opens with, and this is the tool it points at.

## When to use it

- data fits on one machine — which reaches much further than people assume
- **inside a pipeline step**, as a library rather than a service
- exploring Parquet on object storage without a cluster
- local development against the same files production uses
- as the engine behind [dbt](../../../analytics-engineering/transform/dbt/README.md) for smaller models

## When not to use it

- the data genuinely does not fit, or volume is elastic — [Spark](../spark/README.md)
- many concurrent users need a shared service; this is in-process by design
- it is the system of record. It is an analytical engine, not a database to write to

## The threshold question

The useful heuristic: **how much data does one query actually touch?**

Columnar formats and predicate pushdown mean a query over a terabyte of Parquet may read ten
gigabytes. Partitioning and column pruning move the ceiling much further than the total dataset
size suggests.

Measure the query, not the lake.

---

## Notes

```bash
python3 -m venv venv
source venv/bin/activate
# deactivate

pip install duckdb
```

### Related, for when one node is not enough

- [smallpond](https://github.com/deepseek-ai/smallpond) — distributed DuckDB from DeepSeek
- [3FS](https://github.com/deepseek-ai/3FS) — the distributed filesystem underneath it

Worth knowing about as the middle ground: distribution without adopting Spark's full model.

---

[← Processing](../README.md)
