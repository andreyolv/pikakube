[← Query caching](../README.md)

# ReadySet

<https://github.com/readysettech/readyset>

---

## The problem it solves

A cache that **invalidates itself**.

The conventional answer to repeated identical queries is caching in the application with Redis:
fast, well understood, and it moves the whole problem to invalidation — application code that must
know, for every write, which cached entries are now wrong. That code is where stale data comes
from.

ReadySet sits between the application and the database, speaks the **PostgreSQL and MySQL wire
protocols**, and follows the database's replication stream. When a row changes, the cached results
that depend on it are updated.

| | Redis, cache-aside | ReadySet |
|---|---|---|
| Application changes | cache logic at every call site | **connect to a different endpoint** |
| Invalidation | **your responsibility** | derived from replication |
| Staleness | until the TTL, or until a bug | bounded by replication lag |
| What is cached | whatever you decide | query results, declared per query |
| Cache misses | fall through to the database | the same |

## How it works

It is a **partially-materialised dataflow** system. A cached query is compiled into a dataflow
graph; the replication stream feeds updates through that graph, and the results are maintained
incrementally rather than recomputed.

That is the same lineage as [RisingWave](../../../../data-streaming/processing/risingwave/README.md)
and Materialize — incremental view maintenance — applied to caching an OLTP database rather than
to stream processing.

Caching is opt-in per query:

```sql
CREATE CACHE FROM SELECT * FROM products WHERE category_id = ?;
```

Uncached queries pass straight through to the upstream database, so adopting it does not require
routing everything through it at once.

## When to use it

- **the same queries, constantly**, against data that changes far less often
- invalidation logic in the application has already caused stale-data incidents
- the application should not be rewritten to add caching
- read load on the primary is the constraint, and replicas have not solved it

## When not to use it

- **the query is slow because it lacks an index** — fix that first; see
  [`../README.md`](../README.md#when-a-cache-is-the-wrong-answer)
- write-heavy data, invalidated faster than it is read
- another component in the query path is unwelcome
- the project's maturity is a concern for something this central

## What to check before adopting it

| Concern | Detail |
|---|---|
| **Supported queries** | not every query shape can be cached; complex ones fall back |
| **Replication setup** | it needs logical replication configured on the upstream |
| Memory | cached results live in memory, and that is the sizing constraint |
| **In the query path** | it is a component every request passes through |
| Licence | check the current terms; this has moved for comparable projects |
| Cold start | after a restart, the caches rebuild from the upstream |

The fourth row is the one to weigh honestly. A cache that improves the median latency also becomes
something that can fail — and a database that has been serving 10% of its real read load has never
been tested at 100%. See
[`../README.md`](../README.md#anti-patterns), the single-point-of-failure row.

## Notes

Mapped as the query-cache option, and it is the entry that makes the distinction in
[`../README.md`](../README.md#the-two-shapes) concrete: this is a genuinely different tool from
Redis, not a fancier one.

For this platform nothing here is deployed and the ordering in that folder applies —
**query, index, replica, cache.** With
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) running PostgreSQL and no
measured read-load problem, a cache would be solving a problem that has not appeared.

The idea worth carrying forward regardless: if caching ever does become necessary, the first
question is whether the invalidation logic belongs in the application at all — and ReadySet is
the argument that it does not.

---

[← Query caching](../README.md)
