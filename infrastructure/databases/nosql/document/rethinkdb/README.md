[← Document stores](../README.md)

# RethinkDB

<https://github.com/rethinkdb/rethinkdb>

---

## The idea it introduced

**Changefeeds** — a query you subscribe to, which pushes results to the client as the underlying
data changes:

```javascript
r.table('orders').filter({status: 'pending'}).changes()
```

That subscription stays open, and every insert, update or delete matching the filter arrives at
the client. In 2015 that was genuinely novel: the alternative was polling, or building a
change-propagation layer by hand.

It is the reason RethinkDB is remembered, and the idea outlived the database.

## The state of the project

Worth stating first, because it decides everything else.

The company behind it shut down in 2016. The code was open-sourced under the Linux Foundation and
is maintained by a small community, but development is effectively **dormant** — occasional
maintenance, no meaningful roadmap.

That makes it a poor choice for anything new, regardless of technical merit. A database is a
long-term dependency, and this one has no momentum, limited security-update cadence, and a
shrinking pool of people who know it.

## Where the idea went

Changefeeds are now available in systems that are actively developed, which is the practical
takeaway:

| Where | How |
|---|---|
| **MongoDB** | change streams — the same capability, in a maintained database |
| **PostgreSQL** | `LISTEN`/`NOTIFY` for simple cases; logical replication and [Debezium](../../../../data-streaming/README.md) for real CDC |
| [CouchDB](../couchdb/README.md) | the changes feed, plus replication |
| **Materialised views over streams** | [RisingWave](../../../../data-streaming/processing/risingwave/README.md) — a query you subscribe to, at stream scale |

The last row is the interesting one for a data platform. RisingWave's model — define a query,
have its results maintained incrementally and readable over the PostgreSQL protocol — is
RethinkDB's idea, rebuilt for streaming volumes with a real project behind it.

## When to use it

Honestly: not for new work. The realistic cases are an existing deployment being maintained, or
studying the changefeed model.

## When not to use it

- **anything new** — the project is dormant
- production dependence on a database with no active development
- a reactive-updates requirement, which now has maintained answers

## Notes

Mapped for completeness and as a reference point rather than a candidate. It belongs in this
catalogue for the same reason [Amundsen](../../../../data-governance/catalog/amundsen/README.md)
and [Apache Atlas](../../../../data-governance/catalog/atlas/README.md) do: knowing which
projects are dead is part of mapping a solution space, and it prevents someone re-evaluating them
from a search result.

The idea is the part worth keeping. If a requirement here ever reads *"the application should be
notified when matching rows change"*, the answer is MongoDB change streams, Postgres logical
replication, or a materialised view over a stream — not this.

---

[← Document stores](../README.md)
