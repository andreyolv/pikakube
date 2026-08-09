[← Database monitoring](../README.md)

# PMM — Percona Monitoring and Management

<https://github.com/percona/pmm>
<https://github.com/percona/grafana-dashboards>

---

## What it is

A monitoring **platform** for databases rather than a tool: a server, agents on each database
host, and a bundled Grafana with curated dashboards.

Its two distinguishing properties:

**It is multi-engine.** PostgreSQL, MySQL, MariaDB and MongoDB, in one place, with dashboards
designed for each. Nothing else in this folder covers a mixed estate.

**Query Analytics.** Per-query metrics over time — which queries consume the most time, how their
plans and latencies change, and what a deployment did to them. That is the feature people adopt
PMM for, and it goes further than [pghero](../pghero/README.md)'s point-in-time view.

| Component | Role |
|---|---|
| PMM Server | storage, UI and the bundled Grafana |
| **pmm-agent** | runs beside each database, collecting metrics and query data |
| **Query Analytics (QAN)** | per-query performance, with history |
| Dashboards | [percona/grafana-dashboards](https://github.com/percona/grafana-dashboards) — curated, and genuinely good |
| Advisors | automated checks for configuration and security issues |

## When to use it

- a **mixed estate** — PostgreSQL *and* MySQL *and* MongoDB
- **query performance over time** is the question, not just right now
- curated dashboards are worth more than assembling your own
- Percona's operators are already in use — [MongoDB](../../../nosql/document/mongo/percona-mongodb-operator/README.md)
  integrates with it directly

## When not to use it

- **one PostgreSQL cluster** — it is a platform, and
  [pghero](../pghero/README.md) plus
  [postgres-exporter](../../../../observability/metrics/exporters/postgres-exporter/README.md)
  cover it with a fraction of the footprint
- metrics should live in the platform's existing Prometheus rather than in a parallel stack
- an agent per database host is unwelcome
- the bundled Grafana would duplicate the one already running

## The parallel-stack problem

The main architectural objection, and it is worth deciding deliberately rather than discovering.

PMM brings its own storage, its own Grafana and its own alerting. A platform that already runs
[Prometheus](../../../../observability/metrics/storage/prometheus/README.md) and
[Grafana](../../../../observability/dashboards/grafana/README.md) then has two monitoring stacks —
and the database one is the one nobody opens, because it is not where the rest of the platform's
telemetry lives.

Two ways out:

| Approach | Detail |
|---|---|
| **Federate** | scrape PMM's metrics into the platform's Prometheus, and use PMM mainly for QAN |
| **Do not deploy the server** | use [postgres-exporter](../../../../observability/metrics/exporters/postgres-exporter/README.md) for metrics and pghero for diagnosis |

The second is the right default for a single-engine estate. The first is worth the effort when
Query Analytics is genuinely the reason for adopting it.

## The dashboards are worth taking regardless

[percona/grafana-dashboards](https://github.com/percona/grafana-dashboards) is a curated set,
maintained by people who operate these databases professionally.

That matters because of a finding recorded elsewhere in this repository: the **community Grafana
dashboards for postgres-exporter are mostly poor** — broken against current metric names, or
displaying numbers that answer no question anyone asks. Percona's are a better starting point,
and they can be used without deploying PMM itself.

## Notes

Mapped as part of the monitoring set here, and it is the option that covers a **mixed estate** —
which for this platform is a real consideration, since PostgreSQL, MySQL and MongoDB all appear
in [`databases/`](../../../README.md).

The realistic recommendation for the current shape: the platform runs one PostgreSQL cluster under
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md), so
[postgres-exporter](../../../../observability/metrics/exporters/postgres-exporter/README.md) plus
[pghero](../pghero/README.md) is proportionate, with **Percona's dashboards borrowed** rather than
the platform deployed.

PMM becomes the right answer when there is more than one engine to monitor, or when Query
Analytics over time is the question being asked.

---

[← Database monitoring](../README.md)
