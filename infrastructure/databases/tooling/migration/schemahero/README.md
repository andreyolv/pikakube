[← Schema migration](../README.md)

# SchemaHero

<https://github.com/schemahero/schemahero>
<https://github.com/schemahero/schemahero-helm>

---

## The problem it solves

**Schema as a Kubernetes resource**, in the plainest possible form. A table is a custom resource;
an operator reconciles the database to match.

```yaml
apiVersion: schemas.schemahero.io/v1alpha4
kind: Table
metadata:
  name: orders
spec:
  database: primary
  name: orders
  schema:
    postgres:
      primaryKey: [id]
      columns:
        - name: id
          type: uuid
        - name: status
          type: text
```

No migration files, no ordering, no history table to reason about. The desired state is declared,
and the operator computes and applies the difference.

| CRD | What it declares |
|---|---|
| `Database` | the connection, and how credentials are obtained |
| **`Table`** | a table's columns, keys and indexes |
| `Migration` | a generated plan, which can require **explicit approval** before applying |

The `Migration` resource is the safety mechanism and the most interesting part: SchemaHero can be
configured to plan the change, surface it as an object, and wait for a human to approve it —
which addresses the usual objection to declarative schema tools.

## When to use it

- **GitOps-first**, and the schema should look like every other resource in the cluster
- the simplest possible declarative model is preferred over a broader tool
- an approval step before applying generated changes is wanted
- schemas for several small services, each owning its tables

## When not to use it

- **data migrations** — this is structure only, and data changes are inherently imperative
- migration linting and destructive-change analysis matter —
  [Atlas](../atlas/README.md) does that and this does not
- versioned migrations with an audit trail of exactly what ran —
  [Flyway](../flyway/README.md)
- a broad engine catalogue is needed; support here is narrower

## SchemaHero or Atlas

Both are declarative with operators, and they are not the same size of tool:

| | SchemaHero | [Atlas](../atlas/README.md) |
|---|---|---|
| Model | tables as CRDs | schema as a CRD, **plus** versioned mode |
| **Migration linting** | no | **yes** — destructive-change detection |
| Approval gate | **yes**, via `Migration` | via CI |
| Engines | fewer | more |
| Scope | Kubernetes-only | CLI, CI, and Kubernetes |
| Surface | **small** | larger |

**Atlas if linting matters**, which it usually does — a declarative tool generating a `DROP
COLUMN` unnoticed is the failure mode this whole category has to defend against, and Atlas
defends against it directly.

**SchemaHero if the smaller surface is the point**, and the approval gate is considered sufficient
protection.

## The shared caveat

Neither tool manages **grants, roles or row-level security**. That limitation is recorded
explicitly for [Atlas](../atlas/README.md) and applies here too: adopting a declarative schema
tool makes the structure declarative and leaves access control as a separate concern.

Worth deciding where that lives rather than discovering the gap later — for
[CloudNativePG](../../../sql/postgresql/operator/cnpg/README.md), the operator handles part of it.

## Notes

Mapped with its [Helm chart](https://github.com/schemahero/schemahero-helm).

For this platform it is the runner-up to [Atlas](../atlas/README.md), and the deciding factor is
linting: a controller that can apply a generated plan needs something checking that the plan is
not destructive, and Atlas provides it.

The idea is right either way, and it is the one worth taking from this folder — schema
reconciled by a controller is consistent with how everything else in this cluster is managed, and
it removes the class of drift that comes from migrations being run by whoever remembered.

---

[← Schema migration](../README.md)
