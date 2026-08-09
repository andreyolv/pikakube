[← Wide-column stores](../README.md)

# ScyllaDB

<https://github.com/scylladb/scylladb>
<https://github.com/scylladb/scylla-operator>

---

## The problem it solves

Cassandra, rewritten in C++.

It is protocol-compatible: the same CQL, the same drivers, the same data model. What changes is
the engine underneath, and the argument is entirely operational.

| | Cassandra | ScyllaDB |
|---|---|---|
| Runtime | JVM | **C++, no garbage collector** |
| Threading | thread pools | **shard-per-core**, shared-nothing |
| Latency | good, with GC pauses | **lower, and far more predictable tail latency** |
| Nodes for the same load | baseline | **typically fewer** |
| Tuning | JVM heap and GC are a discipline | largely self-tuning |
| Ecosystem | **much larger** | growing |
| Licence | **Apache 2.0** | see below |

**Tail latency is the honest headline.** Garbage-collection pauses are why a Cassandra cluster's
p99 looks worse than its median, and removing the JVM removes that class of problem. For a
serving layer where the p99 is the number that matters, that is a real difference rather than a
benchmark artefact.

The shard-per-core design pins work to cores and gives each its own memory and its own portion of
the data, which is why it uses a large machine more effectively than a JVM process does.

## When to use it

- Cassandra's **data model is right** and its operational profile is not
- tail latency matters — p99 rather than average
- fewer, larger nodes is preferable to more, smaller ones
- JVM tuning is work nobody wants to own

## When not to use it

- **the licence is a constraint** — see below; this is the main reason to decline it
- the ecosystem matters: tooling, answers, and people who have operated it
- the workload does not actually need this family — check
  [`../README.md`](../README.md#5-decision-tree) first
- an existing Cassandra estate with operational knowledge built around it

## The licence

Worth checking rather than assuming, because it has moved.

ScyllaDB Open Source was AGPL. The project has since shifted its open-source and enterprise
boundary, with features and versions distributed differently over time, and the terms are not
the same as Cassandra's Apache-2.0 position.

For a repository that catalogues open-source tooling, that is the substantive difference between
these two — not the performance. Cassandra's licence is unambiguous and unchanging; this one
requires reading the current terms.

## Migration from Cassandra

Genuinely straightforward, which is unusual for a database change:

| Aspect | Effort |
|---|---|
| CQL and drivers | **none** — protocol-compatible |
| Data model | **none** — the same partition-key rules apply |
| Data migration | supported paths exist, including reading Cassandra SSTables |
| Operations | new — different tooling and different tuning assumptions |
| Cluster sizing | usually **smaller** |

What does not transfer is the operational knowledge: the monitoring, the runbooks and the
intuitions are Cassandra's, and the failure modes here are different even though the API is not.

## Notes

Mapped with the [scylla-operator](https://github.com/scylladb/scylla-operator), which is the
realistic way to run it — bootstrap, repair, node replacement and rolling upgrades are sequenced
stateful procedures regardless of which engine implements them.

Nothing here is deployed, for the same reason as [Cassandra](../cassandra/README.md): a masterless
multi-node store on a single Kind cluster demonstrates the API and none of the properties.

The decision between the two, stated plainly: **Cassandra for the ecosystem and the Apache
licence, ScyllaDB for latency and cluster size.** The prior question — whether this family is
needed at all — is the one that matters more, and
[`../README.md`](../README.md#7-how-this-applies-to-pikakube) answers it for this platform with a
qualified no.

---

[← Wide-column stores](../README.md)
