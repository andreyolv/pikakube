[← Schema migration](../README.md)

# Flyway

<https://github.com/flyway/flyway>

---

## The problem it solves

The versioned-migration default. Numbered SQL files, applied in order, each exactly once, tracked
in a table in the target database.

```
V1__create_orders.sql
V2__add_status_column.sql
V3__backfill_status.sql
```

There is no generator and no diff. **You wrote the statement that will run**, which is the entire
argument for this model: during a production change window, there is nothing to second-guess.

| Property | Detail |
|---|---|
| **Ordered, applied once** | tracked in `flyway_schema_history` |
| **Checksums** | an already-applied file that changes is detected and refused |
| Repeatable migrations | `R__` prefix, re-run when the content changes — good for views and functions |
| Callbacks | hooks before and after migration |
| Baseline | adopt it on an existing database without rewriting its history |
| Multi-database | most engines, via JDBC |

The checksum behaviour is what keeps environments honest: editing a migration that has already run
somewhere is the classic way environments diverge silently, and Flyway makes it an error rather
than a surprise.

## When to use it

- a **JVM estate**, where it is the established default and integrates with the build
- predictability matters more than automation — the exact SQL is reviewed and then executed
- **data migrations** alongside schema changes, which declarative tools handle poorly
- adopting migrations on an existing database, where `baseline` is the clean entry point

## When not to use it

- **GitOps-first**, where the schema should be a reconciled resource —
  [Atlas](../atlas/README.md) or [SchemaHero](../schemahero/README.md)
- Python and SQLAlchemy, where [Alembic](../alembic/README.md) generates migrations from model
  changes
- review and approval of schema changes is the actual requirement —
  [Bytebase](../bytebase/README.md)
- the Community edition's limits matter — see below

## The editions

Worth establishing early. Flyway is Red Gate's, and it is tiered:

| | Community | Teams / Enterprise |
|---|---|---|
| Versioned migrations | **yes** | yes |
| Checksums, baseline | yes | yes |
| **Undo migrations** | no | yes |
| Dry runs | no | yes |
| Some engines | limited | full |

Community covers the core competently and is what most projects use. The absence of undo
migrations is less of a loss than it sounds — see below.

## Rollback, honestly

Undo migrations exist and should not be relied on, in any tool.

Dropping a column does not restore its data. Reversing a type change does not recover what was
truncated. A migration that deleted rows cannot un-delete them.

The realistic position is **forward-only**: if a migration causes a problem, the fix is another
migration, and the safety net is backups. Which means the real protection is the expand-and-
contract discipline in
[`../README.md`](../README.md#5-the-part-that-breaks-expand-and-contract) — never deploying a
change that the currently-running application cannot tolerate.

## On Kubernetes

Run it as a `Job` or an init container that completes **before** the application rolls out.

Never at application startup: every replica would race, one would win arbitrarily, and the others
would either wait or fail. See
[`../README.md`](../README.md#6-running-migrations-on-kubernetes).

## Notes

Mapped as the versioned option. For this platform it is not the recommendation —
[`../README.md`](../README.md#8-how-this-applies-to-pikakube) points at the Kubernetes-native
tools, because a schema reconciled by a controller matches how everything else in this cluster is
managed.

Where Flyway would still earn a place is **data migrations**, which are imperative by nature and
which declarative tools do not attempt. A platform running Atlas for structure and Flyway-style
ordered scripts for data is a common and reasonable outcome rather than a failure to choose.

---

[← Schema migration](../README.md)
