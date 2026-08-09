[← OLAP](../README.md)

# Apache Doris

<https://github.com/apache/doris>
<https://github.com/apache/doris-operator>
<https://doris.apache.org/>

Examples: <https://github.com/apache/doris-operator/tree/master/doc/examples>

---

## What it is

An MPP analytical database with the **MySQL protocol** as its interface — so existing clients,
drivers and BI tools connect without changes.

Its positioning is unified serving: real-time ingestion and batch loading into the same tables,
with joins, materialised views and a cost-based optimiser.

| Capability | Detail |
|---|---|
| MySQL protocol | no new drivers, no new client tooling |
| **Real-time and batch** | streaming ingest and bulk load into the same table |
| Joins | properly supported, unlike the time-series-oriented engines |
| Materialised views | transparent query rewriting |
| Lakehouse | external tables over Hive, Iceberg and Hudi |
| Apache governance | which is the usual reason to prefer it over StarRocks |

## When to use it

- **Apache governance** matters for the choice
- the MySQL protocol removes real friction — existing tools connect immediately
- unified real-time and batch serving in one system

## When not to use it

- raw scan performance over one wide table — [ClickHouse](../clickhouse/README.md) is faster at that
- very high QPS on pre-modelled data — [Pinot](../pinot/README.md)
- ad-hoc analyst queries over the lake — [Trino](../../../data-engineering/query-engine/README.md)

## Doris or StarRocks

StarRocks forked from Doris, and both have developed substantially since. They are close enough
that the decision is usually made on:

| Factor | Leans |
|---|---|
| Governance | **Doris** — Apache, community-led |
| Query performance | **StarRocks**, generally, though it changes per release |
| Lakehouse integration | **StarRocks** has pushed harder here |
| Vendor independence | **Doris** |

The honest advice is to benchmark both on real queries. Published comparisons come from one
side or the other, and the gap moves.

## Deployment

The [operator](https://github.com/apache/doris-operator) manages the FE (frontend, metadata and
planning) and BE (backend, storage and execution) roles. That split is where hand-rolled
deployments break, which is the argument for using it.

---

[← OLAP](../README.md)
