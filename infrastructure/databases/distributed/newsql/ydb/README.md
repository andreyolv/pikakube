[← NewSQL](../README.md)

# YDB

<https://github.com/ydb-platform/ydb>
<https://github.com/ydb-platform/ydb-kubernetes-operator>

---

## What it is

Yandex's distributed SQL database, open-sourced under Apache 2.0 and proven at their scale —
it runs a large part of Yandex's infrastructure.

| Property | Detail |
|---|---|
| Consensus | its own, per tablet |
| **Query language** | YQL, an SQL dialect; PostgreSQL wire compatibility has been added |
| Transactions | distributed, serializable |
| **Automatic sharding** | tablets split and move without intervention |
| Serverless and dedicated modes | resource models rather than deployment types |
| Licence | **Apache 2.0** |

Architecturally it sits close to [TiDB](../tidb/README.md) and
[CockroachDB](../cockroachdb/README.md): a distributed storage layer with automatic partitioning,
and a SQL layer above it.

## When to use it

- a **measured** ceiling on one machine, and Apache licensing matters
- the operational profile and Yandex's production record are a good fit
- YQL's semantics are acceptable, or the PostgreSQL compatibility layer is sufficient

## When not to use it

- **the ceiling has not been measured** — see
  [`../README.md`](../README.md#2-the-cost-stated-first)
- close PostgreSQL compatibility matters — [YugabyteDB](../yugabytedb/README.md) reuses the
  actual Postgres query layer
- MySQL compatibility — [TiDB](../tidb/README.md) or [Vitess](../vitess/README.md)
- the ecosystem and community outside its origin are a concern — see below

## The practical position

YDB is competent, genuinely open source, and proven at scale. Its difficulty is adoption, and the
reasons are the same class as those recorded for [OceanBase](../oceanbase/README.md), in a milder
form:

| Factor | Detail |
|---|---|
| **Ecosystem** | small outside Yandex; fewer integrations, fewer tools, fewer answers |
| **Documentation** | English docs exist and are less complete than the Russian material |
| YQL | a dialect to learn, though the PostgreSQL compatibility layer reduces this |
| Community | most operational experience is concentrated in one organisation |
| Geopolitics | for some organisations, provenance is a procurement question rather than a technical one |

The last row is worth naming rather than tiptoeing around: for a number of organisations, adopting
infrastructure originating from a Russian company is a decision made outside engineering. That is
a real constraint on adoption regardless of the software's quality, and pretending otherwise makes
the catalogue less useful.

## Notes

Mapped with the
[ydb-kubernetes-operator](https://github.com/ydb-platform/ydb-kubernetes-operator).

Nothing is deployed here, and for a single Kind cluster nothing should be.

Its position in [`newsql/`](../README.md) is as a **complete alternative that most teams will not
choose** — not for technical reasons, but because
[TiDB](../tidb/README.md) and [YugabyteDB](../yugabytedb/README.md) offer comparable capabilities
with much larger ecosystems and the same Apache licence.

It is catalogued because mapping a solution space means recording the options that exist, along
with the honest reasons they are or are not adopted — and "the software is good, the ecosystem is
small" is a more useful note than silence.

---

[← NewSQL](../README.md)
