[← Graph databases](../README.md)

# Neo4j

<https://github.com/neo4j/neo4j>
<https://github.com/neo4j/helm-charts>
<https://github.com/neo4j/neo4j-python-driver>
<https://github.com/neo4j-contrib/neo4j-streams>

Query language: <https://github.com/opencypher/opencypher>

---

## The problem it solves

The default graph database, and the reason is ecosystem rather than any single technical
advantage: the most tooling, the most documentation, the most people who have used it, and
**Cypher**, which is the closest thing this category has to a standard query language.

```cypher
MATCH (a:Account)-[:TRANSFERRED*1..4]->(b:Account)
WHERE a.id = $id
RETURN b
```

That query — every account within four transfers — is the thing a relational database cannot do
well, and the reason to be in [`graph/`](../README.md) at all.

| Capability | Detail |
|---|---|
| **Cypher** | declarative, readable, and the basis of the ISO GQL standard |
| Neo4j Browser | a genuinely good visual query and exploration tool |
| **APOC** | a large procedure library — imports, graph algorithms, utilities |
| Graph Data Science | centrality, community detection, pathfinding, embeddings |
| Drivers | Python, Java, JavaScript, Go, .NET, all first-party |
| Bloom | visual exploration for non-technical users |

## When to use it

- **traversal is the primary query**, at three hops or more
- the ecosystem matters — tooling, answers, and hiring
- graph algorithms are part of the requirement, not just traversal
- a visual exploration tool would be used

## When not to use it

- one or two hops — that is a join, in a database you already run
- **the Community Edition's limitations bite** — see below
- real-time streaming ingestion with very low latency —
  [Memgraph](../memgraph/README.md)
- the graph is moderate and PostgreSQL is already running —
  [Apache AGE](../age/README.md) adds Cypher to it
- very large graphs requiring horizontal sharding —
  [NebulaGraph](../nebula/README.md)

## The licence, which is the recurring issue

This decides more Neo4j adoptions than any technical factor, and it is best understood before
designing around it.

| | Community Edition | Enterprise |
|---|---|---|
| Licence | GPLv3 | commercial |
| **Clustering** | **no** | yes |
| **Multiple databases** | **one** | yes |
| Role-based access control | no | yes |
| Hot backups | no | yes |
| Graph Data Science | limited | full |

**Community is a single instance with a single database and no clustering.** For development,
for a moderate graph, and for a workload that tolerates restarts, that is genuinely enough — and
it is important to know it is the ceiling rather than the starting point.

The absence of clustering means high availability is not available at any configuration; it is a
commercial feature.

## Streaming and CDC

[neo4j-streams](https://github.com/neo4j-contrib/neo4j-streams) connects Neo4j to Kafka in both
directions — ingesting from topics, and producing change events.

That matters for a data platform, because the realistic way a graph stays current is being fed
from the systems of record rather than written to directly. Building the graph as a **projection**
of relational and event data — rather than as a second source of truth — avoids the
synchronisation problem described in
[`../README.md`](../README.md#6-anti-patterns).

## Modelling notes

Two things that decide whether it performs:

**Supernodes.** A node with a million relationships makes every traversal through it slow, and
the query planner cannot help. Model around them — intermediate nodes, or relationship-type
partitioning — before they appear.

**Bounded traversal.** `MATCH (a)-[*]-(b)` can walk the entire graph. Always specify a depth:
`[*1..4]`. This is the single most common cause of a query that never returns.

## Notes

Mapped as a standard deployment with the official Helm chart, the Python driver, and a
**tutorial series** — fundamentals, create, basic queries, filtering, update, delete and
aggregation — which is more depth than most entries in this catalogue.

[openCypher](https://github.com/opencypher/opencypher) is recorded alongside it, and it is why
that tutorial content transfers: the same queries run against [Memgraph](../memgraph/README.md)
and [Apache AGE](../age/README.md). Learning Cypher is a more durable investment than adopting
Neo4j.

Its realistic role here is the same as MongoDB's — a **standard deployment** and a source
system, not a system of record for the platform. And for a graph that fits on one machine,
[AGE](../age/README.md) on the PostgreSQL that
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already runs is the option that
costs least.

---

[← Graph databases](../README.md)
