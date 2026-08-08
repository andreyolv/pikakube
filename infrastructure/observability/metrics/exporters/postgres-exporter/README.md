[← Exporters](../README.md)

# PostgreSQL Exporter

<https://github.com/prometheus-community/postgres_exporter>

---

## The problem it solves

PostgreSQL health as Prometheus metrics: connections against the limit, transaction rates,
replication lag, cache hit ratio, locks, deadlocks, table and index sizes, vacuum activity.

The ones that actually matter in practice:

| Metric | Why |
|---|---|
| Connections vs `max_connections` | the most common Postgres outage — exhaustion, not load |
| Replication lag | a replica silently falling behind |
| Long-running transactions | they block vacuum and bloat the database |
| Cache hit ratio | a sustained drop usually means the working set outgrew memory |

## When to use it

- any PostgreSQL that matters — including [CloudNativePG](../../../../databases/sql/postgresql/operator/cnpg/) clusters
- you want the standard set without writing queries

## When not to use it

- you need metrics about the **data**, not the database — that is [sql-exporter](../sql-exporter/)
- CloudNativePG is in use and its built-in metrics already cover it; check before adding a second exporter

---

## Notes

> The community Grafana dashboards for this are mostly poor.

<https://grafana.com/grafana/dashboards/12485-postgresql-exporter/>

Worth knowing before spending an afternoon importing dashboards: most reference metrics that
are not enabled by default, or present panels that do not answer any real question. Building a
small dashboard around the four metrics above is usually faster than fixing an imported one.

Open item: <https://github.com/prometheus-community/postgres_exporter/pull/911>

---

[← Exporters](../README.md)
