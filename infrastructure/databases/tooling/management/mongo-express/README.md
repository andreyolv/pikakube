[← Management interfaces](../README.md)

# mongo-express

<https://github.com/mongo-express/mongo-express>
<https://github.com/cowboysysop/charts>

---

## What it is

A light web interface for MongoDB: browse databases and collections, view and edit documents, run
queries, manage indexes.

It is deliberately small — a Node application with a Mongo connection, and nothing else. That
makes it the quickest way to see what is actually in a collection during development.

| Capability | Detail |
|---|---|
| Collection browsing | documents rendered as JSON, with paging |
| Document editing | view, edit, delete |
| Queries | filter and sort, in Mongo's query syntax |
| Indexes | list and create |
| Import and export | JSON |
| GridFS | basic browsing |

## When to use it

- **development**, where "what does this document actually look like" is the question
- a quick look at a collection without a Mongo shell or a port-forward
- someone who needs to inspect data and will not use `mongosh`

## When not to use it

- **a mixed estate** — [CloudBeaver](../cloudbeaver/README.md) covers MongoDB alongside the
  relational databases, with one access model
- anything requiring roles or per-user permissions — see below
- production, unless the access questions below are answered properly
- aggregation-pipeline work, which is far better served by the shell or Compass

## The limitation that decides where it belongs

**There is no user model.** mongo-express authenticates with basic auth and connects to MongoDB
with one set of credentials. Everyone who reaches it has the same access, and that access is
whatever the configured Mongo user has.

That is fine for a development namespace and it is not an access-control mechanism. The
distinction in [`../README.md`](../README.md#the-problem-it-solves) applies directly: this is a
tool, not a way to grant controlled access.

If the requirement is "analysts should be able to query MongoDB without cluster credentials", this
is the wrong answer — [CloudBeaver](../cloudbeaver/README.md) has the roles that make that safe.

| Concern | What to do |
|---|---|
| **Credentials** | a scoped Mongo user, read-only unless editing is deliberately wanted |
| **Exposure** | internal ingress with authentication in front; never public |
| Basic auth | change the defaults — the documented ones are widely known |
| `NetworkPolicy` | it should reach MongoDB and nothing else |
| Which instance | a secondary for anything exploratory |
| Write access | it edits documents; grant that on purpose |

## Notes

Mapped with the [Cowboy Sysop chart](https://github.com/cowboysysop/charts), which is the
maintained packaging.

It was originally recorded alongside the [MongoDB deployment](../../../nosql/document/mongo/README.md)
itself, which reflects how it is actually used — a development convenience beside the database
rather than a platform service.

For this platform, MongoDB is a **source system** rather than something served — see
[`mongo/`](../../../nosql/document/mongo/README.md#notes) — so the realistic use is inspecting a
collection while building an extraction pipeline. That is exactly the case this tool is good at,
and exactly the case where its lack of a user model does not matter.

---

[← Management interfaces](../README.md)
