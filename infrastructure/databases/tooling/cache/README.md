[← Tooling](../README.md)

# Query caching

Serving the same query result without running the query again — and why the hard part is not the
cache.

Tools covered: [`readyset`](readyset/README.md)

---

## The problem it solves

Most applications run a small number of queries an enormous number of times. The same product
lookup, the same permission check, the same dashboard aggregate — identical, repeatedly,
against data that changed hours ago.

The database re-executes each one from scratch. Its own buffer cache avoids the disk read, but
planning, joining and aggregating still happen every time.

The conventional answer is caching in the application with Redis: fast, well understood, and it
moves the entire problem to **invalidation** — which is application code that must know, for
every write, which cached entries are now wrong. That code is where stale data comes from.

## The two shapes

| | **Application cache** (Redis) | **Query cache** (ReadySet) |
|---|---|---|
| Lives | in application code | between the application and the database |
| Application changes | cache-aside logic everywhere | connect to a different endpoint |
| Invalidation | **your responsibility** | derived from the database's replication stream |
| Staleness | as long as your TTL, or until a bug | bounded by replication lag |
| Caches | whatever you decide to | query results, automatically |
| Failure mode | stale data served confidently | one more component in the query path |

The second row is the interesting one. A query cache speaking the PostgreSQL or MySQL wire
protocol is a drop-in: point the application at it instead of the database, and cached queries
are answered from memory.

The third row is the actual argument. ReadySet follows the replication stream and updates cached
results when the underlying rows change, so invalidation stops being a correctness problem the
application has to solve — see [`readyset/`](readyset/README.md).

## When a cache is the wrong answer

Worth asking before adding a component, because it frequently is:

| Situation | The better fix |
|---|---|
| One slow query | an index, or rewriting the query |
| Analytics on the OLTP database | a replica, or the warehouse |
| Reads saturating the primary | read replicas |
| The working set no longer fits in memory | more memory, or partitioning |
| Every query is slow | configuration — `shared_buffers`, `work_mem`, defaults assume a small machine |

A cache in front of a database with no indexes hides the problem, and at the same time makes it
harder to see: the metrics improve while the underlying query stays pathological, and the next
query pattern hits it unprotected.

The order to work through: **fix the query, then add replicas, then cache.** Reversing it is how
platforms accumulate components that cannot be removed.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Caching to avoid indexing | the underlying query stays slow, and the next pattern hits it raw | fix the query first |
| No invalidation plan | stale data served confidently, and it is a support ticket not an alert | decide invalidation before adding the cache |
| TTL as the only invalidation | correctness becomes a guess about acceptable staleness | event-driven, or a query cache that derives it |
| Caching writes-heavy data | invalidated faster than it is read, so the cache costs and returns nothing | measure the read/write ratio |
| The cache as a single point of failure | it goes down and the database receives the full load it was shielded from | verify the database survives a cold cache |
| Redis as a system of record | it is a cache, and everyone treats it as ephemeral until they do not | a durable store |

The second-to-last row is the one to test deliberately: a cache that has been absorbing 90% of
reads means the database has never seen the real load. Restarting the cache is then an
availability event, and finding that out during an incident is expensive.

## How this applies to pikakube

Nothing here is deployed, and for the current workload nothing should be.

The folder's purpose is to make the ordering explicit — **query, index, replica, cache** — and to
record that a query cache is a genuinely different tool from Redis, not a fancier one. If a cache
does become necessary against
[CloudNativePG](../../sql/postgresql/operator/cnpg/README.md), the question worth asking first
is whether the invalidation logic belongs in the application at all.

For the ephemeral-state and session use of Redis, which the platform does have, the relevant
folder is [`nosql/key-value/`](../../nosql/key-value/README.md) — a different job with a
similar-sounding name.

---

[← Tooling](../README.md)
