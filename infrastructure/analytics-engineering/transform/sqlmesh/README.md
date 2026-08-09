[← Transform](../README.md)

# SQLMesh

<https://github.com/TobikoData/sqlmesh>
<https://sqlmesh.readthedocs.io/>

---

## The problem it solves

[dbt](../dbt/README.md) compiles SQL and runs it. It knows the **model graph** — which model references
which — but not what actually changed, at which column, or whether a change affects results at
all.

SQLMesh parses the SQL and tracks **column-level lineage and model state**. Two capabilities
follow that are hard to get otherwise:

**Virtual environments.** A change is built **once** and environments are views pointing at it.
Testing a change stops meaning duplicating the dataset per environment, which is where dbt's
warehouse costs come from.

**Breaking-change detection.** Because it understands the SQL, it can tell whether an edit
changes results — a comment or a reordered column does not — and reprocess only what genuinely
needs it.

| | dbt | SQLMesh |
|---|---|---|
| Understands | the model graph | the **SQL**, to column level |
| Environments | a full build per target | virtual — one build, many views |
| Incremental | you write the logic | managed, with automatic backfill of gaps |
| Change impact | "downstream models" | "these columns, in these models" |
| Ecosystem | very large | growing |

## When to use it

- **cost of rebuilds per environment** is a real problem
- "what breaks if I change this column?" is a question people ask and cannot answer
- incremental logic written by hand has produced gaps or duplicates
- you want a stricter model and can accept a smaller ecosystem

## When not to use it

- the ecosystem is the reason to use dbt: packages, adapters, and people who already know it
- the project is small enough that rebuild cost and lineage are not felt
- the team is mid-migration to something else and cannot absorb another change

## The honest comparison

SQLMesh is the more rigorous system. dbt is the default because ecosystem and familiarity are
worth a great deal in practice, and "more rigorous" does not by itself justify a migration.

The clean cases for adopting it: **starting fresh**, or **rebuild cost and lineage are actively
painful**. Migrating a working dbt project for elegance is rarely worth it.

Worth noting for this repository: its column-level lineage overlaps directly with what
[`data-governance/`](../../../data-governance/README.md) addresses through separate tooling — which makes
it a more interesting evaluation here than it would be elsewhere.

---

## Notes

```bash
sqlmesh init duckdb

sqlmesh plan            # apply to prod
sqlmesh plan dev        # apply to a virtual dev environment

sqlmesh fetchdf "select * from sqlmesh_example__dev.incremental_model"
sqlmesh fetchdf "select * from sqlmesh_example.incremental_model"
```

The two `fetchdf` calls show the point: `sqlmesh_example__dev` and `sqlmesh_example` are
**views over the same build**, not two copies of the data. That is the virtual environment
model in one command.

---

[← Transform](../README.md)
