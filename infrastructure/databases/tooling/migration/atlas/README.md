[← Schema migration](../README.md)

# Atlas

<https://github.com/ariga/atlas>
<https://github.com/ariga/atlas-operator>

---

## The problem it solves

**Declarative schema migration, with a Kubernetes operator.** The repository states what the
schema should be; Atlas computes the diff against the live database and applies it.

That is Terraform's model applied to a database schema, and it is the one that fits GitOps — the
rest of this cluster reconciles desired state, and schema is otherwise the exception managed by
imperative scripts.

| Capability | Detail |
|---|---|
| **Declarative** | write the desired schema; the migration plan is generated |
| **`AtlasSchema` CRD** | the schema as a Kubernetes resource, reconciled by a controller |
| Versioned mode | it also supports classic ordered migration files |
| **Migration linting** | analyses a generated plan for destructive or blocking changes |
| Multi-database | PostgreSQL, MySQL, MariaDB, SQLite, SQL Server, ClickHouse |
| Schema inspection | reads an existing database into a schema definition |

**The linting is the feature that makes declarative safe.** The standard objection to generated
migrations is that the tool might do something destructive; `atlas migrate lint` inspects the
plan and flags exactly that — a dropped column, a lock-taking index build, a narrowing type
change — before it runs.

## When to use it

- **GitOps**, where schema should be reconciled like everything else in the cluster
- the schema should be a Kubernetes resource rather than a job somebody triggers
- destructive-change detection in CI is wanted
- more than one database engine is in play

## When not to use it

- versioned migrations are preferred, and the team wants to write the exact statement that will
  run — [Flyway](../flyway/README.md) or [Alembic](../alembic/README.md)
- **permissions and grants must be managed too** — see the note below
- data migrations dominate, which are inherently imperative
- a generated plan applied by a controller is more autonomy than is comfortable

## Notes

Recorded from evaluating it here:

> Does not support managing permissions via GitOps —
> [ariga/atlas#647](https://github.com/ariga/atlas/issues/647)

That is a real and specific limitation, and it is worth understanding rather than filing away.
Atlas reconciles **structure** — tables, columns, indexes, constraints. Roles, grants and row-level
security policies are outside what it manages.

The consequence for a platform: adopting Atlas does not make the whole schema declarative. Access
control remains a separate concern, handled either by a versioned migration tool alongside it, or
by whatever manages database users — which for
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md) is partly the operator itself.

That is a workable split, and it should be a decision recorded somewhere rather than discovered
when someone asks why a grant drifted.

## Where it fits here

**The strongest candidate for this platform**, for the reason in
[`../README.md`](../README.md#8-how-this-applies-to-pikakube): with CloudNativePG running
PostgreSQL and Flux reconciling everything else, a schema that is a CRD is consistent with how the
cluster already works.

The practical shape would be: `AtlasSchema` resources in Git, the operator reconciling them,
`atlas migrate lint` in CI to catch destructive plans, and grants managed separately with the
limitation above stated explicitly.

The alternative with the same model and a smaller surface is
[SchemaHero](../schemahero/README.md).

---

[← Schema migration](../README.md)
