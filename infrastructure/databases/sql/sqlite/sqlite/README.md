[← SQLite](../README.md)

# sqlite

<https://github.com/sqlite/sqlite>

---

## The problem it solves

A full relational database — SQL, transactions, indexes, constraints, foreign keys — as a
**library reading and writing one file**.

There is no server, no port, no connection string and no user management. Opening the file is
connecting to the database.

It is the most deployed database in the world by a wide margin: every browser, every phone, most
desktop applications, and an enormous number of embedded systems.

## When to use it

- **a service with one writer** — read-heavy, modest writes, single node
- state a CLI or an agent must remember between runs
- local tooling and analysis scripts
- an application's file format, where the file happens to be queryable
- edge and offline, where there is no server to reach

## When not to use it

- **more than one process writing** — this is the hard limit; the workarounds are worse than a
  server
- multiple nodes needing the same data
- analytical scans over large datasets —
  [DuckDB](../../../../data-engineering/processing/duckdb/README.md) is the in-process database for
  that shape
- a network filesystem — see below

## Configuration, which is what makes it production-capable

Out of the box SQLite is tuned to be a file format. Four settings turn it into something suitable
for a service:

| Pragma | Why |
|---|---|
| **`journal_mode = WAL`** | readers stop blocking the writer. Close to mandatory for a service, and it is what [Litestream](../litestream/README.md) replicates |
| **`busy_timeout`** | without it, a concurrent write returns `SQLITE_BUSY` **immediately** instead of waiting |
| `synchronous` | `FULL` for maximum durability; `NORMAL` with WAL is the usual compromise |
| **`foreign_keys = ON`** | **off by default** — SQLite parses foreign-key clauses and does not enforce them |

The last row is a genuine trap and worth checking on any inherited SQLite database: constraints
can be declared, visible in the schema, and doing nothing. The pragma is per connection, so it
must be set every time.

## The network filesystem warning

SQLite's locking relies on the filesystem implementing POSIX advisory locks correctly. NFS
historically does not, reliably.

The result is **silent corruption** rather than an error. This is documented by the project and it
is worth restating because Kubernetes makes it easy to do accidentally — an RWX volume backed by
NFS looks like a convenient way to share a SQLite file between pods, and it is a way to destroy
it.

If the data must be shared, it needs a server database. If it must survive the node, that is what
[Litestream](../litestream/README.md) is for.

## What it is good at that people underestimate

| Property | Detail |
|---|---|
| **Reliability** | one of the most thoroughly tested pieces of software in existence — millions of tests, and full-coverage branch testing |
| **Longevity** | the file format is backwards-compatible and committed to being readable through 2050 |
| Performance | for single-writer workloads, faster than a server, because there is no network |
| Size | a few hundred kilobytes |

The testing point is not marketing. SQLite's test suite is disproportionate to its size and is the
reason it is trusted in aviation, medical devices and every phone.

## Notes

Mapped as the embedded relational option, alongside
[`in-memory/`](../in-memory/README.md) for tests and
[`litestream/`](../litestream/README.md) for durability.

For a Kubernetes platform the combination worth holding as a real alternative is **SQLite plus
Litestream**: one pod, one PVC, continuous replication to
[MinIO](../../../../site-reliability-engineering/storage/object-storage/minio/README.md). Several
platform components keep small amounts of state and imply a PostgreSQL instance to hold it — and
for a single-writer service, a replicated SQLite file is less to deploy, back up and break than a
database cluster.

---

[← SQLite](../README.md)
