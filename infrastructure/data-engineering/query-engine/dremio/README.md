[← Query engine](../README.md)

# Dremio

<https://github.com/dremio/dremio-oss>
<https://github.com/dremio/dremio-cloud-tools>
<https://docs.dremio.com/>

---

## What it is

A lakehouse query **platform** rather than an engine — Trino-like federation, plus the pieces
that usually have to be assembled around it:

| Capability | What it replaces |
|---|---|
| Federated SQL | a query engine |
| **Reflections** | materialised views the optimiser uses automatically, without the query being rewritten |
| Semantic layer | virtual datasets with governed definitions — see [`semantic/`](../../../analytics-engineering/semantic/README.md) |
| Catalogue and lineage | part of what [`data-governance/`](../../../data-governance/README.md) covers |
| UI | self-service exploration for analysts |

**Reflections are the distinguishing feature.** They are transparent materialisations: define
one, and queries that could use it are rewritten to hit it. Users do not know it exists — they
just see a query return in two seconds instead of forty.

That is a genuinely different model from caching, and it is the main technical reason to
consider it.

## When to use it

- you want a **product** rather than assembling engine, semantic layer and catalogue separately
- query acceleration should be automatic rather than modelled by hand
- analysts need self-service over a lakehouse without a warehouse

## When not to use it

- you prefer composable, replaceable components — [Trino](../trino-gateway/README.md) plus [dbt](../../../analytics-engineering/transform/dbt/README.md) plus a [catalogue](../../../data-governance/README.md)
- fully open source is a requirement; the OSS edition is genuinely usable but the product line is commercial
- Trino is already deployed and working

## The trade

Fewer moving parts, in exchange for a platform decision rather than a set of independent ones.

Coming from Trino, the things that would change: the semantic layer moves into Dremio, the
acceleration strategy becomes reflections rather than modelled aggregates, and the catalogue
question is partly answered for you.

Whether that is simplification or lock-in depends on how much of it you would otherwise build —
which is exactly the same question as [`observability/platforms/`](../../../observability/platforms/README.md),
in a different domain.

---

[← Query engine](../README.md)
