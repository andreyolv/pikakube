[← OLAP](../README.md)

# StarRocks

<https://github.com/StarRocks/starrocks>
<https://github.com/StarRocks/starrocks-kubernetes-operator>
<https://docs.starrocks.io/>

---

## The problem it solves

Most OLAP engines are fast because they avoid joins — you denormalise at ingest and accept a
single wide table. StarRocks does **real joins at speed**, with a cost-based optimiser, which
removes the modelling constraint that makes the others awkward.

It also reads the lakehouse directly: Iceberg, Hudi and Delta tables queried in place, without
loading them first.

| Capability | Why it matters |
|---|---|
| **Joins** | no forced denormalisation, so the model can stay normalised |
| Cost-based optimiser | query plans chosen rather than dictated by table layout |
| **Lakehouse tables** | Iceberg, Hudi and Delta, queried where they are |
| Materialised views | transparent rewriting — queries hit them without being changed |
| MySQL protocol | existing clients and BI tools connect unchanged |

The combination is unusual: warehouse-shaped SQL with sub-second latency, over both loaded
tables and the lake.

## When to use it

- **user-facing analytics that need joins** — the case [Druid](../druid/README.md) and [Pinot](../pinot/README.md) handle badly
- serving layer over an Iceberg or Delta lakehouse, without a separate load
- you want warehouse semantics and product-grade latency in one system

## When not to use it

- a single denormalised table is genuinely enough — [ClickHouse](../clickhouse/README.md) is simpler and faster at pure scans
- very high QPS point lookups on pre-aggregated data — [Pinot](../pinot/README.md)
- analysts doing ad-hoc exploration — [Trino](../../../data-engineering/query-engine/README.md) already covers that without another system

## StarRocks or Doris

They share ancestry — StarRocks forked from Apache Doris — and remain close. In practice
StarRocks tends to lead on query performance and lakehouse integration, Doris on Apache
governance and breadth of adoption.

Worth benchmarking both on your own queries rather than choosing on reputation, since the
comparison changes with each release.

---

## Notes

Open issues:

- <https://github.com/StarRocks/starrocks/issues/31130>
- <https://github.com/StarRocks/starrocks/issues/30389>

The [Kubernetes operator](https://github.com/StarRocks/starrocks-kubernetes-operator) manages
the FE and BE components, which is worth using rather than assembling StatefulSets — the
split-role architecture is where manual deployments go wrong.

---

[← OLAP](../README.md)
