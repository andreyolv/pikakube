[← PostgreSQL poolers](../README.md)

# PgCat

<https://github.com/postgresml/pgcat>

Chart references: <https://artifacthub.io/packages/helm/improwised/pgcat> ·
<https://github.com/postgresml/pgcat/blob/main/charts/pgcat/values.yaml>

---

## The problem it solves

Pooling, plus the routing that [PgBouncer](../pgbouncer/README.md) deliberately does not do.

Written in Rust and multi-threaded, PgCat's argument is not speed — it is that a proxy already
sits in the path of every query, so it may as well decide **which server** the query goes to:

| Capability | Why it matters |
|---|---|
| **Read/write splitting** | writes to the primary, reads to replicas, decided by the pooler |
| **Load balancing across replicas** | with health checks, so a lagging or dead replica is taken out |
| Sharding | by key, at the proxy — a much larger commitment |
| Failover awareness | routing follows the primary when it moves |
| Multi-threaded | one process uses the machine, without running several instances |
| Mirroring | send a copy of traffic to another cluster, for testing |

**Read/write splitting is the reason to choose it.** Without a proxy, "use the replica for this
query" is a decision in application code — repeated in every service, implemented differently, and
wrong in at least one of them. Moving it to the pooler makes it configuration, and removes it from
the application entirely.

## When to use it

- **read replicas exist**, and the application should not have to know about them
- failover should not require an application change or a redeploy
- the single-threaded model of PgBouncer is a measured constraint
- traffic mirroring is genuinely useful — testing a new cluster against real load

## When not to use it

- **pooling is all that is needed** — [PgBouncer](../pgbouncer/README.md) is the boring answer, and
  boring is correct for something in the path of every query
- a database **operator** manages the deployment; CloudNativePG, StackGres and Crunchy all
  integrate PgBouncer, not this
- the ecosystem matters: fewer people have operated it, and there is less written about its failure
  modes
- sharding is being considered as a first step — see below

## The read/write splitting caveat

The feature is real and it moves a correctness problem rather than removing it.

A read sent to a replica sees **replica state**, which is behind the primary by the replication
lag. That is fine for a dashboard and wrong for read-your-own-writes: a user updates a record, the
next request is routed to a replica, and their change has not arrived.

The proxy cannot know which of those a given query is. So adopting read/write splitting means
deciding, per workload, whether stale reads are acceptable — and the queries where they are not
have to be pinned to the primary explicitly.

That decision is the actual work. The routing is configuration.

## On sharding

PgCat supports sharding, and it is worth treating as a separate decision rather than a feature you
get for free.

Sharding at the proxy brings the constraint every sharded system has: the shard key becomes part of
the data model, queries that do not specify it fan out to every shard, and cross-shard transactions
are limited. That is the same trade described in
[`distributed/newsql/`](../../../../distributed/newsql/README.md) and in
[Vitess](../../../../distributed/newsql/vitess/README.md).

If sharding is the requirement, evaluate it against those rather than adopting it as a pooler
setting.

## Notes

Two chart references were recorded — the
[Improwised chart on Artifact Hub](https://artifacthub.io/packages/helm/improwised/pgcat) and
[the project's own chart values](https://github.com/postgresml/pgcat/blob/main/charts/pgcat/values.yaml).

That the project publishes its own chart is worth noting: it is a better maintenance signal than a
third-party packaging, and the values file is where the routing configuration is actually
expressed — pools, shards, and the per-role server lists.

PgCat comes from PostgresML, which is worth knowing for context: it exists because that project
needed a pooler that could route, not as a general-purpose successor to PgBouncer.

**For this platform it is not the recommendation.**
[CloudNativePG](../../../../sql/postgresql/operator/cnpg/README.md) integrates PgBouncer through a
`Pooler` resource, and there is one PostgreSQL cluster with no read fleet to balance — so the
capability PgCat exists for has nothing to act on here.

It becomes the right answer at the point where replicas are added and the application would
otherwise need to learn about them. That is a real threshold, and it is worth knowing which tool
crosses it before the first service starts hard-coding a replica hostname.

---

[← PostgreSQL poolers](../README.md)
