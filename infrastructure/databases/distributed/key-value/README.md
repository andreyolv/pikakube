[← Distributed databases](../README.md)

# Distributed key-value stores

The consensus layer itself — the thing other databases are built on.

Tools covered: [`etcd`](etcd/README.md) · [`tikv`](tikv/README.md) ·
[`foundationdb`](foundationdb/README.md)

---

## What this folder is, and is not

These are **not** the key-value stores in [`nosql/key-value/`](../../nosql/key-value/README.md).
Redis and Memcached are caches: fast, in-memory, ephemeral by design. These are the opposite —
slower per operation, strictly durable, transactional, and built to be the foundation something
else stands on.

| | `nosql/key-value/` | this folder |
|---|---|---|
| Purpose | cache, session, counter | durable, consistent state |
| Consistency | eventual, or single-node | **linearizable, via consensus** |
| Speed | microseconds | milliseconds — a write is a quorum round trip |
| Used directly by applications | yes | rarely |
| Used by other databases | no | **that is the point** |

The reason to understand them is that they explain the systems above them:

- **etcd** is where Kubernetes keeps every object in the cluster
- **TiKV** is the storage layer [TiDB](../newsql/tidb/README.md) is built on
- **FoundationDB** is a transactional substrate other databases are built upon —
  [ByConity](../../analytical/byconity/README.md) in this repository uses it

Knowing that a NewSQL engine is a SQL layer over a consensus-replicated key-value store explains
its latency profile immediately, and makes the [`newsql/`](../newsql/README.md) trade-offs read
as consequences rather than as arbitrary limitations.

## The tools

| Tool | Consensus | Where it shines | Detail |
|---|---|---|---|
| **etcd** | Raft | Kubernetes' store; small, critical, strongly consistent configuration and coordination | [→](etcd/README.md) |
| **TiKV** | Raft, per range | a distributed transactional KV store with automatic sharding — the layer under TiDB | [→](tikv/README.md) |
| **FoundationDB** | its own | **ACID transactions across the whole keyspace**, and the most rigorous correctness testing in this list | [→](foundationdb/README.md) |

FoundationDB deserves its reputation for one reason above the others: its deterministic
simulation testing runs the entire cluster — including disk failures, network partitions and
clock skew — inside a single deterministic process, so failure scenarios are reproducible. That
is a genuinely unusual engineering position and it is why other databases are willing to build on
it.

Its constraint is equally distinctive: transactions are limited to 5 seconds and 10 MB. That is a
deliberate design decision, and it means the data model must be built around it rather than
discovering it later.

## When you would use one directly

Rarely, and the honest answer is usually "you would not". The cases that do exist:

- **Coordination** — leader election, distributed locks, service discovery. etcd is built for
  exactly this and it is a small, well-understood dependency
- **Configuration that must be consistent** — small, read often, and wrong answers are
  unacceptable
- **Building a system** that needs a transactional substrate and should not implement consensus
  itself. That is FoundationDB's entire purpose

What they are not for: bulk data, high-throughput writes, large values, or anything that looks
like a general-purpose database.

## The etcd warning

Because it is already running in every Kubernetes cluster, and it is the component whose failure
means the cluster stops rather than degrades:

| Concern | Detail |
|---|---|
| **Disk latency** | etcd is `fsync`-bound. Slow disks cause leader elections, and leader elections cause API server timeouts |
| **Database size** | the default quota is 2 GB; exceeding it puts the cluster into a read-only alarm state |
| Compaction and defrag | revisions accumulate; without compaction the size grows without bound |
| **Backups** | a snapshot is the only real recovery path for cluster state |
| Members | an odd number. Three or five |
| Watch load | many watchers on many objects is a real cost, and controllers are watchers |

The disk row is the one that turns into an incident. "The API server is slow" is very often
"etcd is waiting on `fsync`", and the fix is storage rather than anything in the control plane —
see [`storage/`](../../../site-reliability-engineering/storage/README.md).

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| etcd as an application database | it is sized and tuned for small, critical, mostly-read state | a real database |
| Large values in etcd | every write is replicated by consensus, and the quota is small | store a reference |
| Ignoring etcd disk latency | leader elections, then API timeouts, then a cluster that appears broken | fast storage, and alert on `fsync` duration |
| No etcd backup | cluster state has no other recovery path | scheduled snapshots, tested |
| An even number of members | no better availability, and a worse quorum arithmetic | three or five |
| Deploying FoundationDB casually | a genuinely different operational model, and the transaction limits shape the data model | understand the constraints first |
| Treating these as caches | strictly durable, consensus-replicated, and correspondingly slow | [`nosql/key-value/`](../../nosql/key-value/README.md) |

## How this applies to pikakube

**etcd is already running** — it is where the Kind cluster stores every object. Nothing else in
this folder is deployed, and the folder's value is mostly explanatory.

One deployment note is recorded and worth surfacing: the
[ByConity](../../analytical/byconity/README.md) chart depends on FoundationDB, and its
`fdb-operator.enabled: true` value does **not** install the CRDs, so the deployment fails with
`no matches for kind "FoundationDBCluster"`. The operator has to be installed first, separately,
with that value left off — a good illustration of what "built on FoundationDB" costs
operationally.

---

[← Distributed databases](../README.md)
