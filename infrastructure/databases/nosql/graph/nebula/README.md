[← Graph databases](../README.md)

# NebulaGraph

<https://github.com/vesoft-inc/nebula>
<https://github.com/vesoft-inc/nebula-operator>

---

## The problem it solves

Graphs too large for one machine.

Everything else in [`graph/`](../README.md) scales vertically: [Neo4j](../neo4j/README.md)
Community is a single instance, [Memgraph](../memgraph/README.md) is bounded by RAM, and
[AGE](../age/README.md) is bounded by the PostgreSQL it runs in.

NebulaGraph is **distributed by design** — a shared-nothing architecture that partitions the
graph across storage nodes and scales horizontally.

| Component | Role |
|---|---|
| **Graphd** | stateless query engine; scale it for query throughput |
| **Storaged** | partitioned graph storage, replicated via Raft |
| **Metad** | cluster metadata and schema |

Separating the query layer from storage is the design's main consequence: query capacity and
storage capacity scale independently, which is not true of the alternatives here.

## When to use it

- the graph is **genuinely too large for one machine** — billions of edges
- horizontal scale is a requirement rather than an aspiration
- query throughput and storage need to grow at different rates

## When not to use it

- the graph fits on one machine, which for most platforms it does — the operational cost of a
  three-component distributed system is real
- the ecosystem matters — [Neo4j](../neo4j/README.md) has vastly more of it
- **Cypher portability matters** — see below
- real-time streaming ingestion — [Memgraph](../memgraph/README.md)

## nGQL, and why it matters

NebulaGraph uses its own query language, **nGQL**. It resembles Cypher and it is not Cypher.

That is a real adoption cost, and it cuts against the advice in
[`../README.md`](../README.md#3-query-languages): Cypher has the widest adoption, the emerging
ISO GQL standard is based largely on it, and choosing a Cypher-speaking engine keeps the query
layer portable between [Neo4j](../neo4j/README.md), [Memgraph](../memgraph/README.md) and
[AGE](../age/README.md).

Adopting nGQL means the queries are specific to this database. For a decision justified by scale
that may be acceptable; it should be a known cost rather than a discovery.

## Operationally

The [nebula-operator](https://github.com/vesoft-inc/nebula-operator) is the realistic way to run
it — three component types, Raft groups per partition, and rolling upgrades with ordering
constraints are not a StatefulSet's job.

What to size and decide deliberately:

| Concern | Detail |
|---|---|
| **Partition count** | set at space creation and **not changeable**; it caps how far the graph can be distributed |
| Replication factor | per space, and it decides survivability |
| Storage class | disk latency matters for traversal |
| Anti-affinity | Raft replicas on the same node is not replication |
| Minimum footprint | three component types, replicated — a real cluster before anything useful happens |

The partition-count row is the permanent decision, and it has the same character as the partition
key in [`column/`](../../column/README.md#2-the-partition-key-is-the-schema): chosen once,
before there is data, and expensive to revisit.

## Notes

Mapped as the horizontal-scale option. It is the right answer for a narrow and real case, and it
is the wrong answer for the case most platforms actually have — which is a graph that fits
comfortably on one machine and is chosen for traversal semantics rather than for size.

For this platform nothing here is deployed, and a distributed graph store on a single Kind
cluster would demonstrate the API and none of the properties that justify it — the same position
as [Cassandra](../../column/README.md#7-how-this-applies-to-pikakube) and
[NewSQL](../../../distributed/newsql/README.md#7-how-this-applies-to-pikakube).

---

[← Graph databases](../README.md)
