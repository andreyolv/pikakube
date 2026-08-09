[← Document stores](../README.md)

# CouchDB

<https://github.com/apache/couchdb>
<https://github.com/apache/couchdb-helm>

---

## The problem it solves

Not "a document store" — there are better ones for that. CouchDB's distinctive capability is
**replication between partially connected nodes**, including browsers and mobile devices.

It is multi-master by design: every replica accepts writes, and replication reconciles them
afterwards. That is what makes offline-first possible.

| Property | Why it is unusual |
|---|---|
| **Bidirectional replication** | between any two CouchDB instances, in either direction, resumable |
| **Offline-first** | PouchDB in a browser replicates with a server when connectivity returns |
| Multi-master | every node accepts writes; there is no primary |
| **HTTP as the API** | every operation is a REST call, so `curl` is a client |
| MVCC with revisions | every document carries a revision; conflicts are surfaced, not hidden |
| Crash-only design | it is designed to be killed, not shut down |

The offline-first case is the one nothing else in [`document/`](../README.md) answers. A field
application that works without connectivity and reconciles later is CouchDB's shape, and building
it on MongoDB means writing the synchronisation layer yourself.

## When to use it

- **offline-first applications** — mobile, field work, intermittently connected sites
- data must be replicated between sites with no reliable link
- an HTTP-only interface is an advantage — no driver, no connection pool
- multi-master writes are the requirement rather than a risk

## When not to use it

- a general-purpose document store — [MongoDB](../mongo/README.md) has the ecosystem, or
  PostgreSQL `JSONB` has the transactions
- complex queries and aggregation; the views model is deliberately limited
- write throughput at scale — the HTTP-per-operation model has a cost
- conflicts are unacceptable rather than expected

## Conflicts are the application's problem

This is the trade, and it must be understood before adopting it.

Multi-master means two replicas can modify the same document while disconnected. CouchDB does not
lose either version: it stores both, picks a deterministic winner, and marks the document as
conflicted.

**Deciding what the correct value is remains the application's job.** That is honest — it is the
only correct behaviour for a system that allows concurrent writes without coordination — and it
means "handle conflicts" is a feature to be built, not a setting to be enabled.

Applications that ignore this appear to work until the first real network partition, at which
point data silently reflects the deterministic winner rather than the intended one.

## Views, and what queries look like

Queries are **MapReduce views** written in JavaScript and materialised into indexes, plus Mango,
a declarative query API resembling MongoDB's.

Views are fast to read and must be defined in advance. Ad-hoc querying is not the model, and a
new access pattern usually means a new view and an index build.

## Notes

Mapped with the [official Helm chart](https://github.com/apache/couchdb-helm), which is one of
the better-maintained ones in this catalogue — a genuine advantage over several tools in
[`data-governance/`](../../../../data-governance/README.md) where the chart is the obstacle.

For this platform there is no offline-first requirement, which is the only reason to prefer
CouchDB over the alternatives in this folder. It is catalogued so that when the question *"how do
we sync data to intermittently connected sites?"* appears, the answer is a folder rather than a
research task — and so that MongoDB is not adopted for a problem it does not solve.

---

[← Document stores](../README.md)
