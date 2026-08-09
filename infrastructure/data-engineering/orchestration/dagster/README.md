[← Orchestration](../README.md)

# Dagster

<https://github.com/dagster-io/dagster>
<https://docs.dagster.io/>

---

## The problem it solves

Task-centric orchestrators answer "did the task run". Consumers ask "is this table fresh and
correct" — a different question, and one Airflow cannot answer without another tool.

Dagster inverts the model: you declare **assets** — the tables, files and models that should
exist — and how to produce them. The dependency graph is derived from the assets, not
maintained separately.

| | Task-centric | Dagster |
|---|---|---|
| You declare | what to run, in what order | **what should exist** |
| Failure means | "this task failed" | "this table is stale" |
| Lineage | a separate tool | **native** — the graph is the assets |
| Backfill | by date, per DAG | by asset partition |
| Testing | difficult | designed for it — assets are functions |

## What follows from the asset model

**Lineage comes free.** The graph already knows that `orders_daily` derives from `orders_raw`.
That overlaps directly with what [`data-governance/`](../../../data-governance/) addresses with
separate tooling.

**Local development is genuinely good.** Assets are ordinary Python functions with typed inputs
and outputs, so they can be run and tested without a scheduler — which is the thing Airflow
makes hardest.

**Freshness is a first-class concept.** "This asset should be no more than two hours old" is
expressible, which connects directly to the SLIs that matter for a data platform — see
[`service-level/`](../../../site-reliability-engineering/service-level/README.md#6-slos-for-a-data-platform).

## When to use it

- **data assets** are the mental model, and lineage matters
- pipelines should be testable, and that is currently painful
- freshness and quality are how the platform is judged, rather than task success
- greenfield, or a genuine willingness to migrate

## When not to use it

- the orchestrator also runs infrastructure, ML and maintenance work — [Airflow](../airflow/README.md) is more general
- the ecosystem is the reason: operators, providers, and people who already know it
- an Airflow estate that works. Migrating is a real project, not a swap

## The honest comparison

Dagster is the better-designed system for a **data platform specifically**. Airflow is the
better-supported system for orchestration **generally**, and that support is worth a great deal.

For this repository the interesting angle is the overlap: asset-centric lineage would replace
capability currently assembled from separate governance tooling — which makes it worth a real
evaluation rather than a mention.

---

[← Orchestration](../README.md)
