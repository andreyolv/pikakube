[← Databases](../README.md)

# Tooling

The parts that decide whether a database survives contact with production.

Subfolders: [`migration/`](migration/README.md) · [`pooler/`](pooler/README.md) ·
[`monitoring/`](monitoring/README.md) · [`management/`](management/README.md) ·
[`cache/`](cache/README.md) · [`documentation/`](documentation/README.md) ·
[`orm/`](orm/README.md)

---

## Why this folder matters more than the engine choice

Choosing PostgreSQL over MySQL rarely decides whether a platform works. These do:

| Without it | What happens |
|---|---|
| **Migrations** | environments diverge, and production cannot be reproduced |
| **Connection pooling** | connection exhaustion under load, with CPU graphs that explain nothing |
| **Monitoring** | the first sign of a problem is a user complaint |
| **Management access** | either nobody can inspect the database, or everybody has production credentials |

Every one of these is discovered late, usually during an incident, and each is cheap to put in
place beforehand.

## The map

| Folder | The question it answers | Why it bites |
|---|---|---|
| [`migration/`](migration/README.md) | how does the schema change, reproducibly? | manual `ALTER` statements make environments diverge permanently |
| [`pooler/`](pooler/README.md) | how do thousands of clients share a few hundred connections? | Postgres runs out of connections long before capacity |
| [`monitoring/`](monitoring/README.md) | what is it doing, and what is about to break? | connection exhaustion and replication lag are invisible until they are not |
| [`management/`](management/README.md) | how do people inspect and query it safely? | the alternative is shared production credentials |
| [`cache/`](cache/README.md) | how are repeated queries served without re-running them? | the same query, thousands of times, unchanged |
| [`documentation/`](documentation/README.md) | what does this schema actually contain? | inherited databases nobody can explain |
| [`orm/`](orm/README.md) | how does application code talk to it? | hand-written SQL everywhere, or an ORM generating queries nobody reviews |

## The two that are not optional

**Connection pooling.** PostgreSQL allocates a process per connection. A few hundred is a real
ceiling, and application frameworks open connections generously. Without a pooler, the failure
looks like the database being slow when it is idle — see [`pooler/`](pooler/README.md).

**Migrations.** A schema changed by hand exists in exactly one environment. Every other
environment drifts, and reproducing production becomes archaeology. This is the single
highest-value thing in the folder — see [`migration/`](migration/README.md).

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Schema changes applied by hand | environments diverge and production is not reproducible | a migration tool, in CI |
| No connection pooler | exhaustion under load, with misleading symptoms | PgBouncer or PgCat |
| Monitoring only CPU and memory | connections and replication lag are the ones that page you | database-specific metrics |
| A management UI open to everyone | it is production access with a friendlier interface | scoped credentials, SSO, read-only by default |
| Caching without an invalidation plan | stale data served confidently | decide invalidation before adding the cache |
| An ORM generating unreviewed queries | N+1 queries and full scans in production | inspect what it emits |

## How this applies to pikakube

**Monitoring** is the part with real history — [pghero](monitoring/pghero/README.md),
[PMM](monitoring/pmm/README.md) and the
[postgres-exporter](../../observability/metrics/exporters/postgres-exporter/README.md), which carries the
honest note that the community dashboards for it are mostly poor.

**Migration** is documented as a process for PostgreSQL on Kubernetes; the tools in
[`migration/`](migration/README.md) are the alternatives to doing it by hand.

The gap worth naming: with [CloudNativePG](../sql/postgresql/operator/cnpg/README.md) deployed,
**pooling** is the piece that decides behaviour under load, and it is easy to leave until the
first incident.

---

[← Databases](../README.md)
