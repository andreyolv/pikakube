[← Analytical databases](../README.md)

# ByConity

<https://github.com/ByConity/ByConity>
<https://github.com/ByConity/byconity-deploy>

---

## What it is

ByteDance's fork of [ClickHouse](../../../data-streaming/olap/clickhouse/README.md), rearchitected
to **separate storage from compute**.

ClickHouse attaches storage to nodes: scaling means adding nodes and rebalancing, and workloads
share the same resources. ByConity keeps data in object storage and makes compute stateless, so
different workloads get isolated compute over the same data.

| Property | Detail |
|---|---|
| **Storage/compute separation** | data in object storage, compute elastic |
| **Workload isolation** | separate virtual warehouses for ETL and for queries |
| ClickHouse compatibility | much of the SQL and the ecosystem carry over |
| Scale | proven inside ByteDance |
| Dependency | **[FoundationDB](../../distributed/key-value/foundationdb/README.md)** for metadata |

The FoundationDB dependency is the distinctive architectural choice, and it is also the practical
obstacle — see the notes.

## When to use it

- ClickHouse's engine with **elastic, isolated compute**
- heavy ETL and interactive queries competing for the same cluster today
- object storage is the platform's foundation
- ByteDance-scale workloads, where its production record is relevant

## When not to use it

- **plain ClickHouse would do** — which for most workloads it would, with far less to operate
- the operational surface is a concern: this is ClickHouse plus FoundationDB plus a compute layer
- the community outside ByteDance is small
- the deployment story matters — see below

## The honest assessment

The architecture is sound and the operational cost is high.

ClickHouse is already a substantial system to run well. ByConity adds a distributed transactional
key-value store as a hard dependency, plus a compute-management layer, in exchange for elasticity
and workload isolation.

That trade is right at ByteDance's scale. At most other scales, the question in
[`../README.md`](../README.md) applies: would plain ClickHouse, or a lakehouse with a query
engine, solve this with less?

## Notes

Recorded from actually attempting to deploy it:

> ```
> no matches for kind "FoundationDBCluster" in version "apps.foundationdb.org/v1beta2"
> ```
>
> Setting `fdb-operator.enabled: true` in the values should bring up the FoundationDB operator
> **with its CRDs**, and it does not. The operator has to be installed first, separately, with that
> value left off — which was not done here, because the project is rough enough not to justify it.

That is a fair verdict and the failure is worth understanding, because the pattern recurs.

**A Helm value that enables a sub-chart does not reliably install that sub-chart's CRDs.** Helm
applies CRDs in a separate phase, and a dependency's CRDs frequently do not arrive before the
resources that reference them. The standard workaround is to install the operator and its CRDs
first, explicitly, and disable the bundled one.

The same problem appears in this repository with
[TiDB](../../distributed/newsql/tidb/README.md), where the CRDs are installed from a sliced
manifest before the operator — see that page for the technique.

The wider signal is worth reading too: a project whose primary deployment path fails on its own
declared dependency is telling you something about how many people have deployed it. For a
component that would hold the platform's analytical data, that matters more than the architecture
diagram.

Nothing is deployed. ByConity is catalogued as the storage/compute-separated ClickHouse, alongside
[Databend](../databend/README.md), which pursues the same idea with a considerably simpler
dependency graph.

---

[← Analytical databases](../README.md)
