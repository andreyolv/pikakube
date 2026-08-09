[← Redis](../README.md)

# redis-cluster

Sharding across nodes — and the one Redis topology that changes how clients behave.

---

## What it is

Redis Cluster splits the keyspace into **16,384 hash slots** distributed across primaries, each
with its own replicas. A key hashes to a slot, the slot lives on one node, and the client is
redirected to it.

That gives horizontal scale for both memory and throughput. It also changes the contract the
application works against, which is the part worth understanding before adopting it.

## The constraint that decides everything

**Operations spanning multiple keys only work if the keys are in the same slot.**

| Operation | Standalone | Cluster |
|---|---|---|
| `GET`, `SET` | fine | fine |
| `MGET` across keys | fine | **fails** unless the keys share a slot |
| `SUNION`, `ZUNIONSTORE` | fine | **fails** across slots |
| Transactions (`MULTI`) | fine | **single slot only** |
| Lua scripts | any keys | declared keys, single slot |
| `KEYS`, `SCAN` | one node | per node, and must be aggregated |

The escape hatch is **hash tags**: `{user:1000}:profile` and `{user:1000}:sessions` hash on the
part inside the braces, so they land on the same slot and can be operated on together.

That is a data-modelling decision, made in advance, and retrofitting it means changing every key
name. It is the direct equivalent of the partition-key problem in
[`column/`](../../../column/README.md) — the distribution key becomes part of the schema.

## When to use it

- the dataset **does not fit in one node's memory**
- write throughput exceeds what one primary can absorb
- the key access patterns are single-key, or the hash tags are already designed in

## When not to use it

- **for availability** — this is the most common mistake. Cluster is for *sharding*; replication
  plus Sentinel gives failover with none of the client constraints
- multi-key operations are used and hash tags have not been planned
- one node is sufficient, which it very often is — Redis holds a lot in a little
- vertical scale is possible — [DragonflyDB](../../dragonflydb/README.md) is Redis-compatible and
  multi-threaded, and scales up rather than out

The first row deserves emphasis. "We need high availability, so we set up Redis Cluster" is a
frequent and expensive misreading: it constrains every client and every data model to solve a
problem that replicas already solve.

## Operational notes

| Concern | Detail |
|---|---|
| **Client support** | the client must be cluster-aware and follow `MOVED` and `ASK` redirects |
| **Resharding** | moving slots between nodes is an online operation, and it is a real procedure |
| Minimum size | three primaries plus replicas — six pods before anything useful happens |
| Anti-affinity | a primary and its replica on the same node is not high availability |
| Failure semantics | losing a primary and its replicas makes that **slot range** unavailable, not the whole cluster |

The last row is worth internalising: a partial failure means part of the keyspace is gone while
the rest answers normally, which is a different debugging experience from a database being down.

## Notes

Kept as the sharded option in this folder, alongside three progressively simpler ones:

| Option | Use |
|---|---|
| [`redis-simple/`](../redis-simple/README.md) | development, throwaway |
| [`redis/`](../redis/README.md) | one Redis, configured properly |
| [`redis-operator/`](../redis-operator/README.md) | many instances, with failover |
| **redis-cluster** | one dataset too large for one node |

For this platform the honest position is that Redis is used as a **cache**, and a cache that fits
in one node's memory should stay in one node. Adopting cluster here would constrain the data
model and the clients to solve a scale problem that does not exist — which is the anti-pattern in
[`../../README.md`](../../README.md#7-anti-patterns), specifically.

---

[← Redis](../README.md)
