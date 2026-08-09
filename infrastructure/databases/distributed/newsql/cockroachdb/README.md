[← NewSQL](../README.md)

# CockroachDB

<https://github.com/cockroachdb/cockroach>
<https://github.com/cockroachdb/helm-charts>

---

## The problem it solves

Distributed SQL with the **PostgreSQL wire protocol**, and the most polished operational
experience in [`newsql/`](../README.md).

Its distinctive feature is that survivability and data placement are **declarative**:

```sql
ALTER DATABASE app SURVIVE REGION FAILURE;
ALTER TABLE users SET LOCALITY REGIONAL BY ROW;
```

That is a statement about the topology, expressed in SQL. Elsewhere the same outcome is a
replication configuration, a placement policy and a set of assumptions.

| Capability | Detail |
|---|---|
| **PostgreSQL wire protocol** | existing drivers and most tooling connect unchanged |
| **Survival goals** | survive a node, a zone, or a region — as a database setting |
| **Geo-partitioning** | rows placed near the users who read them, by a column value |
| Symmetric nodes | every node is identical; there are no roles to assign |
| Online schema changes | non-blocking, and asynchronous |
| Automatic rebalancing | ranges split and move without intervention |

The symmetry is worth noting operationally: unlike [TiDB](../tidb/README.md), there are no
separate component types. Every node does everything, which makes the deployment considerably
simpler to reason about.

## When to use it

- a **measured** write or storage ceiling on one machine
- multi-region, where survival goals and geo-partitioning are genuinely used
- PostgreSQL wire compatibility matters, and the operational polish is worth the trade
- resilience is a first-class requirement rather than an aspiration

## When not to use it

- **the ceiling has not been measured** — a workload that fits on one machine will be *slower*
  here; see [`distributed/`](../../README.md#2-the-cost-stated-first)
- deep PostgreSQL compatibility is needed — extensions, PostGIS, specific plan behaviour.
  [YugabyteDB](../yugabytedb/README.md) reuses the actual Postgres query layer
- **single region** — you pay the design's cost and get none of its benefit
- MySQL compatibility — [TiDB](../tidb/README.md) or [Vitess](../vitess/README.md)
- the licence is a constraint — see below

## The licence

CockroachDB uses the **Cockroach Community License** — source-available, not OSI open source, and
it has been revised more than once. Recent versions moved further towards requiring a licence key
for production use, including for some previously-free tiers.

For a repository cataloguing open-source tooling this is a material difference from
[TiDB](../tidb/README.md) (Apache 2.0) and [YugabyteDB](../yugabytedb/README.md) (Apache 2.0),
and it is the kind of thing to establish before designing around it rather than at renewal.

## Wire compatibility is not behavioural compatibility

The point made in [`../README.md`](../README.md#6-anti-patterns), and it applies most often here
because the PostgreSQL protocol makes it feel like a drop-in.

What actually differs:

| Area | Detail |
|---|---|
| **Extensions** | no PostGIS, no `pg_stat_statements`, no arbitrary extensions |
| Query plans | a different optimiser, with different choices |
| **Latency** | every write is a consensus round trip |
| Some SQL surface | edge behaviours and functions differ |
| Sequences | monotonic keys are a bottleneck, so `UUID` or `unique_rowid()` |

The last row is the same warning as everywhere in this folder: a sequential primary key sends
every insert to one range, and that range's leader becomes the cluster's write bottleneck.

## Notes

Mapped with the [official Helm charts](https://github.com/cockroachdb/helm-charts).

Nothing is deployed here, and on a single Kind cluster nothing should be — a three-node consensus
group on one machine demonstrates the API and none of the properties.

Where it stands relative to the others in this folder: **the best operational experience, and the
least permissive licence.** If a distributed SQL database were adopted here on open-source terms,
[TiDB](../tidb/README.md) or [YugabyteDB](../yugabytedb/README.md) would be the candidates — and
CockroachDB's survival goals remain the clearest expression of what this category is actually for.

---

[← NewSQL](../README.md)
