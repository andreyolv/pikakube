[← Document stores](../README.md)

# RavenDB

<https://github.com/ravendb/ravendb>

---

## The problem it solves

A document database that **does not give up ACID transactions**.

That is the distinguishing claim. Most of this folder trades transactional guarantees for the
document model — see
[`../README.md`](../README.md#5-what-actually-goes-wrong) — and RavenDB's position is that the
trade was never necessary.

| Capability | Why it stands out here |
|---|---|
| **ACID across documents** | fully transactional, not "transactions with caveats" |
| **Automatic indexing** | it observes queries and creates the indexes they need |
| Built-in full-text search | Lucene-based, without a separate search system |
| Multi-model | documents, plus time-series, counters and attachments |
| **.NET-first** | the client library and the ecosystem are strongest there |
| Studio | a management UI shipped with the database |

**Automatic indexing** is the feature people remember. Issue a query with no suitable index and
RavenDB creates one, then maintains it. That removes a whole class of "the query is slow because
nobody added the index" — at the cost of indexes appearing that nobody chose, which is worth
monitoring rather than assuming is free.

## When to use it

- a **.NET estate**, where the client library and the idioms fit naturally
- documents *and* real transactions, without accepting the usual compromise
- full-text search matters and adding Elasticsearch is unattractive
- a small team that would rather not tune indexes

## When not to use it

- the ecosystem is the priority — [MongoDB](../mongo/README.md) has vastly more of everything
- the licence matters: RavenDB is **AGPL with a commercial option**, which needs checking against
  how the product ships
- polyglot teams where .NET is not the centre of gravity
- PostgreSQL `JSONB` would cover it, which for transactional documents it very often would

## The comparison that decides it

| | RavenDB | MongoDB | PostgreSQL `JSONB` |
|---|---|---|---|
| ACID across documents | **yes** | with caveats | **yes** |
| Automatic indexing | **yes** | no | no |
| Full-text search | built in | Atlas Search, or external | built in |
| Ecosystem | modest | **very large** | **very large** |
| Licence | AGPL / commercial | SSPL | **PostgreSQL licence** |
| Joins to relational data | no | no | **yes** |

The last row is the one that usually settles it for a platform rather than an application. If
transactions are the reason RavenDB is attractive, PostgreSQL provides them *and* joins *and* a
permissive licence — see
[`sql/`](../../../sql/README.md#2-postgresql-is-usually-the-answer).

RavenDB's remaining argument is the combination of automatic indexing and search in a .NET
context, which is real and narrow.

## Notes

Mapped for completeness. It is a genuinely well-engineered database and the least likely of this
folder to fit here, for a specific reason: this platform is not a .NET estate, and its strongest
argument — transactional documents — is already answered by
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) with `JSONB`.

Worth knowing about mainly so that the claim *"document stores cannot do transactions"* is not
made carelessly. RavenDB is the counter-example, and it shows the trade in
[`../README.md`](../README.md#5-what-actually-goes-wrong) is a design choice rather than a law.

---

[← Document stores](../README.md)
