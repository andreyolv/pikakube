[← Visualisation](../README.md)

# Apache Superset

<https://github.com/apache/superset>
<https://superset.apache.org/>

---

## The problem it solves

Breadth. Superset connects to essentially every database with a SQLAlchemy driver, offers
dozens of chart types, and gives fine-grained control over queries, caching, row-level security
and permissions.

Where [Metabase](../metabase/README.md) optimises for people who do not write SQL, Superset optimises
for **analysts who do** — SQL Lab is a first-class part of the product, not an escape hatch.

| Strength | Detail |
|---|---|
| Database coverage | anything with a SQLAlchemy dialect, including Trino and Druid |
| Chart types | far more than the alternatives, including geospatial |
| **Row-level security** | filters applied per role, enforced server-side |
| Caching | configurable, with async query execution for long-running queries |
| Permissions | granular, down to datasets and actions |

## When to use it

- **analysts who write SQL** are the primary audience
- many different data sources need one interface
- row-level security or granular permissions are a requirement
- Apache governance matters

## When not to use it

- business users are the audience — Metabase is markedly easier for them
- you want low operational cost. Superset has more moving parts: a metadata database, a cache, workers for async queries
- dashboards should live in Git — [Evidence](../evidence/README.md)

## Operationally

Not a single binary. A realistic deployment includes a metadata database, Redis for caching and
the Celery broker, and worker processes for async queries and alerts.

That is worth planning for rather than discovering: the difference in operational weight against
Metabase is larger than the feature comparison suggests.

## The pairing worth knowing

Superset over [Trino](../../../data-engineering/query-engine/README.md) is a common and effective
combination for a lakehouse — Trino federates and Superset visualises, with SQL Lab as the
exploration surface. That covers the analyst case without a warehouse in between.

---

[← Visualisation](../README.md)
