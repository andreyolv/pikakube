[← SQLite](../README.md)

# SQLite in-memory

<https://github.com/sqlite/sqlite>

---

## What it is

SQLite with the database held entirely in memory, created by connecting to `:memory:`:

```python
import sqlite3
conn = sqlite3.connect(":memory:")
```

The database exists for the life of the connection and disappears with it. Nothing is written to
disk, nothing needs cleaning up, and creation costs microseconds.

## The case it is actually for: tests

This is the reason the folder exists, and it is a genuinely better pattern than the alternative.

| | A database container per test run | In-memory SQLite |
|---|---|---|
| Startup | seconds | **microseconds** |
| Isolation | shared, usually — with cleanup between tests | **one database per test** |
| Parallelism | contended | **trivially parallel** |
| Cleanup | truncate, or transactions rolled back | **none — it ceases to exist** |
| Flakiness | ordering and leftover state | none |
| CI dependencies | Docker, a service, a health check | **nothing** |

The isolation property is the one that changes how tests are written. Each test gets a fresh
database, so there is no shared state to reset, no ordering dependency, and no "this test only
fails when run after that one".

## The trade, stated honestly

**The tests then run against a different engine than production.**

That matters or it does not, depending on what is being tested:

| Testing | In-memory SQLite |
|---|---|
| Application logic and control flow | **fine** |
| ORM mappings and relationships | mostly fine |
| **PostgreSQL-specific SQL** | **not fine** — `JSONB`, arrays, window-function edge cases, `RETURNING` |
| Migrations | not fine — dialects differ |
| Query plans and performance | meaningless |
| Concurrency behaviour | meaningless — different locking model entirely |

The honest position is a **split**: fast in-memory tests for the majority of the suite, and a
smaller set of integration tests against real PostgreSQL for the parts that depend on it.

Using in-memory SQLite for everything and discovering the dialect gap in production is the failure
this pattern is known for. Refusing to use it at all and running every test against a container is
the slower failure.

## Other uses

Smaller, and worth knowing:

- **ephemeral computation** — load data, query it with SQL, discard it. Often clearer than
  writing the equivalent logic by hand
- prototyping a schema before deciding where it will live
- caching structured data within a process, queryable rather than looked up

For analytical work over larger data, the in-process answer is
[DuckDB](../../../../data-engineering/processing/duckdb/README.md) rather than this — same "no
server" property, columnar rather than row-oriented.

## The gotcha

Each connection to `:memory:` creates a **separate** database. Code that opens a second connection
finds an empty one, which is confusing the first time.

The fix is a shared cache, or holding a single connection open for the lifetime of the test:

```python
sqlite3.connect("file::memory:?cache=shared", uri=True)
```

With SQLAlchemy, a `StaticPool` achieves the same thing — otherwise the pool hands out new
connections and each gets its own empty database.

## Notes

Mapped as the testing option alongside [`sqlite/`](../sqlite/README.md) and
[`litestream/`](../litestream/README.md).

For this platform the relevance is to the Python components — anything using SQLAlchemy, which
includes [Airflow](../../../../data-engineering/orchestration/airflow/README.md) and any service
built with it. A test suite that starts instantly and parallelises cleanly is worth the dialect
split, provided the split is deliberate and the PostgreSQL-specific parts are covered separately.

---

[← SQLite](../README.md)
