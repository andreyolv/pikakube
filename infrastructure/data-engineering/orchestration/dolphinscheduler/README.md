[← Orchestration](../README.md)

# Apache DolphinScheduler

<https://github.com/apache/dolphinscheduler>
<https://dolphinscheduler.apache.org/>

---

## What it is

A distributed workflow scheduler with a **visual DAG editor**: pipelines are drawn in a UI
rather than written in code, with a decentralised, HA-oriented architecture underneath.

Apache project, widely used in China, and built around a different assumption from Airflow —
that the people defining workflows are not necessarily engineers.

| Feature | Detail |
|---|---|
| **Visual editor** | drag-and-drop DAG construction |
| Task types | shell, SQL, Spark, Flink, Python, HTTP, and more |
| **Decentralised HA** | no single scheduler to be a bottleneck or a failure point |
| Multi-tenancy | tenants, queues and resource isolation built in |
| Versioning | workflow versions with rollback |

The HA architecture is a genuine differentiator. Airflow's scheduler has historically been the
constraint, and this was designed without a central one.

## When to use it

- a **visual editor** is a requirement, because the authors are not writing Python
- multi-tenancy with resource isolation between teams matters
- scheduler high availability is a hard requirement
- the estate is Apache-ecosystem-oriented

## When not to use it

- pipelines should be **code**, reviewed in pull requests — which is the dominant expectation now, and where [Airflow](../airflow/README.md), [Dagster](../dagster/README.md) and [Prefect](../prefect/README.md) sit
- the operator ecosystem is the reason for the choice
- documentation and community outside China are thinner, which matters when something breaks

## The trade at the centre of it

A visual editor lowers the barrier and raises the cost of everything else: workflows are harder
to review, harder to diff, harder to test, and harder to generate.

That is the same tension as [NiFi](../../../analytics-engineering/integration/nifi/README.md) and
[Hop](../hop/README.md) — visual tools are genuinely more accessible, and the artefact they produce is
not code.

Worth choosing deliberately rather than by preference: if pipelines must be reviewable in Git,
this is the wrong shape regardless of its other merits.

---

[← Orchestration](../README.md)
