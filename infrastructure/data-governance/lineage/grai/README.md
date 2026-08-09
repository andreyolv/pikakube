[← Data lineage](../README.md)

# Grai

<https://github.com/grai-io/grai-core>
<https://github.com/grai-io/grai-helm>

---

## The problem it solves

Lineage that starts at the **application database**, not at the warehouse — and a **CI check** that
fails a pull request when a schema change would break something downstream.

Both of those are gaps in the conventional approach.

[OpenLineage](../open-lineage/README.md) instruments the pipeline: Airflow, Spark, dbt. That
graph begins where data is *ingested*. What produced the source table — a migration in an
application repository — is outside it.

Which means the most common breaking change is invisible to lineage: **a developer renames a
column in the application's schema**, their tests pass, and the pipeline reading it breaks after
the deploy.

| | Pipeline lineage | Grai |
|---|---|---|
| Starts at | ingestion | **the application database** |
| Built from | run events | connectors reading schemas, plus pipeline metadata |
| Used during | incidents, impact analysis | **pull requests** |
| Prevents breakage | no — it explains it afterwards | **yes, before merge** |

## The CI integration is the point

Grai's distinguishing feature is running as a check on a pull request:

```
This PR drops `orders.legacy_status`.
Downstream: dbt model `fct_orders`, dashboard `Revenue by status`.
```

That turns lineage from a diagnostic tool into a **preventive control** — and it puts the warning
where it is actionable, in front of the person making the change, before it merges.

That is the same shift that [`contract/`](../../contract/README.md) makes for data quality: move
the check from the consumer, where the problem is discovered, to the producer, where it is caused.

| Capability | Detail |
|---|---|
| **Connectors** | PostgreSQL, MySQL, Snowflake, BigQuery, dbt, Fivetran, Airflow, and more |
| **Whole-stack graph** | application databases through to dashboards |
| **CI checks** | GitHub Actions integration on pull requests |
| Column-level | where the connector supports it |
| Web UI | for browsing the graph |
| Open source | with a hosted option |

## When to use it

- **schema changes in application repositories keep breaking pipelines** — the specific problem
- lineage should cover application databases, not just the pipeline
- a preventive check is wanted rather than a diagnostic graph
- the estate is heterogeneous enough that connectors beat instrumentation

## When not to use it

- pipeline lineage is sufficient — [OpenLineage](../open-lineage/README.md) plus
  [Marquez](../marquez/README.md) is a standard and less to run
- column-level lineage for **Spark** is the requirement —
  [Spline](../spline/README.md)
- a full governance platform — [`platform/`](../../platform/README.md)
- application repositories are outside the platform team's reach, so no CI check can be added

## The trade against OpenLineage

Worth being explicit, because they are built on different assumptions:

| | OpenLineage | Grai |
|---|---|---|
| Model | **push** — systems emit events | **pull** — connectors read metadata |
| Accuracy | what actually ran | what the schemas say |
| Standard | **an open specification** | its own model |
| Store portability | replaceable | tied to Grai |
| Coverage | instrumented systems only | anything with a connector |
| Prevention | no | **yes, via CI** |

The push/pull distinction has a real consequence. OpenLineage records **runs that happened**, so
the graph reflects reality. Grai reads **schemas and definitions**, so it can describe a
relationship that exists on paper and is no longer exercised.

Neither is wrong. They answer *"what actually ran"* and *"what is connected to what"*, which are
different questions.

## Notes

Mapped with its [Helm chart](https://github.com/grai-io/grai-helm).

For this platform the recommendation remains [OpenLineage](../open-lineage/README.md) first — it
is a standard, the emitters cost configuration rather than code, and the store stays replaceable.

Grai is worth revisiting for the problem it uniquely addresses, which
[`../README.md`](../README.md#6-anti-patterns) names as an anti-pattern of the conventional
approach: *lineage only for the warehouse, when the pipeline that populates it is where breakage
originates.*

The scenario it prevents is the one this repository is otherwise exposed to — a schema change in a
[source database](../../../databases/sql/mysql/README.md) breaking a downstream model, with the
lineage graph starting too late to have warned anyone.

---

[← Data lineage](../README.md)
