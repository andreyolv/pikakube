[← Distributed key-value stores](../README.md)

# FoundationDB

<https://github.com/apple/foundationdb>
<https://github.com/FoundationDB/fdb-kubernetes-operator>

---

## What it is

A distributed, transactional key-value store designed to be the **substrate other databases are
built on** — Apple's, and used inside iCloud.

It provides one thing exceptionally well: **ACID transactions across the entire keyspace**,
distributed, with strict serializability. Everything else — the data model, the query language,
the indexes — is expected to be built above it as a "layer".

| Property | Detail |
|---|---|
| **Transactions** | ACID, across any keys, strictly serializable |
| Data model | ordered key-value, and nothing more |
| **Layers** | document, SQL and graph models built on top by others |
| Scale | horizontal, with automatic data distribution |
| **Testing** | see below — this is its real distinguishing feature |

## The reason for its reputation

**Deterministic simulation testing.** FoundationDB runs the entire cluster — every node, the
network between them, and the disks underneath — inside a single deterministic process, and
injects failures: partitions, disk corruption, clock skew, machine death, in every combination.

Because the simulation is deterministic, a failure found is a failure that can be **replayed
exactly**. Distributed-systems bugs that would otherwise be unreproducible become debuggable.

That is a genuinely unusual engineering position, and it is why other database projects are
willing to build on it rather than implementing consensus themselves.

## The constraint that shapes everything

**Transactions are limited to 5 seconds and 10 MB.**

That is deliberate rather than an oversight: bounded transactions are what make the system's
performance predictable and its conflict resolution tractable.

The consequence is that the data model must be designed around it. A bulk operation is many
transactions, not one, and idempotency and resumability become the application's responsibility.
Discovering this after building on it is expensive, which is why it belongs at the top of any
evaluation.

## When to use it

- **building a system** that needs a transactional distributed substrate
- correctness under failure is the primary requirement, above convenience
- the data model can be built above a key-value layer, within the transaction limits

## When not to use it

- as an application database — there is no query language, no schema, and no indexes
- the team is not prepared to build or adopt a layer
- coordination and configuration — [etcd](../etcd/README.md) is smaller and purpose-built
- caching — [`nosql/key-value/`](../../../nosql/key-value/README.md)

## Operationally

The [fdb-kubernetes-operator](https://github.com/FoundationDB/fdb-kubernetes-operator) manages
clusters through a `FoundationDBCluster` resource. FoundationDB has several process roles —
coordinators, storage, transaction logs, proxies — and assigning and rebalancing them is not
something to do by hand.

## Notes

Recorded from actually attempting to deploy something built on it, via
[ByConity](../../../analytical/byconity/README.md):

> `no matches for kind "FoundationDBCluster" in version "apps.foundationdb.org/v1beta2"`
>
> If `fdb-operator.enabled: true` is set in the values, it should bring up the FDB operator with
> its CRDs — and it does not. The operator has to be installed first, separately, with that value
> left off.

That is a good illustration of what "built on FoundationDB" costs operationally: the dependency is
a distributed system with its own CRDs and its own operator, and a chart that claims to handle it
as a sub-dependency may not install the CRDs at all.

The general lesson worth keeping: a Helm value that enables a dependency does not necessarily
install that dependency's CRDs, because CRDs and the resources using them cannot reliably be
applied in one pass. Installing the operator first and disabling the bundled one is the standard
workaround — and it is the kind of thing that is only learned by hitting it.

Nothing here is deployed. FoundationDB is catalogued because it explains the architecture of
things built on it, and because
[`../README.md`](../README.md#what-this-folder-is-and-is-not) makes the case that understanding
the layer underneath explains a great deal about the databases above it.

---

[← Distributed key-value stores](../README.md)
