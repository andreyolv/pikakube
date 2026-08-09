[← Data lineage](../README.md)

# Spline

<https://github.com/AbsaOSS/spline>
<https://github.com/AbsaOSS/spline-getting-started>

---

## The problem it solves

**Column-level lineage for Spark**, which is the case that defeats most lineage tooling.

The reason it works is architectural. Generic lineage integrations observe a job's inputs and
outputs. Spline hooks into Spark's **query execution listener** and reads the *logical plan* —
the resolved tree of operations Spark is about to execute.

That plan contains the actual derivation of every output column from its inputs. So Spline does
not infer column lineage, it reads it:

| | Generic OpenLineage integration | Spline |
|---|---|---|
| Source | job inputs and outputs | **the Spark logical plan** |
| Table-level lineage | yes | yes |
| **Column-level, for Spark** | patchy | **yes** |
| Transformations | opaque | the operations are visible |
| Scope | many engines | **Spark only** |

This directly addresses the limitation named in
[`../README.md`](../README.md#2-table-level-and-column-level): column-level lineage is universally
promised and unevenly delivered, and Spark is where it usually fails — because the transformation
is code rather than a query that can be parsed.

## When to use it

- **Spark is the processing engine**, and column-level lineage is a real requirement
- compliance or PII tracing, where "which column did this derive from" must be answerable
- impact analysis at column granularity rather than table granularity
- the transformations are complex enough that reading the code is not a practical answer

## When not to use it

- Spark is not the engine — this is Spark-specific by design
- table-level lineage is sufficient, which for impact analysis it usually is —
  [OpenLineage](../open-lineage/README.md) plus [Marquez](../marquez/README.md) is less to run
- lineage across the whole stack including application databases —
  [Grai](../grai/README.md)
- a governance platform is the actual requirement —
  [`platform/`](../../platform/README.md)

## How it deploys

| Component | Role |
|---|---|
| **Spark agent** | a JAR on the Spark classpath, plus configuration |
| **REST server** | receives the captured plans |
| ArangoDB | stores the lineage graph |
| Web UI | visualises plans and lineage |

The [ArangoDB](../../../databases/nosql/multi-model/arangodb/README.md) dependency is worth
noting: it is a graph database, chosen because lineage is a graph, and it is a stateful system to
operate. For a platform not already running it, that is the main cost of adopting Spline.

Enabling the agent is configuration rather than code — Spark properties and a JAR, the same shape
as the OpenLineage Spark listener.

## Spline or OpenLineage

Not mutually exclusive, and the choice depends on what is actually needed:

| | OpenLineage + Marquez | Spline |
|---|---|---|
| Engines | Airflow, Spark, dbt, Flink, Trino | **Spark only** |
| Granularity | table; column where supported | **column, reliably, for Spark** |
| Storage | PostgreSQL | ArangoDB |
| Standard | **an open specification** | its own model |
| Portability | the store is replaceable | tied to Spline |

**Start with OpenLineage.** It covers the whole pipeline, it is a standard, and table-level
lineage answers the question most often asked.

**Add Spline** if column-level lineage for Spark turns out to be a hard requirement — compliance
being the usual reason — and accept the additional store.

Note that Spline has an OpenLineage-compatible path, which reduces the either/or nature of this
somewhat and is worth checking against current versions.

## Notes

From [ABSA OSS](https://github.com/AbsaOSS), a South African banking group — which shows in what
it prioritises: column-level traceability, of the kind a regulator asks about.

The [getting-started repository](https://github.com/AbsaOSS/spline-getting-started) is the
practical entry point.

For this platform, [Spark is genuinely deployed](../../../data-engineering/processing/spark/README.md)
— the Kubernetes operator, the history server and the performance tooling are all mapped. That
makes Spline the relevant answer *if* column-level lineage becomes a requirement.

It is not the first step. The sequence in
[`../README.md`](../README.md#7-how-this-applies-to-pikakube) is OpenLineage into Marquez, which
requires no new stateful system and answers the impact-analysis question. Spline is what to reach
for when "which column did this come from" stops being a nice-to-have.

---

[← Data lineage](../README.md)
