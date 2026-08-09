[← Management interfaces](../README.md)

# pgAdmin

<https://github.com/pgadmin-org/pgadmin4>

---

## What it is

The reference PostgreSQL client, maintained by people from the PostgreSQL project. It runs as a
web application, and it does considerably more than run queries.

That is the distinction from the other tools in this folder: they are query interfaces, and this
is an **administration** tool.

| Capability | Beyond querying |
|---|---|
| **Server statistics** | activity, locks, transactions, database size |
| **Roles and privileges** | created and inspected through the interface |
| Maintenance | `VACUUM`, `ANALYZE`, `REINDEX` invoked on an object |
| **Backup and restore** | `pg_dump` and `pg_restore` wrapped in a UI |
| Query plans | `EXPLAIN` rendered graphically, which is genuinely useful |
| Schema browser | every object type, with ER diagrams |
| Extensions, tablespaces, publications | the parts of PostgreSQL other tools ignore |

The graphical `EXPLAIN` is the feature worth mentioning on its own — a nested-loop join over a
sequential scan is much easier to see than to read.

## When to use it

- **PostgreSQL only**, and administrative depth is wanted
- someone needs to inspect roles, privileges or server activity through an interface
- query-plan analysis is part of the work
- the PostgreSQL-native tool is preferred to a generic one

## When not to use it

- **a mixed estate** — [CloudBeaver](../cloudbeaver/README.md) covers several engines with one
  access model
- the requirement is diagnosis rather than administration —
  [pghero](../../monitoring/pghero/README.md) answers "what is slow and what is blocking" far more
  directly
- **the access question has not been answered** — see
  [`../README.md`](../README.md#deciding-whether-to-deploy-one-at-all)
- a desktop client would serve the same people

## The thing to be careful with

pgAdmin's administrative capability is the reason to deploy it and the reason to be careful.

It can create roles, grant privileges, terminate sessions and restore backups. Configured with a
superuser and exposed on an ingress, it is not a query tool — it is complete control of the
database behind a login form.

| Concern | What to do |
|---|---|
| **Credentials** | never the superuser; a scoped role per person or per function |
| **Authentication** | SSO, not pgAdmin's own user list with a shared password |
| Exposure | internal only, with authentication in front |
| **Which server** | prefer a replica for anything exploratory |
| Write and admin capability | granted deliberately, and separately from read access |
| `NetworkPolicy` | it should reach the databases and little else |
| Server definitions | pgAdmin stores its own configuration; back it up or define it declaratively |

## pgAdmin or pghero

They overlap and answer different questions, which is worth being explicit about since both are
mapped in this repository:

| | pgAdmin | [pghero](../../monitoring/pghero/README.md) |
|---|---|---|
| Purpose | **administration** | **diagnosis** |
| Answers | manage roles, run queries, inspect objects | what is slow, what is blocking, which indexes are unused |
| During an incident | you can look things up | it tells you |
| Footprint | larger | small |

Both is a reasonable outcome. If only one, the deciding question is whether the need is
*administering* the database or *understanding* it.

## Notes

Mapped as the PostgreSQL-native option.

For this platform, [CloudBeaver](../cloudbeaver/README.md) is the recommendation in
[`../README.md`](../README.md#how-this-applies-to-pikakube) because
[`databases/`](../../../README.md) is a mixed estate — but pgAdmin remains the deeper tool for
PostgreSQL specifically, and its administrative surface is a real argument when the work is
administration rather than querying.

Note also that [CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) already makes
roles, databases and backups declarative resources — which removes a good part of what pgAdmin's
administrative features exist for, and is the better place for those changes to live.

---

[← Management interfaces](../README.md)
