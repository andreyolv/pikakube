[← Schema migration](../README.md)

# Bytebase

<https://github.com/bytebase/bytebase>

---

## The problem it solves

Not migration. **Change management.**

Every other tool in this folder answers *"how does the schema change get applied?"* Bytebase
answers *"who is allowed to change this, who reviewed it, and what actually ran in production?"*

That is a different problem, and it appears once more than one team can change the same database:

| Question | A migration tool | Bytebase |
|---|---|---|
| How is it applied? | yes | yes |
| **Who approved it?** | no | **yes** |
| Was it reviewed against a standard? | no | **yes** — automated review rules |
| What ran in production, and when? | partly | **an audit trail** |
| Can developers apply changes directly? | nothing stops them | **controlled** |
| Are ad-hoc queries recorded? | no | **yes** |

## What it provides

| Capability | Detail |
|---|---|
| **Review workflow** | schema changes as reviewable, approvable issues |
| **SQL review rules** | automated checks — naming conventions, missing indexes, dangerous statements |
| **Audit log** | who ran what, against which environment |
| GitOps integration | changes driven from a repository, with the workflow attached |
| Environment promotion | a change progresses dev → staging → production |
| Data masking | sensitive columns obscured in query results |
| Multi-engine | PostgreSQL, MySQL, and many others |

The **SQL review rules** are the underrated part. Rejecting a migration that adds a column without
a default to a large table, or one that builds an index without `CONCURRENTLY`, encodes the
anti-patterns in [`../README.md`](../README.md#7-anti-patterns) as an automated check rather than
as knowledge someone has to already have.

## When to use it

- **several teams change the same database**, and the process is currently trust
- schema changes need a documented approval trail — audit, compliance, or scale
- ad-hoc production queries should be recorded rather than run over a port-forward
- database change standards exist and are currently enforced by review, inconsistently

## When not to use it

- **one team, one database** — this is a governance product, and there is nothing to govern
- the requirement is applying migrations reliably —
  [Atlas](../atlas/README.md), [Flyway](../flyway/README.md) or
  [Alembic](../alembic/README.md) are far less to run
- a web application with its own database, users and workflow is more platform than the problem
  deserves
- GitOps purity matters; the workflow lives partly in Bytebase's own state

## The overlap worth naming

Bytebase overlaps two other folders in this repository, and the boundary is worth being clear
about:

| Concern | Where it belongs |
|---|---|
| Applying schema changes | this folder — Atlas, Flyway, Alembic |
| **Approval and audit of changes** | Bytebase |
| Querying the database safely | [`management/`](../../management/README.md) — CloudBeaver, pgAdmin |

It does the third as well, with data masking and query audit, which makes it a plausible
alternative to a management UI *if* the governance features are wanted anyway. Deploying it purely
as a query interface would be considerable overkill.

## Notes

Mapped as the governance option. For this platform the honest answer is that the problem it solves
does not exist here — a single-operator homelab has no approval workflow to encode, and the tools
in [`../README.md`](../README.md#8-how-this-applies-to-pikakube) cover the actual requirement.

It is worth having catalogued for the corporate case, which is where this genuinely matters: the
moment several teams share a database, "schema changes go through review" stops being a convention
people follow and becomes something that needs a mechanism. Bytebase is that mechanism, and the
alternative is a wiki page nobody reads.

---

[← Schema migration](../README.md)
