[← Data lineage](../README.md)

# OpenLineage

<https://github.com/OpenLineage/OpenLineage>
<https://github.com/OpenLineage/workshops>

---

## What it is

**A specification**, not a product — the event format that tools emit to describe what a job read
and wrote.

That is the important framing. OpenLineage does not store lineage or display it. It defines the
event, and the integrations that emit it from the systems that already run jobs.

```
RunEvent {
  eventType: START | COMPLETE | FAIL
  job:    { namespace, name }
  run:    { runId }
  inputs:  [ Dataset ]
  outputs: [ Dataset ]
  facets: { schema, columnLineage, dataQuality, ... }
}
```

| Layer | This project provides |
|---|---|
| **Specification** | the event format, and facets that extend it |
| **Integrations** | emitters for Airflow, Spark, dbt, Flink, Trino, Dagster |
| Client libraries | Python and Java, for emitting custom events |
| Storage and UI | **no** — that is [Marquez](../marquez/README.md), DataHub, OpenMetadata |

## Why the specification matters more than any tool

The only property that makes a lineage system worth deploying is **automatic collection** — see
[`../README.md`](../README.md#3-the-only-thing-that-matters-automatic-collection).

OpenLineage is what makes that possible, because the systems that run jobs emit it with
**configuration rather than code**:

| System | How |
|---|---|
| **Airflow** | a provider package plus config — no DAG changes |
| **Spark** | a listener JAR and a few Spark properties |
| **dbt** | `dbt-ol`, wrapping the normal command |
| Flink, Trino, Dagster | comparable integrations |

Nobody writes lineage. It is a by-product of jobs that already run.

The second consequence is portability: because the store consumes a standard, choosing
[Marquez](../marquez/README.md) today and [OpenMetadata](../../platform/open-metadata/README.md)
later is a change of destination rather than a re-instrumentation.

## Facets, and what they add

The extension mechanism, and where the more interesting metadata lives:

| Facet | Carries |
|---|---|
| `schema` | the dataset's columns at the time of the run |
| **`columnLineage`** | which output column derived from which input columns |
| `dataQualityMetrics` | row counts, null counts — quality results attached to the run |
| `sql` | the query that produced the output |
| `dataSource` | where the dataset actually lives |
| `documentation`, `ownership` | description and owner |

**`columnLineage` is the one people ask for**, and its support is uneven — see
[`../README.md`](../README.md#2-table-level-and-column-level). SQL-based sources parse well;
Spark jobs, where the transformation is code rather than a query, generally do not. Verify it for
the specific engines before promising it.

The `dataQualityMetrics` facet is the underrated one: it lets a quality result travel with the
lineage event, so the graph shows not only what produced a dataset but whether that run was
healthy. That connects [`quality/`](../../quality/README.md) to lineage without a second system.

## When to use it

Always, if lineage is wanted at all. There is no competing open standard, and the alternative is a
proprietary format that makes the store impossible to change.

## When not to use it

There is no real case. The decision is not *whether* OpenLineage, it is **where the events go** —
see [`../README.md`](../README.md#5-decision-tree).

## Notes

The [workshops repository](https://github.com/OpenLineage/workshops) is the practical starting
point — worked examples of instrumenting Airflow and Spark, which is more useful than the
specification for getting the first events flowing.

**This is the cheapest governance capability available to this platform, and it is switched off.**

All three emitting systems are already running here:
[Airflow](../../../data-engineering/orchestration/airflow/README.md),
[Spark](../../../data-engineering/processing/spark/README.md) and
[dbt](../../../analytics-engineering/transform/dbt/README.md). None of them requires code changes
— a provider package, a listener JAR, and a command wrapper respectively.

The sequence from [`../README.md`](../README.md#7-how-this-applies-to-pikakube): emit the events,
send them to [Marquez](../marquez/README.md) to prove collection works, and defer the decision
about a full catalogue until there is something in it worth browsing.

---

[← Data lineage](../README.md)
