[← Schema migration](../README.md)

# Alembic

<https://github.com/sqlalchemy/alembic>

---

## The problem it solves

Migrations for **SQLAlchemy**, from the same author. It compares the ORM models against the live
database and generates the migration that closes the gap:

```bash
alembic revision --autogenerate -m "add status to orders"
alembic upgrade head
```

That is the distinguishing feature. In a Python application where the models already define the
schema, having a second hand-written description of it is duplication waiting to diverge —
Alembic derives one from the other.

| Property | Detail |
|---|---|
| **Autogenerate** | migrations derived from model changes |
| Versioned | ordered revisions, applied once, tracked in `alembic_version` |
| **Branching and merging** | revisions form a graph, so parallel feature branches can be merged |
| Python migrations | so data migrations are ordinary code |
| Offline mode | emit SQL for a DBA to review and run |

The branching support is unusual among migration tools and genuinely useful: two feature branches
each adding a migration produce a merge conflict in most tools, and a merge revision here.

## When to use it

- **Python with SQLAlchemy** — this is the case it exists for
- the ORM models are the source of truth for the schema
- data migrations written in Python alongside schema changes
- Airflow, FastAPI, or any Python service already using SQLAlchemy

## When not to use it

- the application is not Python — [Flyway](../flyway/README.md)
- **GitOps-first**, where the schema should be a reconciled Kubernetes resource —
  [Atlas](../atlas/README.md) or [SchemaHero](../schemahero/README.md)
- the schema is shared by several applications in different languages; deriving it from one
  application's models makes that application the owner
- review and approval workflow is the requirement — [Bytebase](../bytebase/README.md)

## Autogenerate is a draft, not an answer

The most important thing to know about the tool, and the source of most incidents involving it.

`--autogenerate` produces a **candidate** migration. It reliably detects added and removed tables
and columns, and it is unreliable in exactly the places that matter:

| Change | Detected |
|---|---|
| New table or column | yes |
| Dropped column | yes — and it will happily emit the `DROP` |
| **Renamed column** | **no** — it sees a drop and an add, which loses the data |
| Type changes | sometimes, depending on configuration |
| Constraint and index changes | inconsistently |
| Server defaults | often missed |

The rename row is the one that destroys data. A renamed column autogenerates as `DROP` plus
`ADD`, which passes review if nobody reads the generated file, and silently discards the contents.

**Every generated migration must be read before it is committed.** That is the discipline the
tool assumes and does not enforce.

## On Kubernetes

`alembic upgrade head` as a `Job` or init container that completes before the application rolls
out — never at application startup, where every replica races. See
[`../README.md`](../README.md#6-running-migrations-on-kubernetes).

## Notes

Mapped as the Python option, and it is the relevant one for the Python components in this
platform — [Airflow](../../../../data-engineering/orchestration/airflow/README.md) itself uses
Alembic for its own metadata database, which is a reasonable endorsement of the tool for that
role.

For the platform's own schemas the recommendation remains
[Atlas](../atlas/README.md), for the reason in
[`../README.md`](../README.md#8-how-this-applies-to-pikakube): a schema reconciled by a controller
matches how the rest of the cluster is managed.

Where Alembic wins is inside a Python service that owns its schema — there, deriving migrations
from the models is less duplication than maintaining a separate declarative definition of the same
thing.

---

[← Schema migration](../README.md)
