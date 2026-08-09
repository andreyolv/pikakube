[← Schema documentation](../README.md)

# SchemaSpy

<https://github.com/schemaspy/schemaspy>

---

## The problem it solves

Point it at a database and it produces a browsable HTML site describing the schema — every table,
every column, every constraint, and **entity-relationship diagrams generated from the foreign
keys**.

The output is generated from the catalogue, so it is necessarily current. There is nothing to
maintain and nothing that can drift, which is the whole argument in
[`../README.md`](../README.md#the-problem-it-solves).

| Output | Why it is useful |
|---|---|
| Table and column inventory | with real types, nullability and defaults |
| **ER diagrams** | per table and per schema — how structure becomes visible |
| **Orphan tables** | no foreign keys in either direction; the strongest available "this is dead" signal |
| Constraints and indexes | what is enforced, versus what is merely intended |
| **Anomalies** | columns nullable but never null, missing indexes on foreign keys |
| Comments | `COMMENT ON` surfaced beside each object |

The orphan-table list is the practical one. Identifying unused tables in an inherited database is
otherwise guesswork, and this is close to the only automatic signal available.

## When to use it

- **inheriting a database** nobody can fully explain — the fastest available orientation
- onboarding, where a diagram beats a walkthrough
- planning a refactor, where the relationship graph *is* the blast radius
- producing a reference for people who will not open a SQL client

## When not to use it

- a schema designed last month by the person asking
- **as a substitute for meaning** — it describes structure; see below
- against production without thought — it is a catalogue read, and the same care applies as to
  any other query someone runs there

## Running it

It is a Java application, and the container image is the least awkward way to use it:

```bash
docker run --rm \
  -v "$(pwd)/output:/output" \
  schemaspy/schemaspy:latest \
  -t pgsql -host <host> -port 5432 -db <database> \
  -u <user> -p <password> -o /output
```

Two things to get right:

| Concern | Detail |
|---|---|
| **JDBC driver** | the image bundles common ones; some engines need the jar supplied |
| **Graphviz** | required for the ER diagrams — present in the image, absent from most hosts |
| Credentials | a **read-only** user is sufficient, and is what should be used |
| Schema filtering | large databases benefit from generating per schema rather than all at once |

## The limitation, stated plainly

SchemaSpy documents **structure**, not **meaning**. It will report that `orders.status` is a
`varchar(20)` with no foreign key. It cannot say that `3` means cancelled-after-dispatch and that
nothing has written `4` since 2021.

Two things fill that gap, and only one is a tool:

- **`COMMENT ON`** — a first-class PostgreSQL feature that lives in the catalogue and is surfaced
  directly in SchemaSpy's output. Adding comments in migrations is the highest-leverage habit
  here, because it captures meaning at the moment someone knows it
- **a data catalogue** — ownership, lineage and glossary, which is
  [`data-governance/`](../../../../data-governance/README.md)

## Notes

Mapped as the schema-documentation option. For this platform the value is as a **process** rather
than a deployed service: run it against a
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) replica, publish the output, and
regenerate it when the schema changes.

The two connections worth making, from [`../README.md`](../README.md):

- [`migration/`](../../migration/README.md) is where `COMMENT ON` statements belong — written
  with the column, by the person who knows why it exists
- [`management/`](../../management/README.md) gives people a query interface, and giving them one
  for a schema nobody can explain moves the bottleneck rather than removing it

Generating against a replica rather than the primary is the detail worth keeping — it is a
harmless read until it is the one that coincides with something else.

---

[← Schema documentation](../README.md)
