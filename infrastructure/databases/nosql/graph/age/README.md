[← Graph databases](../README.md)

# Apache AGE

<https://github.com/apache/age>

---

## The problem it solves

**Cypher inside PostgreSQL.** AGE is an extension, not a database — graph queries run against the
PostgreSQL instance that is already deployed, backed up, monitored and operated.

```sql
SELECT * FROM cypher('my_graph', $$
  MATCH (a:Account)-[:TRANSFERRED*1..4]->(b:Account)
  WHERE a.id = 1234
  RETURN b
$$) AS (account agtype);
```

That is a genuine graph traversal, in the same transaction as the relational query next to it,
against the same database.

| | A dedicated graph database | AGE |
|---|---|---|
| New stateful system | **yes** | no |
| Backups, monitoring, operator | new | **already exist** |
| Joins to relational data | in application code | **in the query** |
| Transactions across both | no | **yes** |
| Depth and scale | better | good enough for a lot |
| Ecosystem | Neo4j's is large | PostgreSQL's is larger |

## When to use it

- **PostgreSQL is already running** — which on this cluster it is
- the graph is moderate: millions of nodes rather than billions
- graph and relational data are queried together, which they usually are
- adding a stateful system for a graph capability is hard to justify

## When not to use it

- very large graphs, or traversals deep and hot enough that a purpose-built engine matters —
  [Neo4j](../neo4j/README.md) or [NebulaGraph](../nebula/README.md)
- graph algorithms are the requirement — centrality, community detection, embeddings. Neo4j's
  Graph Data Science library has no equivalent here
- real-time streaming ingestion with very low latency — [Memgraph](../memgraph/README.md)
- the tooling matters: there is no equivalent of Neo4j Browser

## What to check before committing

| Concern | Detail |
|---|---|
| **PostgreSQL version support** | AGE tracks specific major versions, and the supported set has lagged at times — check against what the operator runs |
| **Extension availability** | it must be installed in the image; the standard PostgreSQL images do not include it |
| Cypher coverage | a large subset, not all of it |
| `agtype` | results come back as AGE's own type, which needs casting |
| Performance at depth | good, and not equal to a native engine |

The first two rows are the practical blockers on Kubernetes. Running AGE with
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) means a container image that
includes the extension — either a community image that bundles it, or one built for the purpose.
That is a small piece of work and it is not zero, and it is worth knowing before the design
depends on it.

## The argument this makes

Worth stating explicitly, because it generalises beyond graphs.

[`sql/`](../../../sql/README.md#2-postgresql-is-usually-the-answer) argues that PostgreSQL
absorbs most of the reasons people reach for a second database — `JSONB` for documents, PostGIS
for geospatial, TimescaleDB for time-series. AGE extends that list to graphs, which
[`../README.md`](../README.md#1-why-this-one-is-different) names as one of only two NoSQL
families where the choice is genuinely forced.

It does not fully close the gap: a dedicated engine is faster at depth and has algorithms AGE
lacks. It does change the question from *"do we deploy a graph database?"* to *"is our graph big
enough to need one?"* — and for most platforms the answer to the second is no.

## Notes

**The pragmatic option for this cluster.** With
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already running PostgreSQL, a
graph capability that is an extension rather than a new stateful system is a materially different
proposition from deploying [Neo4j](../neo4j/README.md).

The Cypher knowledge transfers in both directions — see
[openCypher](https://github.com/opencypher/opencypher) — so starting here and moving to a
dedicated engine later, if the graph outgrows it, does not mean rewriting the queries.

---

[← Graph databases](../README.md)
