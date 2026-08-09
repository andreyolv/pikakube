[← Tooling](../README.md)

# Schema documentation

What is actually in this database — answered from the database, not from memory.

Tools covered: [`schemaspy`](schemaspy/README.md)

---

## The problem it solves

Every organisation has a database nobody can fully explain. It has a few hundred tables, some
named for a project that no longer exists, and the people who designed it have moved on.

The questions that then take days instead of minutes:

- what does this table contain, and what still writes to it?
- which tables reference this one — what breaks if the column changes?
- is this table used, or a leftover from a migration in 2019?
- where does this value come from, and where does it go?

The information exists. It is in the catalogue — tables, columns, types, foreign keys,
indexes — and it is the one description of the schema that is **necessarily current**, because
it is generated from the thing itself.

## What generated documentation gives you

| Output | Why it matters |
|---|---|
| Table and column inventory | with real types, nullability and defaults |
| **Relationship diagrams** | foreign keys drawn, which is how structure becomes visible |
| Orphan tables | no inbound or outbound references — usually dead |
| Constraints and indexes | what is enforced, and what is merely intended |
| Anomaly detection | columns nullable but never null, missing indexes on foreign keys |
| Comments | if anybody wrote them, they surface here |

The orphan-table output is the practical one. Tables with no foreign keys in either direction
are the strongest available signal that something is unused, and it is very hard to get any
other way.

## The limitation, stated first

Generated documentation describes **structure**, not **meaning**. It will tell you that
`orders.status` is a `varchar(20)` with a foreign key to nothing. It cannot tell you that `3`
means cancelled-after-dispatch and that nothing has written `4` since a migration in 2021.

That gap is filled by two things, and only one of them is a tool:

- **Database comments** — `COMMENT ON COLUMN` is a first-class feature, it survives in the
  catalogue, and generators surface it. Comments in the DDL are documentation that ships with
  the schema and cannot drift from it.
- **A data catalogue** — ownership, lineage, glossary. That is a different concern and lives in
  [`data-governance/`](../../../data-governance/).

Writing comments as part of migrations is the highest-leverage habit here, and it costs a line
per column at the moment when someone actually knows the answer.

## When to generate it

| Situation | Value |
|---|---|
| Inheriting a database | **high** — the fastest available orientation |
| Onboarding a new engineer | high — a diagram beats a walkthrough |
| Planning a refactor | high — the relationship graph is the blast radius |
| A schema you designed last month | low — you already know |

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Hand-written schema documentation | correct on the day it is written, wrong within a month | generate it |
| Generated once and committed | it becomes a confidently wrong document | regenerate in CI, on schema change |
| Documenting structure and calling it done | types are not meaning; nobody was asking about types | comments, plus a catalogue |
| No `COMMENT ON` anywhere | the only place meaning could live is empty | write comments in migrations |
| Generating against production | it is a catalogue read, but so is every other "harmless" query someone runs there | a replica, or a restored copy |
| A diagram of 400 tables | unreadable, so nobody reads it | generate per schema or per domain |

## How this applies to pikakube

Nothing here is deployed. The value is as a **process** rather than a service: point
[SchemaSpy](schemaspy/README.md) at a database, publish the output, and regenerate it when the
schema changes.

Two connections worth making explicit:

- [`migration/`](../migration/README.md) is the right place to add `COMMENT ON` statements —
  the comment is written when the column is, by the person who knows why it exists
- [`management/`](../management/README.md) gives people a query interface; giving them one for a
  schema nobody can explain moves the bottleneck rather than removing it

Structure here, meaning in [`data-governance/`](../../../data-governance/). Neither substitutes
for the other.

---

[← Tooling](../README.md)
