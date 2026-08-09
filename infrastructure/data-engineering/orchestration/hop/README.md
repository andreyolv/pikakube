[← Orchestration](../README.md)

# Apache Hop

<https://github.com/apache/hop>
<https://hop.apache.org/>

---

## What it is

Visual data integration — the successor to Pentaho Data Integration (Kettle), rebuilt as an
Apache project.

Pipelines and workflows are designed in a desktop IDE and run on the Hop engine, on Spark, or
on Flink via Beam. The interface is a canvas of steps, which is the Kettle lineage carried
forward.

| Concept | What it is |
|---|---|
| **Pipeline** | data transformation — the equivalent of a Kettle transformation |
| **Workflow** | orchestration of pipelines and other actions |
| Hop GUI | the desktop design environment |
| Runtime | Hop engine, Spark, or Flink |

## When to use it

- **migrating from Pentaho / Kettle**, which is its clearest purpose
- visual ETL is the established working style for the team
- an existing investment in that model, where rebuilding in code is not realistic

## When not to use it

- greenfield ELT — [Airbyte](../../../analytics-engineering/integration/airbyte/README.md) plus [dbt](../../../analytics-engineering/transform/dbt/README.md) is the modern shape, and the logic ends up in Git
- pipelines must be reviewable as code
- Kubernetes-native operation; the design experience is desktop-first

## Why it is mapped here

Two reasons, both honest.

**Pentaho estates are real.** A large amount of production ETL still runs on Kettle, and Hop is
the migration path for it — knowing it exists is more useful than pretending everything is
greenfield.

**The visual-versus-code trade recurs**, and this is its clearest expression. Hop is genuinely
good at what it does. The reason ELT moved to code is not that visual tools cannot transform
data — it is that transformation logic in a canvas is not reviewable, testable or diffable, and
that turned out to matter more than authoring convenience.

Same conclusion as [NiFi](../../../analytics-engineering/integration/nifi/README.md) and
[DolphinScheduler](../dolphinscheduler/README.md), from a different direction.

---

[← Orchestration](../README.md)
