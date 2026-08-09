[← Data Streaming](../README.md)

# Migration

Moving between brokers without losing events.

---

## Why this is hard

A broker is not a stateless service. Migrating one means moving:

| What | Why it is difficult |
|---|---|
| **Topic data** | possibly terabytes, and it keeps arriving during the move |
| **Consumer offsets** | the position each consumer group holds — get this wrong and you replay or skip |
| **Topic configuration** | partitions, retention, compaction, ACLs |
| **Producers and consumers** | every client has to repoint, and they do not all deploy together |

The offsets are the part that catches people. Copying messages is straightforward; translating
a consumer group's position from the source cluster to the target — where the same message may
have a different offset — is not.

## The approaches

| Approach | How | Trade |
|---|---|---|
| **Mirror** | replicate topics continuously into the new cluster, then cut clients over | consumers must handle offset translation at the cut |
| **Dual write** | producers write to both for a period | application change, and a window where the two can diverge |
| **Drain** | stop producing, let consumers finish, then move | requires downtime, and is by far the simplest |
| **Replay from source** | reproduce from the original systems rather than the broker | only possible when the true source still holds the data |

The drain is underrated. If a maintenance window is available, it removes the offset problem
entirely — and offset translation is where migrations go wrong.

## MirrorMaker 2

The standard tool, part of Kafka. It replicates topics, configuration and consumer group
offsets between clusters, using Kafka Connect underneath.

What to know before relying on it:

- topics are **renamed with a cluster prefix** by default, which changes what consumers subscribe to
- **offset translation is approximate**, because offsets are per-cluster
- it replicates continuously, so the cut is a client change rather than a data move
- it also supports active/active geo-replication, which is a different use case from migration

Redpanda's take on the same problem, with connector-based migration:
<https://www.redpanda.com/blog/kafka-migrator-redpanda-connect>

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Migrating without testing offset translation | consumers replay or skip messages, silently | verify with a non-critical consumer group first |
| Cutting all clients at once | no way back if something is wrong | move one consumer group at a time |
| Ignoring the topic prefix | consumers subscribe to a topic that does not exist under that name | plan the naming before starting |
| Assuming exactly-once survives the migration | duplicates around the cut are the normal case | idempotent consumers |
| No rollback plan | the old cluster is decommissioned too early | keep the source running until the new one is proven |

## Related

- Brokers and their trade-offs: [`event-streaming/`](../event-streaming/README.md)
- Moving persistent volumes rather than topics: [`pv-migrate`](../../site-reliability-engineering/backup/pv-migrate/README.md)

---

[← Data Streaming](../README.md)
