[← Exporters](../README.md)

# SQL Exporter

<https://github.com/burningalchemist/sql_exporter>

---

## The problem it solves

Database exporters expose the metrics **the database** cares about — connections, locks,
replication lag. They say nothing about the data inside it.

sql_exporter runs **arbitrary queries** on a schedule and turns the results into Prometheus
metrics. Any question expressible in SQL becomes a metric, and therefore alertable.

Supports PostgreSQL, MySQL, SQL Server, Snowflake, ClickHouse and more, with several targets
from one deployment.

## Why this is the important one for a data platform

Data quality monitoring usually means adopting a new tool and a new pipeline. This turns it
into a query:

| Question | Metric |
|---|---|
| Is the table fresh? | `SELECT extract(epoch from now() - max(updated_at)) FROM orders` |
| Did the load complete? | `SELECT count(*) FROM orders WHERE loaded_at > current_date` |
| Are records being rejected? | `SELECT count(*) FROM staging_errors WHERE created_at > now() - interval '1 hour'` |
| Is the queue backing up? | `SELECT count(*) FROM jobs WHERE status = 'pending'` |

Those land in the **same Prometheus, same Alertmanager, same dashboards** as everything else —
no new system, no new on-call surface. For a platform that already runs this stack, it is the
cheapest route to freshness and completeness alerting that exists.

## When to use it

- data quality and freshness alerting without a dedicated tool
- business metrics that live in the database and nowhere else
- anything a specific exporter does not cover

## When not to use it

- database health metrics — [postgres-exporter](../postgres-exporter/) is purpose-built
- heavy analytical queries; the exporter runs them on schedule and becomes load on the database
- full data quality management with lineage and expectations — that is
  [`data-governance/quality/`](../../../../data-governance/quality/)

## The two rules

**Queries must be cheap.** They run on every scrape. A query that takes 30 seconds will
eventually run concurrently with itself. Set timeouts and long intervals.

**Do not label by row identity.** A label per customer or per table row is a cardinality bomb —
see [cardinality](../../README.md#3-cardinality-is-the-whole-game). Aggregate in the query.

---

[← Exporters](../README.md)
