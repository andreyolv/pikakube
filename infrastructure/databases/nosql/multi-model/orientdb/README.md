[← Multi-model databases](../README.md)

# OrientDB

<https://github.com/orientechnologies/orientdb>

---

## What it was

One of the first multi-model databases: documents, graphs and object storage in one engine, with
SQL-like syntax extended for traversal, and ACID transactions across all of it.

That was genuinely ahead of its time. When it appeared, the choice was a document store *or* a
graph database, and OrientDB argued the split was unnecessary — an argument
[ArangoDB](../arangodb/README.md) now makes with a maintained project behind it.

## The state of the project

This decides the entry, so it comes first.

OrientDB was acquired by SAP in 2017. Development slowed markedly afterwards and the project is
now **effectively dormant** — sporadic maintenance, no meaningful roadmap, and a community that
has largely moved on.

For a database, that is disqualifying regardless of technical merit. A database is among the
longest-lived dependencies a system takes on: it needs security updates, version compatibility as
the runtime moves, and people who can answer questions when it misbehaves at 2am.

## When to use it

Honestly: an existing OrientDB deployment being maintained, and nothing else.

## When not to use it

- **anything new** — [ArangoDB](../arangodb/README.md) is the maintained answer in this category
- production dependence on a project without active development
- and the prior question still applies: multi-model is often a way to avoid deciding — see
  [`../README.md`](../README.md#the-counter-argument)

## Why it is still in the catalogue

For the same reason [RethinkDB](../../document/rethinkdb/README.md) and
[KeyDB](../../key-value/keydb/README.md) are, and it is a deliberate part of how this repository
is meant to work.

Mapping a solution space includes recording which options are **dead**. Without that, someone
evaluating multi-model databases finds OrientDB in a search result, reads a feature list written
in 2016, and spends a week discovering what a single line here could have told them.

The pattern across all three: a good idea, an early implementation, an acquisition, and a project
that stopped. The idea usually survives somewhere maintained — changefeeds in MongoDB change
streams, multithreaded Redis in DragonflyDB, multi-model in ArangoDB.

## Notes

Mapped as a historical entry.

If the multi-model question is being asked at all, the sequence in
[`../README.md`](../README.md#decision-tree) applies: check whether one model dominates, then
check whether PostgreSQL with `JSONB` and [Apache AGE](../../graph/age/README.md) covers it, and
only then evaluate [ArangoDB](../arangodb/README.md).

For this platform the answer is no at the first step.

---

[← Multi-model databases](../README.md)
