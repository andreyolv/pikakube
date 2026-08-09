[← SQL databases](../README.md)

# MariaDB

<https://github.com/MariaDB/server>

---

## What it is

A fork of MySQL, created by MySQL's original author after Oracle's acquisition of Sun, and now a
database that has diverged enough to be a distinct choice rather than a compatible alternative.

The distinction that matters for a platform is governance: MariaDB Server is **GPLv2**, developed
in the open by the MariaDB Foundation. MySQL is Oracle's, with a community edition and a
commercial one.

## Where it has diverged

Early on it was a drop-in replacement. That is no longer safe to assume:

| Area | Detail |
|---|---|
| **Storage engines** | Aria, ColumnStore, Spider — MySQL has InnoDB and little else |
| **JSON** | MariaDB stores JSON as text with functions; MySQL has a native binary type |
| **System-versioned tables** | temporal tables built in — query a table as it was at a point in time |
| Replication | different GTID implementations; **not interchangeable** |
| Optimiser | different, with different plan choices |
| Sequences | MariaDB has real `SEQUENCE` objects |

**System-versioned tables are the feature worth knowing about.** `SELECT * FROM orders FOR SYSTEM_TIME AS OF '2026-01-01'` is temporal querying without an audit table and triggers, and it has no MySQL equivalent.

The replication row is the important warning: MariaDB and MySQL cannot replicate to each other
reliably across recent versions, which rules out several migration strategies that would otherwise
be obvious.

## When to use it

- **the licence and governance matter** — GPLv2, community-developed, no Oracle dependency
- ColumnStore or another MariaDB-specific engine is genuinely useful
- system-versioned tables solve an actual requirement
- the distribution is what the platform or distro already ships

## When not to use it

- **a new service** — [PostgreSQL](../postgresql/README.md) is usually the better answer; see
  [`../README.md`](../README.md#2-postgresql-is-usually-the-answer)
- MySQL-specific tooling or replication compatibility is required
- CDC tooling has been validated against MySQL specifically — see below
- the existing estate is MySQL and nothing forces a change

## The CDC question

The point that matters most for this repository.

MariaDB appears in a data platform the same way MySQL does — as a **source** to extract from, not
a target to build on. That makes the extraction path the deciding concern rather than the feature
list:

| Concern | Detail |
|---|---|
| **`binlog_format = ROW`** | CDC does not work properly without it; the same requirement as MySQL |
| **Connector support** | Debezium supports MariaDB, and the coverage and maturity are not identical to its MySQL support |
| GTID differences | replication-based tooling written for MySQL may not transfer |
| Batch extraction | [Airbyte](../../../analytics-engineering/integration/airbyte/README.md) and similar treat it as a distinct source |

The practical advice: **verify the specific connector against the specific MariaDB version**
before designing a pipeline around it. "It is MySQL-compatible" has been true enough for a long
time to be assumed, and it is exactly the assumption that fails at the replication layer.

## Notes

Mapped as a source system, which is the honest position — the same as
[MySQL](../mysql/README.md) and [SQL Server](../sqlserver/README.md).

Its realistic appearance here is an application database that a data platform reads from, chosen
by whoever built that application. In that position the questions are narrow: is `binlog_format`
set to `ROW`, and does the CDC connector actually support this version.

Where MariaDB genuinely wins over MySQL is **governance** — GPLv2 and a foundation rather than a
vendor with a commercial tier. For a repository that catalogues open-source tooling, that is not a
small point, even if it rarely decides an existing deployment.

---

[← SQL databases](../README.md)
