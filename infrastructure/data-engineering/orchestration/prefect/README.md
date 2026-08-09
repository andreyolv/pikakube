[← Orchestration](../README.md)

# Prefect

<https://github.com/PrefectHQ/prefect>
<https://github.com/PrefectHQ/prefect-helm/>
<https://docs.prefect.io/>

---

## The problem it solves

Airflow DAGs are declared statically: the structure is known when the file is parsed, and
building it dynamically means generating DAGs, which is awkward and fragile.

Prefect makes pipelines **ordinary Python**. A flow is a function, tasks are functions it
calls, and the graph is whatever the code does at runtime — including loops, conditionals and
task counts that depend on data.

```python
@flow
def process(customers: list[str]):
    for c in customers:          # the graph depends on the input
        result = extract(c)
        transform(result)
```

That is genuinely hard in Airflow and natural here.

## When to use it

- the pipeline shape **depends on data** — a task per file, per customer, per partition
- the team writes Python and wants pipelines to be normal code rather than a framework
- local development and testing matter; flows run as plain functions

## When not to use it

- **backfill by partition** is central. Airflow's date-partitioned model is more mature for reprocessing history
- the ecosystem is the reason for the choice — Airflow's operator library is far larger
- assets and lineage are the model — [Dagster](../dagster/README.md)

## Where it fits best

Workloads that are **event-driven or parameterised** rather than scheduled. "Process this file
that arrived", "run for these twelve customers", "retry the ones that failed" — Prefect
expresses those directly.

For a nightly DAG with date partitions and backfill, Airflow's model fits better, and that is
most of a traditional data platform's work.

## Note on versions

Prefect 2 and 3 differ substantially from Prefect 1, and much of the material online refers to
the older model. Worth checking which version any tutorial assumes before following it.

---

[← Orchestration](../README.md)
