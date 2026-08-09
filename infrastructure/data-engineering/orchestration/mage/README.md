[← Orchestration](../README.md)

# Mage

<https://github.com/mage-ai/mage-ai>
<https://github.com/mage-ai/helm-charts>

---

## What it is

Pipeline authoring in a **notebook-like interface**: blocks of Python or SQL, each with a
preview of its output, composed into a pipeline that runs on a schedule.

The positioning is explicit — Airflow for people who found Airflow too much. The gap between
"exploring in a notebook" and "having a scheduled pipeline" is the friction it targets.

| Feature | Detail |
|---|---|
| Block-based | each step is a block, with typed inputs and outputs |
| **Preview per block** | see the data at each step while building |
| Python and SQL together | in the same pipeline |
| Built-in charts | inspect data without leaving the tool |
| Scheduling and backfill | included |

## When to use it

- **analysts and analytics engineers** build the pipelines, not platform engineers
- fast iteration matters more than operational depth
- small teams, where Airflow's footprint is disproportionate

## When not to use it

- a platform with strict operational requirements — Airflow's maturity, ecosystem and community are the reason it dominates
- the orchestrator must handle more than data pipelines
- the notebook-style interface encourages logic that should live in [dbt](../../../analytics-engineering/transform/dbt/README.md)

## The risk worth naming

It is the [notebook problem](../../../analytics-engineering/notebook/README.md#2-the-problem-with-notebooks-in-production)
one level up: an interface that makes exploration easy makes it easy for exploration to
**become** the pipeline.

That is fine when the pipeline is small and owned by the person who wrote it. It stops being
fine when it is load-bearing and the author has left — the same reason notebooks do not belong
in production.

Used deliberately — for genuinely small pipelines, with real transformation in dbt — it removes
real friction. Used as the default, it accumulates logic nobody can review.

---

[← Orchestration](../README.md)
