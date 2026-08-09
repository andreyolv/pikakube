[← Time-series databases](../README.md)

# QuestDB

<https://github.com/questdb/questdb>
<https://github.com/questdb/questdb-kubernetes>

---

## The problem it solves

Very high ingest throughput, queried in **SQL** rather than in a bespoke language.

That combination is the argument. [InfluxDB](../influxdb/README.md) has the ecosystem and asked
people to learn Flux; QuestDB keeps SQL and optimises the write path aggressively.

| Property | Detail |
|---|---|
| **SQL** | with time-series extensions — `SAMPLE BY`, `LATEST ON`, `ASOF JOIN` |
| **Ingest rate** | very high; this is what it is built for |
| Line protocol | accepts InfluxDB's, so Telegraf and existing writers work |
| PostgreSQL wire protocol | existing Postgres clients and BI tools connect |
| Columnar, time-partitioned | on-disk layout designed for time-range scans |
| Written in | Java, with heavy use of off-heap memory and SIMD |

**`ASOF JOIN` is the feature worth knowing about.** It joins two time-series on the nearest
preceding timestamp — trades against the prevailing quote, readings against the most recent
configuration. Expressing that in standard SQL is a window function and a subquery; here it is a
join. Financial tick data is the canonical case, and it generalises to any "what was the state at
this moment" question.

## When to use it

- **ingest rate is the constraint**, measurably
- SQL should be the interface, for people and for tooling
- `ASOF JOIN` or `SAMPLE BY` maps directly onto the questions being asked
- an existing InfluxDB line-protocol writer should keep working

## When not to use it

- **PostgreSQL is already running** and the volume is moderate —
  [TimescaleDB](../timescaledb/README.md) adds no new system
- the Telegraf ecosystem and Influx dashboards are the requirement —
  [InfluxDB](../influxdb/README.md)
- **infrastructure metrics** — see
  [`observability/metrics/`](../../../../observability/metrics/README.md)
- horizontal scale-out is required; the open-source edition is single-node

## The single-node point

Worth being explicit about. QuestDB's open-source edition runs on **one node**. Replication and
clustering belong to the enterprise offering.

For time-series that is less limiting than it sounds — one node handles a great deal, and the
data is often reproducible from its source. It does mean high availability is not available at
any configuration of the open-source edition, which is the same position as
[Neo4j Community](../../graph/neo4j/README.md#the-licence-which-is-the-recurring-issue) and should
be established with equal clarity.

## What to configure

| Setting | Why |
|---|---|
| **Partition granularity** | `DAY`, `MONTH` or `YEAR` per table; it decides how much is scanned and how retention works |
| **Designated timestamp** | the column that makes a table a time-series; ordering and partitioning depend on it |
| Out-of-order tolerance | QuestDB handles out-of-order writes, with a cost worth understanding at high rates |
| Retention | dropping partitions is the mechanism — cheap, and it requires the partitioning to match |
| Storage | it is I/O-bound at high ingest; the storage class matters |

## Notes

Mapped with [questdb-kubernetes](https://github.com/questdb/questdb-kubernetes).

For this platform it is the answer to a narrow question — *"the ingest rate is the problem, and
SQL must stay the interface"* — and that question is not currently being asked here. The
recommendation in [`../README.md`](../README.md#7-how-this-applies-to-pikakube) remains
TimescaleDB, for the reason that it is an extension to a database that already exists.

It is worth keeping visible because it is the one entry in this folder whose argument is
throughput rather than ecosystem or integration, and it is the right answer when that is genuinely
the constraint rather than an assumption.

---

[← Time-series databases](../README.md)
