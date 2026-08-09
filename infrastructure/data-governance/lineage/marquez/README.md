[← Data lineage](../README.md)

# Marquez

<https://github.com/MarquezProject/marquez>

---

## What it is

The **reference implementation** of [OpenLineage](../open-lineage/README.md): a service that
receives lineage events, builds the graph, and displays it.

It came from the same origin as the specification, so it implements it fully and first — which
makes it the natural place to send events when the goal is to prove collection works.

| Component | Role |
|---|---|
| **API** | receives OpenLineage events over HTTP |
| PostgreSQL | stores the graph |
| **Web UI** | datasets, jobs, runs, and the lineage between them |
| Run history | every execution, with inputs, outputs and status |

## When to use it

- **proving the collection works** — the smallest thing that turns events into a visible graph
- lineage is the requirement, without a full catalogue's surface area
- a dedicated lineage store, kept separate from a governance platform
- learning the model, before deciding where lineage should ultimately live

## When not to use it

- a **catalogue** is the actual requirement — search, ownership, glossary, classification. That is
  [`platform/`](../../platform/README.md), and both OpenMetadata and DataHub ingest the same
  OpenLineage events
- lineage across **application databases**, beyond the pipeline —
  [Grai](../grai/README.md)
- column-level lineage for Spark specifically — [Spline](../spline/README.md) reads the execution
  plan and gets further

## Notes

Recorded from evaluating it:

> Input is via **API only** —
> [MarquezProject/marquez#2642](https://github.com/MarquezProject/marquez/issues/2642)

Worth understanding rather than filing as a complaint, because it cuts both ways.

Marquez accepts lineage **only** as OpenLineage events posted to its API. There is no ingestion
that goes and reads a warehouse's metadata, no connector catalogue, and no way to seed the graph
from an existing system.

| Consequence | Detail |
|---|---|
| **Emitters must be configured** | nothing appears until Airflow, Spark or dbt are emitting |
| No backfill from existing systems | the graph starts empty and fills forward |
| No connectors | it does not crawl a database to discover datasets |
| **Purity** | everything in the graph came from a real run — nothing is inferred or stale |

The last row is the upside, and it is genuine: every edge in a Marquez graph corresponds to a job
that actually executed. Catalogues that crawl metadata show datasets that may no longer be
produced by anything.

The practical implication for adoption: **Marquez is a destination, not a discovery tool.** It is
the right first store precisely because it forces the emitters to be set up — which is the part
that matters and the part most easily deferred.

## Where it fits here

The recommended first step for this platform, from
[`../README.md`](../README.md#7-how-this-applies-to-pikakube):

1. Configure [OpenLineage](../open-lineage/README.md) emitters in
   [Airflow](../../../data-engineering/orchestration/airflow/README.md),
   [Spark](../../../data-engineering/processing/spark/README.md) and
   [dbt](../../../analytics-engineering/transform/dbt/README.md)
2. **Point them at Marquez** — one service and a PostgreSQL database
3. Confirm the graph reflects reality
4. Decide about a full catalogue later, with the events already flowing

Step 3 is the one that has value on its own. A lineage graph built from real runs answers *"what
breaks if I change this table?"* immediately, and that is the question this discipline exists for.

If [OpenMetadata](../../platform/open-metadata/README.md) is adopted afterwards, it consumes the
same events — so this is a starting point rather than a commitment.

The PostgreSQL dependency is small here:
[CloudNativePG](../../../databases/sql/postgresql/operator/cnpg/README.md) already runs in this
cluster, so Marquez adds a service rather than a stateful system.

---

[← Data lineage](../README.md)
