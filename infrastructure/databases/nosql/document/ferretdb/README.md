[← Document stores](../README.md)

# FerretDB

<https://github.com/FerretDB/FerretDB>

---

## The problem it solves

MongoDB's wire protocol, with **PostgreSQL underneath**.

Applications connect with an ordinary MongoDB driver and issue ordinary MongoDB queries.
FerretDB translates them into SQL against PostgreSQL, where the documents are stored as `JSONB`.

That turns two separate problems into one answer:

| Problem | How this addresses it |
|---|---|
| **The SSPL licence** | MongoDB is SSPL, which is not OSI-approved and restricts offering it as a service. FerretDB is Apache 2.0 |
| **Another stateful system** | if PostgreSQL is already operated, backed up and monitored, this adds no new database to run |
| Two databases for one platform | documents and relational data in the same engine, with one backup strategy |

## When to use it

- **existing code speaks the MongoDB protocol**, and running MongoDB is unattractive
- the SSPL licence is a genuine constraint on how the product ships
- PostgreSQL is already running, and adding a second stateful system is the cost being avoided
- the document workload is modest — application state, configuration, semi-structured records

## When not to use it

- **MongoDB-specific features are in use** — aggregation pipeline stages, change streams,
  sharding, Atlas Search. Compatibility is good and it is not complete
- the collection genuinely outgrows one PostgreSQL instance; sharding is MongoDB's answer and not
  this one
- performance characteristics have been tuned against MongoDB's engine
- the requirement is documents and there is no existing Mongo code — plain `JSONB` in PostgreSQL
  is simpler than a translation layer

## The limitation to verify first

Compatibility is a **moving target**. FerretDB implements a large and growing subset of the
MongoDB API, and the honest way to evaluate it is to run the application's actual queries rather
than to read the compatibility matrix.

The areas that most often fall outside it:

| Feature | Status |
|---|---|
| Basic CRUD, indexes, common aggregation | works |
| **Change streams** | the CDC path most data platforms depend on — check before assuming |
| Sharding | not the model; PostgreSQL scaling applies instead |
| Transactions | more limited than MongoDB's |
| Text search, geospatial | partial |

The change-streams row matters specifically for this repository, because that is how MongoDB data
reaches [`data-streaming/`](../../../../data-streaming/README.md).

## The architectural point

Worth naming, because it is the reason this is interesting beyond the licence.

A document store is usually adopted because the *application* wants documents — not because the
data outgrew relational storage. FerretDB separates those two concerns: the application keeps the
document API it was written against, and the operations team keeps one database.

That is the same argument [`sql/`](../../../sql/README.md#2-postgresql-is-usually-the-answer)
makes about `JSONB`, applied to code that has already been written and will not be rewritten.

## Notes

**The interesting entry in this folder for this platform.**

With [CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already running PostgreSQL
here, a MongoDB requirement becomes a compatibility layer over a database that is already
operated, backed up and monitored — rather than a second stateful system with its own operator,
its own backup story and its own failure modes.

On a single cluster that is most of the argument. The check to do first is section 4: run the real
queries, and specifically confirm whether change streams are needed, because that is the path
MongoDB data takes out of the database in this platform.

---

[← Document stores](../README.md)
