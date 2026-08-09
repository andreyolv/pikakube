[← Time-series databases](../README.md)

# TimescaleDB

<https://github.com/timescale/timescaledb>
<https://github.com/timescale/helm-charts>

---

## The problem it solves

Time-series in **PostgreSQL**, as an extension — full SQL, real joins to relational data, and no
new stateful system.

A hypertable looks like an ordinary table and is partitioned by time underneath. Queries are
plain SQL; the extension adds the operations that make time-series manageable.

| Capability | What it replaces |
|---|---|
| **Hypertables** | manual partitioning by time, maintained by a cron job |
| **Continuous aggregates** | a downsampling pipeline somebody wrote and nobody maintains |
| **Compression** | 10–20× on time-series data, columnar within chunks |
| **Retention policies** | a scheduled delete script |
| `time_bucket()` | awkward date arithmetic in every query |
| Gap filling, `locf` | interpolation done in application code |

**Continuous aggregates are the feature that pays for itself.** A materialised view that
refreshes incrementally as new data arrives — per-minute rollups from per-second readings,
maintained automatically. Doing that by hand is a scheduled job, a watermark, and a class of bug
where the rollup misses late-arriving data.

## When to use it

- **PostgreSQL is already running** — which is the whole argument
- measurements are interpreted against relational data, which they almost always are
- SQL is the interface, and the existing drivers and tooling should keep working
- retention and downsampling should be table properties rather than scripts

## When not to use it

- extreme ingest rates where a purpose-built engine is measurably required —
  [QuestDB](../questdb/README.md)
- the Influx ecosystem is the requirement — Telegraf collectors, existing dashboards
- **infrastructure metrics** — wrong folder; see
  [`observability/metrics/`](../../../../observability/metrics/README.md)
- the licence for the advanced features is a constraint — see below

## The licence, which needs stating

TimescaleDB is split:

| Component | Licence |
|---|---|
| Core hypertables, `time_bucket`, basic features | **Apache 2.0** |
| Compression, continuous aggregates, some policies | **Timescale License** (source-available, free to use, restricts offering it as a service) |

The features most worth having are in the second row. Using them internally is free and
unrestricted; offering a managed TimescaleDB service is not. For a platform that is internal, this
is a non-issue — and it is exactly the kind of thing that should be established before the design
depends on it.

## Running it on Kubernetes

The practical constraint is the same one that affects [Apache AGE](../../graph/age/README.md):
**it is an extension, so it must be in the image.**

Standard PostgreSQL images do not include it. With
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md), that means either a community
image that bundles TimescaleDB or one built for the purpose — a small piece of work that is not
zero, and worth knowing before planning around it.

The alternative is Timescale's own [Helm charts](https://github.com/timescale/helm-charts),
which package PostgreSQL with the extension already present. That trades the operator's
capabilities for a simpler start.

## What to configure

| Setting | Why |
|---|---|
| **Chunk interval** | the partition size; too small means thousands of chunks, too large means poor pruning. Aim for chunks that hold roughly a week of data, or that fit in memory |
| **Compression policy** | after what age chunks are compressed — compressed chunks are far cheaper and less flexible to modify |
| Continuous aggregate refresh | how often, and over what window, so late data is included |
| Retention policy | when raw data is dropped, after the rollups exist |

The chunk interval is the one that is set once and quietly determines performance, and the
default is not always right for a given ingest rate.

## Notes

**The answer for this platform if a time-series requirement appears**, and the reason is in
[`../README.md`](../README.md#2-ask-postgresql-first--and-here-the-answer-is-often-yes):
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already runs PostgreSQL, with
backups, monitoring and an operator. A time-series capability that is an extension rather than a
new database is a materially different proposition on a single cluster.

The distinction to keep clear: this is for time-series that are **data** — usage metering, device
telemetry, price history. Metrics about the platform belong in
[`observability/metrics/`](../../../../observability/metrics/README.md), and mixing the two is the
category error described in [`../README.md`](../README.md#3-this-is-not-the-observability-folder).

---

[← Time-series databases](../README.md)
