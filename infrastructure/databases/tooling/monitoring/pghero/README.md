[← Database monitoring](../README.md)

# pghero

<https://github.com/ankane/pghero>

Multiple databases:
<https://github.com/ankane/pghero/blob/master/guides/Docker.md#customization--multiple-databases>

---

## The problem it solves

The highest value per unit of effort for PostgreSQL. A small web interface that answers the three
questions actually asked during an incident:

| Question | What it shows |
|---|---|
| **What is slow?** | queries ranked by total time, from `pg_stat_statements` |
| **What is blocking?** | live queries, locks, and which session is holding things up |
| **What is wasteful?** | unused indexes, duplicate indexes, missing indexes on foreign keys |

Plus the ones that predict problems rather than explain them: table and index bloat, connection
usage against the limit, replication lag, vacuum status, and long-running transactions.

It is a Rails application with a database connection. There is no agent, no collector and no
storage layer — it queries PostgreSQL's own statistics views and renders them.

## When to use it

- **PostgreSQL, and someone needs to answer "why is it slow?"** without a research project
- unused and missing indexes should be visible rather than guessed at
- a small, low-commitment tool is preferred to a monitoring platform
- during incidents, where a blocked-session view is worth more than a dashboard

## When not to use it

- **alerting** — it is a diagnosis tool, not a monitoring system. Use
  [postgres-exporter](../../../../observability/metrics/exporters/postgres-exporter/README.md)
  with Prometheus for anything that must page someone
- MySQL or MongoDB — [PMM](../pmm/README.md) covers a mixed estate
- historical analysis over months; retention here is limited
- offline post-incident analysis from logs — [pgbadger](../pgbadger/README.md)

## The prerequisite

**`pg_stat_statements` must be enabled**, and it is not on by default.

Without it, the query-performance section — the main reason to deploy pghero — is empty. It
requires the extension in `shared_preload_libraries`, which means a restart, so it is worth
enabling before it is needed rather than during an incident.

With [CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) this is a cluster
configuration setting rather than a manual change, which makes it straightforward to do
correctly.

## Access, which is the thing to get right

pghero reads statistics and, with a suitable role, can also terminate queries. That makes it
production database access with a friendly interface, and the caveats in
[`management/`](../../management/README.md) apply in full:

| Concern | What to do |
|---|---|
| **Credentials** | a dedicated role with `pg_monitor`, not a superuser |
| Exposure | internal ingress with authentication in front, never public |
| Kill-query capability | grant it deliberately, or not at all |
| Multiple databases | supported — see the [guide](https://github.com/ankane/pghero/blob/master/guides/Docker.md#customization--multiple-databases) |

`pg_monitor` is the correct role: it exposes the statistics views without granting data access,
which is exactly the separation wanted here.

## Notes

Mapped as part of the PostgreSQL monitoring set here, alongside
[PMM](../pmm/README.md) and the
[postgres-exporter](../../../../observability/metrics/exporters/postgres-exporter/README.md).

The division of labour worth keeping clear, from
[`../README.md`](../README.md#2-two-different-jobs): the exporter and Prometheus are what **wake
someone up**; pghero is what they **open next**. Both are needed, and expecting either to do the
other's job produces either alert fatigue or a slow incident.

The multi-database guide is recorded because the default configuration assumes one — and on a
platform where CloudNativePG runs several clusters, that is the first thing to change.

---

[← Database monitoring](../README.md)
