[← Time-series databases](../README.md)

# InfluxDB

<https://github.com/influxdata/influxdb>
<https://github.com/influxdata/helm-charts>

---

## What it is

The best-known dedicated time-series database, and the centre of a large IoT and monitoring
ecosystem — **Telegraf** in particular, which collects from several hundred sources and writes
the line protocol.

That ecosystem is the main reason to choose it. The database itself is good; the collectors,
integrations and existing dashboards are what is hard to replicate.

## The version question, which comes first

InfluxDB has changed direction twice, and the generations are not compatible. This is the single
most important thing to establish before adopting it:

| Version | Storage | Query language | Position |
|---|---|---|---|
| **1.x** | TSM | InfluxQL (SQL-like) | still widely deployed; simple, familiar |
| **2.x** | TSM | **Flux** — a new functional language | the generation that lost people |
| **3.x** | **Parquet, object storage** | **SQL**, plus InfluxQL | a rewrite in Rust; SQL restored |

The consequences are practical rather than theoretical:

- documentation, tutorials and Stack Overflow answers are split across three generations, often
  without saying which
- client libraries differ per version
- **Flux** was introduced in 2.x and is being de-emphasised in 3.x, so material written for it has
  a limited shelf life
- 3.x's open-source edition has different capabilities from the commercial one — clustering in
  particular

**Pin the version deliberately** and read documentation that matches it. Not doing so is the most
common source of wasted time with this database.

## When to use it

- **the Telegraf ecosystem** is the requirement — hundreds of input plugins, already written
- IoT, where Influx's line protocol and collectors are the established path
- existing InfluxDB dashboards and queries to preserve
- a dedicated engine is genuinely wanted, rather than an extension

## When not to use it

- **PostgreSQL is already running** — [TimescaleDB](../timescaledb/README.md) gives time-series
  with full SQL and joins, and no new system
- raw ingest throughput is the constraint — [QuestDB](../questdb/README.md)
- **infrastructure metrics** — wrong folder; see
  [`observability/metrics/`](../../../../observability/metrics/README.md), where Prometheus and
  VictoriaMetrics are built for that job
- the version churn is unattractive, which is a legitimate position

## The cardinality trap

The classic failure with InfluxDB, and it deserves naming because it arrives suddenly.

A **series** is a unique combination of measurement and tag values. Adding a tag with high
cardinality — a request ID, a user ID, a container ID — multiplies the series count, and memory
usage follows it. In 1.x and 2.x this is the well-documented cause of instances that become
unstable without warning.

The rule: **tags are for values you filter and group by, with bounded cardinality.** Anything
unbounded belongs in a field, which is not indexed.

3.x's Parquet-based storage handles high cardinality far better, which is one of the strongest
arguments for the rewrite — and it does not retroactively fix a schema designed for 1.x.

## Notes

Mapped with the [official Helm charts](https://github.com/influxdata/helm-charts).

For this platform it is not the recommendation, and the reason is
[`../README.md`](../README.md#2-ask-postgresql-first--and-here-the-answer-is-often-yes):
[TimescaleDB](../timescaledb/README.md) provides time-series inside the PostgreSQL that
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already operates, with joins to
the relational data that gives measurements meaning.

Where InfluxDB would win is the ecosystem — if Telegraf's collectors are the actual requirement,
that is a real argument and nothing in the Postgres world matches it.

The open-source alternative in the same ecosystem: [openGemini](../opengemini/README.md), which is
InfluxDB-compatible and distributed.

---

[← Time-series databases](../README.md)
