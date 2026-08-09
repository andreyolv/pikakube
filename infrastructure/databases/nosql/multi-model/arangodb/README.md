[← Multi-model databases](../README.md)

# ArangoDB

<https://github.com/arangodb/arangodb>
<https://github.com/arangodb/kube-arangodb>

Examples: <https://github.com/arangodb/kube-arangodb/tree/master/examples>

---

## What it is

The credible multi-model database: documents, graphs and key-value in one engine, queried by
**AQL** across all three.

```aql
FOR account IN accounts
  FILTER account.status == "active"
  FOR related IN 1..4 OUTBOUND account transfers
    RETURN {account, related}
```

That query filters documents and traverses a graph in one statement. Doing the equivalent with a
document store and a graph database means two queries, two round trips, and the join in
application code — which is the multi-model argument in its strongest form.

| Capability | Detail |
|---|---|
| **AQL across models** | one language for documents, graphs and key-value |
| **Native graph traversal** | not a bolt-on; it is a first-class part of the engine |
| Joins | between collections, unlike most document stores |
| ACID transactions | including across collections |
| **kube-arangodb** | a real operator — clusters, failover, backups |
| Deployment modes | single, active-failover, and a sharded cluster |

## When to use it

- **more than one model is genuinely required**, and the alternative is two stateful systems
- **cross-model queries** are part of the requirement, not just two datasets
- graph traversal matters, and a document store alone would push it into application code
- the operational cost of running two databases is the thing being avoided

## When not to use it

- one model dominates — use the specialist:
  [MongoDB](../../document/mongo/README.md), [Neo4j](../../graph/neo4j/README.md),
  [Redis](../../key-value/redis/README.md)
- **PostgreSQL is already running** — `JSONB` plus [Apache AGE](../../graph/age/README.md) is
  documents and graph in a database that is already operated
- specialist depth is needed — graph algorithms, Mongo's ecosystem, Redis's latency
- the licence is a constraint — see below

## The licence

Worth checking rather than assuming. ArangoDB's community edition terms have changed over the
project's life, including a move away from Apache 2.0 for the core, and the boundary between the
community and enterprise editions has shifted.

The features most relevant to a production deployment — some clustering and security capabilities
— have at times sat on the enterprise side. Establish the current terms before designing around
it, and specifically before assuming clustering is available.

## The operator

[kube-arangodb](https://github.com/arangodb/kube-arangodb) is a genuine operator rather than a
chart that starts pods:

| CRD | What it declares |
|---|---|
| `ArangoDeployment` | the cluster — single, active-failover, or sharded |
| `ArangoBackup` | scheduled backups, to object storage |
| `ArangoLocalStorage` | local persistent volumes |
| `ArangoDeploymentReplication` | datacentre-to-datacentre replication |

That is a stronger deployment story than most of this catalogue, and it is one of the concrete
reasons ArangoDB is the one to evaluate in this category rather than
[OrientDB](../orientdb/README.md).

## Notes

Mapped with the operator and its
[examples](https://github.com/arangodb/kube-arangodb/tree/master/examples).

For this platform the answer is no, and the reason is in
[`../README.md`](../README.md#how-this-applies-to-pikakube): the models are already covered.
[Redis](../../key-value/redis/README.md) is genuinely in use, MongoDB and Neo4j are mapped, and
PostgreSQL with `JSONB` plus [AGE](../../graph/age/README.md) would cover documents and graph in
the database [CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already runs.

Consolidating into ArangoDB would mean introducing a new stateful system to reduce a count that
is not causing pain — which fails the test in
[`../README.md`](../README.md#the-counter-argument).

---

[← Multi-model databases](../README.md)
