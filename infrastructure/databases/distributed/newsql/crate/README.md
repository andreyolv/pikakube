[← NewSQL](../README.md)

# CrateDB

<https://github.com/crate/crate>
<https://github.com/crate/crate-operator>

---

## What it is

Distributed SQL over **semi-structured and time-series data**, with full-text search built in. It
speaks the PostgreSQL wire protocol and is built on Lucene underneath.

That combination places it slightly apart from the rest of
[`newsql/`](../README.md): the others are distributed OLTP databases, and CrateDB is aimed at
high-volume ingest with analytical and search queries over it.

| Capability | Detail |
|---|---|
| **PostgreSQL wire protocol** | existing drivers and BI tools connect |
| **Full-text search** | Lucene-based, so it is real search rather than `LIKE` |
| Dynamic objects | nested JSON columns, queryable and indexable per path |
| **Time-series** | partitioning by time, with sharding |
| Columnar storage | for aggregation performance |
| Horizontal scale | shards and replicas across nodes |

Where it fits best is IoT and machine data: high ingest, semi-structured payloads, and queries
that mix aggregation with search.

## When to use it

- **high-volume ingest** of semi-structured or time-series data, queried in SQL
- search and analytics over the same dataset, without a separate search cluster
- the schema varies and should still be queryable per field
- horizontal scale for reads and ingest

## When not to use it

- **transactional workloads** — this is not the OLTP answer; no cross-row transactions in the
  sense [CockroachDB](../cockroachdb/README.md) or [YugabyteDB](../yugabytedb/README.md) provide
- time-series where PostgreSQL is already running —
  [TimescaleDB](../../../nosql/timeseries/timescaledb/README.md) adds no new system
- pure analytics — [`data-streaming/olap/`](../../../../data-streaming/olap/README.md) has
  ClickHouse and StarRocks for exactly that
- the licence matters — CrateDB is split between an Apache-licensed core and an enterprise edition

## The consistency caveat

Worth stating clearly, because the PostgreSQL protocol implies more than is delivered.

CrateDB provides **eventual consistency for reads** and does not offer multi-row ACID transactions
the way the other NewSQL entries do. It is closer in model to Elasticsearch — which its Lucene
foundation explains — than to a distributed OLTP database.

That is appropriate for its target workload and it is the thing most likely to surprise someone
who read "PostgreSQL wire protocol" and assumed PostgreSQL semantics. The warning in
[`../README.md`](../README.md#6-anti-patterns) — *wire compatibility is not behavioural
compatibility* — applies here more sharply than anywhere else in the folder.

## Notes

Recorded from actually deploying it:

```bash
k port-forward svc/crate-discovery-pikakube 4200
```

> When a database is created through the CRD, a `LoadBalancer` service is created automatically,
> and there appears to be no configuration option to disable it.

That is a real operational annoyance and worth taking seriously in this environment. On a
[Kind](../../../../../clusters/kind-configs/) cluster a `LoadBalancer` service stays `Pending`
unless something provides an address —
[MetalLB](../../../../network/load-balancer/metallb/README.md) here — and on a cloud provider it
would silently provision a real load balancer, with a real cost, for a database that may not have
been meant to be publicly reachable.

An operator that creates a `LoadBalancer` with no opt-out is the kind of default that is
harmless in a demo and expensive in an account with a billing alert. The workaround in this
environment is the port-forward above.

Nothing is deployed here. CrateDB is catalogued as the entry in
[`newsql/`](../README.md) that is **not really an OLTP database** — which is useful to know
before it is evaluated on that basis.

---

[← NewSQL](../README.md)
