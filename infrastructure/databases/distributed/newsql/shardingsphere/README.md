[← NewSQL](../README.md)

# Apache ShardingSphere

<https://github.com/apache/shardingsphere>

---

## What it is

Sharding as a **layer**, not a database. It sits between applications and existing PostgreSQL or
MySQL instances and makes several of them look like one.

It ships in two forms, and the choice between them is the main decision:

| Form | What it is | Trade |
|---|---|---|
| **ShardingSphere-Proxy** | a database proxy speaking the MySQL and PostgreSQL protocols | language-agnostic; one more hop and a component to run |
| **ShardingSphere-JDBC** | a JDBC driver that shards client-side | **no extra hop, no extra process** — and JVM only |

The JDBC form is unusual and worth understanding: sharding happens inside the application's
driver, so there is no proxy to deploy, scale or keep available. The cost is that every client
must be a JVM application with the same configuration.

## What it provides

| Capability | Detail |
|---|---|
| **Sharding** | by rules — hash, range, or custom, per table |
| Read/write splitting | reads to replicas, writes to the primary |
| **Data encryption** | column-level, transparent to the application |
| Data masking | for non-production environments |
| Distributed transactions | XA or Seata-based, opt-in |
| Shadow database | traffic routed to a shadow for load testing |
| **Engine-agnostic** | PostgreSQL and MySQL, not just one |

The encryption and masking features are worth noting because they are unusual in this folder and
overlap [`data-governance/anonymization/`](../../../../data-governance/anonymization/README.md) —
transparent column encryption at the proxy is a real capability, not a checkbox.

## When to use it

- an existing PostgreSQL **or** MySQL estate needs sharding, as a layer rather than a migration
- a **JVM application** where the JDBC form removes the proxy entirely
- transparent column encryption or masking is a requirement alongside sharding
- Apache licensing matters

## When not to use it

- **greenfield** — a natively distributed engine is simpler than sharding rules over instances
- MySQL specifically, at serious scale — [Vitess](../vitess/README.md) is more mature at exactly
  that job, with online resharding
- the sharding rules would live only in configuration nobody documents
- cross-shard queries and transactions are common — the constraints in
  [`vitess/`](../vitess/README.md#the-constraint-the-sharding-key) apply here too

## ShardingSphere or Vitess

Both put a layer in front of real databases. They differ in focus:

| | ShardingSphere | [Vitess](../vitess/README.md) |
|---|---|---|
| Engines | **PostgreSQL and MySQL** | MySQL only |
| Deployment | proxy **or** JDBC driver | proxy plus per-instance agents |
| **Online resharding** | more limited | **a core strength** |
| Extras | encryption, masking, shadow DB | topology and lifecycle management |
| Maturity at scale | good | **proven at YouTube scale** |
| Operational model | a layer you configure | a system that manages MySQL for you |

**Vitess for MySQL at scale. ShardingSphere when PostgreSQL is involved, or when the JDBC form's
absence of a proxy is the deciding factor.**

## Notes

Nothing here is deployed, and the prior question in
[`../README.md`](../README.md#4-decision-tree) applies with full force: sharding is what you reach
for after a **measured** ceiling, and read replicas plus connection pooling solve most of what
people reach for it to fix.

Its position in this folder is as the **engine-agnostic** option — the only entry that answers
"we need to shard, and it is PostgreSQL". For that case there is no equivalent to Vitess, which
is worth knowing before assuming the MySQL playbook transfers.

---

[← NewSQL](../README.md)
