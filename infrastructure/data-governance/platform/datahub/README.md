[← Governance platforms](../README.md)

# DataHub

<https://github.com/datahub-project/datahub>
<https://github.com/acryldata/datahub-helm>

---

## What it is

LinkedIn's metadata platform, and the one with the **largest connector catalogue** and the most
active community in this category.

Its architecture is genuinely well designed: a metadata model built on entities and aspects, an
event-sourced change log, and ingestion as a pluggable framework. Conceptually it is the most
extensible option here.

| Capability | Detail |
|---|---|
| **Connectors** | the widest catalogue — most warehouses, BI tools, orchestrators and streams |
| Metadata model | entities and aspects, extensible without forking |
| **Event-sourced** | every metadata change is an event, so downstream consumers can react |
| Lineage | ingested from connectors and from [OpenLineage](../../lineage/open-lineage/README.md) |
| Discovery | search, browse, ownership, tags, glossary |
| Column-level lineage | **for some sources** — see the notes |

## When to use it

- the **connector catalogue** is the deciding factor, and the specific sources are supported well
- the metadata model's extensibility matters — custom entity types
- the event stream is useful: reacting to metadata changes programmatically
- there is capacity to operate a large distributed application

## When not to use it

- **the Helm chart is a blocker** — see the notes; this is not a hypothetical
- discovery and lineage are the whole requirement —
  [OpenDataDiscovery](../opendatadiscovery/README.md)
- quality and catalogue should be one product —
  [OpenMetadata](../open-metadata/README.md) integrates them
- column-level lineage **for Spark** is the reason for adopting it — it is not there
- the operational footprint is a concern: Kafka, Elasticsearch, a relational store and several
  services

## Notes

Recorded from actually trying to deploy and use it, and the findings are blunt:

> Full of bugs.
>
> Ran the Jupyter notebook but could not see anything in the DataHub UI.
>
> The Helm chart is terrible, it never works —
> [acryldata/datahub-helm#347](https://github.com/acryldata/datahub-helm/issues/347)
>
> Column-level lineage is available for Snowflake and Looker, **not Spark**. :(
>
> Create a token at `http://127.0.0.1:9002/settings/tokens`; log into the UI as admin.
>
> Spark lineage reference:
> <https://datahubproject.io/docs/metadata-integration/java/spark-lineage-beta>

Three of those deserve to be read as findings rather than complaints.

**The chart.** DataHub is a large distributed application — Kafka, Elasticsearch, a relational
store, a GMS service, a frontend and several ingestion components. A chart that does not reliably
install it is not a detail; it is the difference between an afternoon and a fortnight. For a
GitOps repository where deployment *is* the mechanism, a broken chart is close to disqualifying.

**Lineage submitted but not visible.** The Spark integration ran and nothing appeared in the UI.
That is the worst class of failure for a metadata platform, because there is no error to
investigate — events are accepted and the graph stays empty, so the debugging surface is the whole
pipeline.

**Column-level lineage for Snowflake and Looker, not Spark.** This is exactly the gap that
[`lineage/`](../../lineage/README.md#2-table-level-and-column-level) warns about in the abstract,
found concretely: column-level lineage is universally promised and unevenly delivered, and Spark —
where the transformation is code rather than a parseable query — is where it usually fails.

For a platform whose processing is [Spark](../../../data-engineering/processing/spark/README.md),
that removes the main reason to prefer DataHub for lineage. The tool that does reach column level
for Spark is [Spline](../../lineage/spline/README.md), by reading the execution plan.

## The verdict for this platform

Not the recommendation, and the reasoning is comparative:
[OpenMetadata](../open-metadata/README.md) installed and this did not.

That is not a judgement about which is better designed — DataHub's metadata model is arguably the
stronger one. It is a judgement about which can be operated here, and for a large distributed
application that question comes first.

Worth revisiting if the chart situation improves, or if the connector catalogue turns out to cover
a source nothing else does.

---

[← Governance platforms](../README.md)
