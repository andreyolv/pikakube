[← Key-value stores](../README.md)

# KeyDB

<https://github.com/Snapchat/KeyDB>

---

## What it is

A **fork of Redis** that added multithreading, from Snap. It predates
[DragonflyDB](../dragonflydb/README.md) and answered the same question — one Redis instance uses
one core — by modifying Redis rather than rewriting it.

| | Redis | KeyDB |
|---|---|---|
| Origin | — | **a fork**, kept close to upstream |
| Threading | single-threaded core | multi-threaded |
| Active replication | primary/replica | **active-active**, two writable nodes |
| Licence | RSALv2 / SSPL / AGPL | **BSD** |
| Compatibility | — | very high; it is Redis with changes |

**Active replication** is its distinctive feature: two nodes both accepting writes and
replicating to each other. That is unusual in this family, and it comes with the conflict
semantics that multi-master always implies — last write wins, by timestamp — which is acceptable
for a cache and not for much else.

## The state of the project

Worth stating before anything else, because it decides whether the rest matters.

KeyDB was acquired by Snap in 2022. Development since has been **quiet** — maintenance rather
than momentum, and it has fallen behind upstream Redis versions.

Meanwhile the landscape moved: [Valkey](../valkey/README.md) now provides a BSD-licensed Redis
with the original maintainers and major backing, and [DragonflyDB](../dragonflydb/README.md)
provides a more thorough answer to the threading question.

KeyDB's two arguments — a permissive licence and multithreading — are each now better served
elsewhere.

## When to use it

- an **existing KeyDB deployment** that works
- active-active replication is specifically the requirement, and the conflict semantics are
  acceptable

## When not to use it

- **anything new** — [Valkey](../valkey/README.md) for the licence,
  [DragonflyDB](../dragonflydb/README.md) for the threading
- current Redis features matter; it lags upstream
- production dependence on a project with limited active development

## Where it fits in the folder

Reading the five tools as a sequence makes the position clear:

| Tool | Its argument | Still the best answer for it? |
|---|---|---|
| [Redis](../redis/README.md) | the ecosystem | yes |
| [Valkey](../valkey/README.md) | BSD licence | **yes** |
| [DragonflyDB](../dragonflydb/README.md) | multithreading, vertical scale | **yes** |
| **KeyDB** | BSD **and** multithreading | superseded on both |
| [Memcached](../memcached/README.md) | pure caching, no temptation | yes |

## Notes

Mapped for completeness and as a historical marker: KeyDB was the first serious attempt to make
Redis use more than one core, and that idea is now mainstream.

It is included in this catalogue for the same reason
[RethinkDB](../../document/rethinkdb/README.md) and
[OrientDB](../../multi-model/orientdb/README.md) are — knowing which projects have stalled is
part of mapping a solution space, and it stops someone re-evaluating them from a search result
that does not mention the commit history.

---

[← Key-value stores](../README.md)
