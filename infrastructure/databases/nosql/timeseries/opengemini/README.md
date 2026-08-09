[← Time-series databases](../README.md)

# openGemini

<https://github.com/openGemini/openGemini>
<https://github.com/openGemini/openGemini-operator>

---

## What it is

An open-source, **distributed** time-series database that is compatible with InfluxDB — the line
protocol for writes, and InfluxQL for queries.

It originated at Huawei and is now a CNCF sandbox project, written in Go.

Its position in this folder is specific: it answers the gap left by
[InfluxDB](../influxdb/README.md), where clustering belongs to the commercial edition.

| | InfluxDB OSS | openGemini |
|---|---|---|
| Clustering | **not in the open-source edition** | **yes** |
| Licence | MIT (OSS edition), commercial for clustering | **Apache 2.0** |
| Write protocol | line protocol | **compatible** |
| Query | InfluxQL / Flux / SQL, by version | InfluxQL |
| Ecosystem | **very large** | small |
| Governance | InfluxData | CNCF sandbox |

## When to use it

- InfluxDB compatibility **and** clustering **and** an open licence — the combination is the
  reason it exists
- an existing Influx line-protocol writer, such as Telegraf, should keep working
- horizontal scale is required and paying for InfluxDB Enterprise is not the plan

## When not to use it

- **PostgreSQL is already running** — [TimescaleDB](../timescaledb/README.md) adds no new system
  and gives full SQL
- the InfluxDB ecosystem beyond the write protocol matters — tooling, integrations and community
  answers are InfluxData's, not this project's
- ingest throughput on one node is the constraint — [QuestDB](../questdb/README.md)
- production dependence on a smaller project is a concern

## The honest assessment

The technical proposition is coherent and the adoption risk is the ecosystem.

Compatibility at the protocol level means writers work. It does not mean the surrounding
InfluxData ecosystem — dashboards, tooling, integrations, and the accumulated answers to
operational questions — transfers with it. A problem encountered at 2am with openGemini has a
much smaller body of prior art behind it than the same problem with InfluxDB.

CNCF sandbox status is a positive signal about governance and a neutral one about maturity —
sandbox is the entry stage, not an endorsement of production readiness.

## Notes

Mapped with the [openGemini-operator](https://github.com/openGemini/openGemini-operator).

For this platform it is not the recommendation, for the same reason as
[InfluxDB](../influxdb/README.md): the requirement does not exist, and if it did,
[TimescaleDB](../timescaledb/README.md) answers it inside the PostgreSQL that
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already operates.

It is catalogued because it occupies a real gap — Influx-compatible, distributed, Apache-licensed
— and that combination is otherwise unavailable. If an Influx-shaped requirement ever appears here
alongside a licensing or clustering constraint, this is where the answer is.

---

[← Time-series databases](../README.md)
