[← Application authorization](../README.md)

# OpenFGA

<https://github.com/openfga/openfga>
<https://github.com/openfga/helm-charts>

---

## The problem it solves

OpenFGA is the CNCF implementation of Google's **Zanzibar** model, described in
[`../README.md`](../README.md): permissions stored as a graph of relationships and computed by
traversing it, rather than stored as a list of grants.

Concretely, it answers the questions an application cannot express in RBAC:

| API | Question | Why it matters |
|---|---|---|
| `Check` | "may Bob view document 42?" | the per-request authorization decision |
| `ListObjects` | "which documents may Bob view?" | the query that makes a filtered UI possible without scanning everything |
| `ListUsers` | "who may view document 42?" | the query that makes an audit possible |
| `Expand` | "why?" — the relationship path that produced the answer | the debugging tool, and the reason a denial is explicable |

The model is declared once, in a DSL:

```
type document
  relations
    define parent: [folder]
    define owner:  [user]
    define editor: [user] or owner
    define viewer: [user] or editor or viewer from parent
```

Then relationships are written as tuples — `(document:42, owner, alice)` — and every permission
follows from the schema plus the tuples. Adding a document requires no new roles and no schema
change.

What distinguishes OpenFGA within its family:

- **CNCF incubating**, donated by Auth0/Okta. That governance matters for a component that sits
  on the request path of every authorization decision in a product — it is the difference between
  a dependency and a vendor.
- **Conditions.** Tuples can carry CEL expressions evaluated at check time, so attribute-based
  rules (time of day, IP range, a resource attribute) combine with the relationship graph. That
  closes the usual gap between ReBAC and ABAC without a second system.
- **Modelling tooling that is genuinely good.** A hosted playground, a VS Code extension with
  syntax support, and a well-defined **assertion** mechanism for testing a model. Given that
  schema design is the hard part, this is a substantial practical advantage.
- **Breadth of SDKs** — Go, JavaScript, Python, Java, .NET and more — plus both gRPC and HTTP
  APIs.

## When to use it

- **Per-object permissions in an application**, particularly with user-to-user sharing or a
  hierarchy that access should follow. The test in [`../README.md`](../README.md) §3 is the one
  to apply.
- **"What can this user see?" is on the render path.** `ListObjects` is designed for it; the
  alternatives are not.
- **Several services need to agree on permissions.** Centralising the decision is the argument,
  and the one that most often justifies the operational cost.
- **You want the safest choice in this family.** CNCF governance, the largest community, the best
  tooling.
- **You need relationship and attribute rules together.** Conditions handle this in one system.

## When not to use it

- **Roles are enough.** `admin` / `editor` / `viewer` over resource types is RBAC, and RBAC
  belongs in the application. Do not deploy a permission service for it.
- **Ownership is the only per-object rule.** An `owner_id` column and a `WHERE` clause is the
  entire answer and always will be faster.
- **For Kubernetes API permissions.** That is [`k8s-rbac/`](../../k8s-rbac/README.md), built into
  the API server.
- **You cannot accept a network call per check.** Authorization becomes a synchronous dependency
  of every request. There are caching and batching strategies, but the dependency is real and
  must be budgeted for.
- **You cannot keep tuples in sync.** Every object created, moved, reparented or deleted must
  write a tuple. If that cannot be guaranteed from every code path, the permission data is wrong
  in ways that are silent in both directions.
- **You have no application.** Stated plainly because it is the situation in this repository —
  see the Notes.

## Notes

**`https://github.com/openfga/openfga`** — the project. Go, Apache-2.0, CNCF incubating.

**`https://github.com/openfga/helm-charts`** — the official chart repository, which is what the
staged `HelmRepository` points at.

What is staged: a `HelmRepository`, a `Namespace` `openfga`, and a `HelmRelease` for the `openfga`
chart at version `0.2.3`.

| Setting | What it means |
|---|---|
| `replicaCount: 1` | single replica. It would be on the request path of every authorization decision, so anything real needs more |
| `telemetry.metrics.serviceMonitor.enabled: true` | Prometheus Operator scraping. Correct instinct — check latency is the metric that matters, because it lands directly in every request's budget |
| `datastore.engine: postgres` | the right choice. The in-memory engine loses every tuple on restart and exists for experimentation only |
| `postgresql.enabled: true` | the bundled Postgres subchart. Convenient for a demo; the platform already runs CloudNativePG, which would be the consistent choice |
| `datastore.uri: postgres://postgres:password@openfga-postgresql.openfga.svc.cluster.local:5432/postgres?sslmode=disable` | **credentials in plain text in the manifest**, matching the `postgresql.auth.postgresPassword: password` below it. These are chart placeholders and must become a Secret reference before this is applied anywhere |
| `sslmode=disable` | unencrypted database connections. Acceptable within a local cluster, wrong anywhere else |

Two things a working deployment would still need, neither of which is a Helm value:

- **A store and an authorization model.** OpenFGA is empty on startup. A *store* must be created,
  and a model written to it, through the API or the CLI (`fga`). The schema is the actual product
  and it lives outside the chart.
- **Tuple writes from the application.** Nothing populates the graph automatically. Every
  permission-relevant change in the application has to write a tuple, ideally in the same
  transaction as the change itself.

For this platform the conclusion in [`../README.md`](../README.md) applies without qualification:
there is no application with per-object permissions here, so there is nothing for OpenFGA to
answer. It is catalogued as the option to reach for if that ever changes — and it is the one to
reach for, over [Permify](../permify/README.md), on governance and ecosystem grounds.

---

[← Application authorization](../README.md)
