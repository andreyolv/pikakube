[← SQL databases](../README.md)

# SQL Server

Present because it exists in real estates — and for a data platform, almost always as a source.

<https://github.com/microsoft/mssql-docker>
<https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-overview>

---

## Why it is here

Nobody builds a new data platform on SQL Server. Plenty of data platforms **read** from one,
because it is where a decade of line-of-business applications keep their data — ERP, CRM,
finance, and the internal systems nobody has migrated.

That framing decides what matters about it in this repository:

| Concern | Why |
|---|---|
| **CDC** | how data leaves it — SQL Server has first-class change data capture |
| **Extraction** | batch loads via [Airbyte](../../../analytics-engineering/integration/airbyte/README.md) or similar |
| Read replicas | so analytical reads never touch the transactional system |
| Licensing | the reason to avoid putting anything new on it |
| Collation and encoding | a recurring source of migration surprises |

## The licensing point, stated once

SQL Server is commercially licensed per core, and it is expensive. The Developer edition is free
and licensed for non-production use; the Express edition is free with hard limits — 10 GB per
database, capped memory and CPU.

The practical consequence for a platform: **there is no good reason to place new workloads
here.** Existing systems stay, and new ones go to
[PostgreSQL](../postgresql/README.md), which is why this folder is short.

## Running it on Kubernetes

Microsoft publishes Linux container images and it runs on Kubernetes without difficulty. The
sensible uses:

- a **local instance for development**, so an extraction pipeline can be tested against the real
  engine and its real quirks
- integration tests for a connector
- a restored copy for a migration exercise

For anything production, availability groups, licensing and support mean this is not the shape.
The deployment kept here — a Deployment, a PVC, a Service and a secret — is deliberately the
development shape.

## Getting data out

The two paths, and they answer different questions:

| Path | Use | Tooling |
|---|---|---|
| **CDC** | continuous, low-latency, captures every change | [Debezium](../../../data-streaming/README.md) reads the SQL Server CDC tables |
| **Batch extraction** | periodic full or incremental loads | [Airbyte](../../../analytics-engineering/integration/airbyte/README.md), [SeaTunnel](../../../analytics-engineering/integration/seatunnel/README.md) |

CDC has to be enabled per database and per table on the SQL Server side — it is not on by
default, and it creates capture tables and jobs that a DBA must agree to. Discovering that
requirement after designing the pipeline is the usual sequence.

The batch path is simpler and is the right default when hourly or daily freshness is acceptable.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| New workloads placed on it | per-core licensing, for something PostgreSQL does free | [PostgreSQL](../postgresql/README.md) |
| Analytical queries against the transactional instance | one report causes an unrelated production incident | a replica, or extract to the platform |
| Extracting with `SELECT *` on a schedule | full table scans against a live system | CDC, or incremental by a watermark column |
| Assuming CDC is available | it must be enabled per table, by someone with rights | confirm before designing the pipeline |
| Ignoring collation | case-insensitive by default, unlike PostgreSQL; joins and keys behave differently after migration | check it explicitly |
| Express edition in production | 10 GB per database, and it stops | Developer for dev, licensed for production |
| `datetime` mapped naively | precision and range differ from PostgreSQL's types | map types deliberately |

## Notes

Mapped as a **source system**, which is the honest position for this platform.

The deployment here is the development shape — a container, a volume and a secret — for testing
extraction against the real engine rather than against an approximation. That is worth having
precisely because the differences that break pipelines are the small ones: collation, datetime
precision, and identifier quoting.

The related folders: [`data-streaming/`](../../../data-streaming/README.md) for the CDC path, and
[`analytics-engineering/integration/`](../../../analytics-engineering/integration/README.md) for
batch extraction. Both treat SQL Server as one source among several, which is exactly how it
should appear.

---

[← SQL databases](../README.md)
