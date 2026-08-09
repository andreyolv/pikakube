[← Integration](../README.md)

# PeerDB

<https://github.com/PeerDB-io/peerdb>

---

## The problem it solves

Generic connectors treat PostgreSQL as one source among hundreds. PeerDB treats it as **the**
source, and specialises accordingly.

The difference shows in the mechanism: it uses **logical replication** rather than polling a
cursor. That means changes arrive as they happen, deletes are captured, and the source is not
repeatedly queried for "what changed since".

| Property | Generic connector | PeerDB |
|---|---|---|
| Mechanism | query with a cursor | logical replication slot |
| Deletes | usually missed | captured |
| Latency | the sync interval | seconds |
| Load on the source | a query per sync | the replication stream |

## When to use it

- **PostgreSQL** is the source and it matters — volume, latency, or both
- deletes must be captured, which cursor-based connectors generally miss
- replicating Postgres into a warehouse or lakehouse continuously

## When not to use it

- sources are heterogeneous — [Airbyte](../airbyte/README.md) covers breadth, this covers depth
- the requirement is a daily batch of a small table, where a generic connector is simpler
- you already run [Debezium](../../../data-streaming/README.md) for CDC into Kafka; that is the same mechanism in a streaming shape

## The prerequisite

Logical replication has to be **enabled on the source**, with `wal_level = logical`, a
replication slot, and the permissions to create one. On a managed Postgres that is a provider
setting, and on a production database it is a change someone has to approve.

Worth establishing before planning around it — an unconsumed replication slot also retains WAL
indefinitely, which fills the source's disk. That is the failure mode to know about.

---

## Notes

> The chart documentation is poor.

Expect to read the manifests rather than the docs when deploying it.

---

[← Integration](../README.md)
