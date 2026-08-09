[← Graph databases](../README.md)

# Dgraph

<https://github.com/dgraph-io/dgraph>
<https://github.com/dgraph-io/charts>

---

## What it is

A distributed graph database with a **GraphQL-shaped interface**. Define a GraphQL schema, and
Dgraph generates the API — queries, mutations and the storage behind them.

That is its distinguishing idea: for a team already building a GraphQL API, the database and the
API layer collapse into one thing.

| Property | Detail |
|---|---|
| **GraphQL native** | a schema produces a working API, without a resolver layer |
| **DQL** | its own query language, for what GraphQL cannot express |
| Distributed | sharded and replicated via Raft, horizontally scalable |
| Written in | Go — a single binary, no JVM |
| Transactions | ACID, distributed |

## When to use it

- **GraphQL is the API layer**, and eliminating the resolver plumbing is worth something
- the graph is large enough to need distribution
- a Go-based single binary is preferable to a JVM deployment

## When not to use it

- **Cypher portability matters** — DQL is specific to Dgraph, and the argument in
  [`../README.md`](../README.md#3-query-languages) applies with full force
- the ecosystem matters — [Neo4j](../neo4j/README.md) has far more of it
- graph algorithms are the requirement; there is no equivalent of Graph Data Science
- the graph fits on one machine and PostgreSQL is running —
  [Apache AGE](../age/README.md)
- **project stability is a concern** — see below

## The project history

Worth knowing before adopting it, because the trajectory has not been smooth.

Dgraph Labs went through significant upheaval — layoffs, a change of direction, and a period
where development slowed markedly. The project was subsequently taken on by Hypermode, and
activity resumed.

That history does not make it a bad database; the engineering is genuinely interesting. It does
mean the usual due diligence applies with more weight than for a project with a boring history:
check recent commit activity, release cadence, and who is answering issues, rather than relying
on its reputation from several years ago.

## The GraphQL question

The pitch is compelling and the trade deserves stating.

Generating the API from a schema removes a layer of code. It also means **the database's data
model and the API contract are the same thing** — so an API change is a schema migration, and an
internal storage decision is visible to every consumer.

For a small service that is a simplification. For a platform where the API is a contract with
other teams — see [`api-contract/`](../../../../docs/api-contract/README.md) — coupling the two
removes the ability to evolve them independently, which is usually the point of having a contract.

## Notes

Mapped with the [official charts](https://github.com/dgraph-io/charts).

For this platform it is the least likely entry in [`graph/`](../README.md) to be chosen, and the
reason is the combination in section 2: a non-Cypher query language, and a project history that
warrants checking. Either alone would be manageable; together they mean the graph queries written
here would be specific to a database that requires ongoing verification of its momentum.

The alternatives for the same requirement: [Neo4j](../neo4j/README.md) for the ecosystem,
[NebulaGraph](../nebula/README.md) for distribution, [AGE](../age/README.md) for the case this
cluster actually has.

---

[← Graph databases](../README.md)
