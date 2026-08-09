[← Database monitoring](../README.md)

# pgbadger

<https://github.com/darold/pgbadger>

---

## The problem it solves

**Post-incident analysis, with no agent and nothing deployed in advance.**

pgbadger is a Perl script that parses PostgreSQL log files and produces a self-contained HTML
report. There is no server, no collector, no database and no prior installation — point it at logs
that already exist and it produces the analysis.

That property makes it uniquely useful for the situation nobody plans for: something went wrong on
a database that was not instrumented, and the only evidence is the logs.

```bash
pgbadger /var/log/postgresql/postgresql-*.log -o report.html
```

## What the report contains

| Section | What it answers |
|---|---|
| **Slowest queries** | ranked by total time and by frequency, with examples |
| **Time distribution** | when the load actually happened |
| Errors and fatals | grouped, with counts |
| **Locks and waits** | what was blocking what |
| Connections | sessions over time, and by host |
| Checkpoints and vacuum | how often, how long, and whether they were forced |
| Temporary files | queries spilling to disk, which means `work_mem` is too small |

The temporary-files section is the one people are surprised by. A query that exceeds `work_mem`
writes to disk silently, and it is a common cause of "the query got slower and nothing changed" —
visible here and almost nowhere else.

## When to use it

- **analysing an incident afterwards**, from logs already on disk
- a database nobody instrumented, where the logs are the only evidence
- a one-off performance review, without deploying anything
- producing a report for someone who will not open Grafana

## When not to use it

- **live monitoring or alerting** — it is offline analysis; use
  [postgres-exporter](../../../../observability/metrics/exporters/postgres-exporter/README.md)
  with Prometheus
- current state during an incident — [pghero](../pghero/README.md) shows what is happening now
- query performance trends over time — [PMM](../pmm/README.md)'s Query Analytics
- MySQL or MongoDB — this is PostgreSQL-only

## The prerequisite

The logs must contain something worth parsing, and the default configuration does not produce it.

| Setting | Why |
|---|---|
| **`log_min_duration_statement`** | the threshold above which queries are logged — this is the one that matters |
| `log_checkpoints` | so checkpoint frequency and duration appear |
| `log_lock_waits` | so blocking is visible |
| `log_temp_files` | so spills to disk are recorded |
| **`log_line_prefix`** | pgbadger needs specific fields; the recommended prefix is in its documentation |
| `lc_messages = 'en_US.UTF-8'` | it parses English messages; a localised server produces an empty report |

The last row catches people and is easy to miss: on a server logging in another language,
pgbadger parses nothing and reports no errors about it.

The trade on `log_min_duration_statement` is the usual one — a low threshold captures everything
and generates a lot of log volume. Setting it to something like 250ms is a reasonable default that
keeps the evidence useful without flooding the disk.

## Notes

Mapped alongside [pghero](../pghero/README.md) and [PMM](../pmm/README.md), and it occupies the
position the other two do not: **offline, retrospective, and requiring nothing to have been
installed beforehand.**

The practical value for this platform is preparation rather than deployment. Setting
`log_min_duration_statement` and the recommended `log_line_prefix` on the
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) cluster costs nothing and means
the evidence exists when it is wanted — which is the only time anyone thinks about it.

The logs themselves flow into the platform's existing pipeline via
[`observability/logs/`](../../../../observability/logs/README.md), so the report is generated from
data that is already being collected.

---

[← Database monitoring](../README.md)
