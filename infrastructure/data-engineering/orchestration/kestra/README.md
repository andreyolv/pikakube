[← Orchestration](../README.md)

# Kestra

<https://github.com/kestra-io/kestra>
<https://github.com/kestra-io/helm-charts>
<https://kestra.io/docs>

---

## The problem it solves

Airflow requires Python. That is fine when the platform team writes the pipelines and a problem
when the people who understand the work do not write Python.

Kestra makes flows **declarative YAML**, with tasks that can run anything — a script in any
language, a container, a query, an API call.

```yaml
id: daily_load
namespace: data
tasks:
  - id: extract
    type: io.kestra.plugin.jdbc.postgresql.Query
  - id: transform
    type: io.kestra.plugin.dbt.cli.DbtCLI
```

The pipeline is configuration, which means it is reviewable by people who are not Python
developers and diffable in a way a DAG file is not.

## When to use it

- pipelines should be **configuration**, not code
- the estate is multi-language — the team is not Python-first
- a UI matters for building and observing flows
- event-driven triggers alongside schedules

## When not to use it

- Python **is** the ecosystem, and the value is in its libraries — [Airflow](../airflow/README.md) or [Prefect](../prefect/README.md)
- complex dynamic logic; YAML has a ceiling, and passing it produces unreadable templating
- the operator ecosystem is the reason for the choice

## The trade

Declarative is easier to read and harder to abuse. The ceiling is real: once the flow needs
genuine logic, YAML templating becomes worse than code would have been.

The useful question is whether pipelines are mostly **orchestration** — run this, then that,
with conditions — or mostly **transformation logic**. Kestra fits the first well and the second
badly.

For a data platform that is often the right split anyway: orchestration declared, transformation
in [dbt](../../../analytics-engineering/transform/dbt/README.md) or a
[Spark job](../../processing/spark/README.md).

---

[← Orchestration](../README.md)
