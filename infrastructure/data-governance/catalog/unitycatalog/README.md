[← Data catalogs](../README.md)

# Unity Catalog

<https://github.com/unitycatalog/unitycatalog>

<https://github.com/unitycatalog/unitycatalog-python>

---

## The problem it solves

Databricks' catalog, open-sourced and donated to the Linux Foundation. It is the one entry in this
folder that deliberately sits **on both sides of the "catalog" split** that runs through this
discipline:

| Role | What it does |
|---|---|
| **Technical catalog** | engines resolve tables through it — it speaks the **Iceberg REST catalog** API as well as its own |
| **Governance layer** | three-level namespace (catalog → schema → table), grants, lineage, tags |
| **Beyond tables** | volumes (files), functions, and registered ML models as first-class objects |
| **Credential vending** | temporary, scoped storage credentials issued to engines |
| Formats | Delta and Iceberg, plus Parquet and others as external tables |

That combination is the ambition: one system that both Spark asks *"where is this table"* and a
human asks *"who owns this and may I read it"*. Nothing else in this repository tries to be both —
[`metadata-catalog/`](../../metadata-catalog/README.md) is infrastructure in the query path and
[`platform/`](../../platform/README.md) is a product beside it.

The model extending past tables is the other genuinely distinctive part. Volumes and models being
catalog objects means the same grants cover a directory of files and a registered model, which is
where governance usually falls apart — everything that is not a table ends up ungoverned.

## When to use it

- **Databricks is in the picture.** The open-source server is the same model as the managed one,
  so the concepts, the three-level namespace and the grants transfer
- **Delta is the table format** and a catalog is needed that treats it as a first-class citizen —
  see [`lakehouse/table-formats/delta/`](../../lakehouse/table-formats/delta/README.md)
- files and ML models need to be governed alongside tables, under the same grants
- the goal is one catalog for engines **and** people, and the packaging cost below is acceptable

## When not to use it

- the requirement is only an **Iceberg REST catalog** — the dedicated implementations are further
  along: [Lakekeeper](../../metadata-catalog/iceberg/lakekeeper/README.md),
  [Polaris](../../metadata-catalog/iceberg/polaris/README.md)
- the requirement is only a **data catalogue for people** — search, glossary, ownership,
  connectors. That is [OpenMetadata](../../platform/open-metadata/README.md), which is far more
  complete on the human-facing side
- it has to be **deployed reliably by GitOps today** — see the note below
- automatic lineage is expected to arrive on its own; the discussion below shows that is still
  being designed

## Notes

Recorded from evaluating it here:

> No official Helm chart yet —
> [unitycatalog/unitycatalog#433](https://github.com/unitycatalog/unitycatalog/issues/433)
>
> Supporting OpenLineage in Unity Catalog —
> [unitycatalog/unitycatalog#244](https://github.com/unitycatalog/unitycatalog/discussions/244)

### No official Helm chart

Issue 433 is a request for an official chart, and the state it describes is visible in the
manifests here. [`helm/gitrepository.yaml`](helm/gitrepository.yaml) points Flux at the project's
**Git repository** at tag `v0.3.0`, with an `ignore` block excluding everything except `/helm`,
and [`helm/helmrelease.yaml`](helm/helmrelease.yaml) builds from that directory in the source
tree.

That works, and it is worth being clear about what it costs:

| Consequence | Detail |
|---|---|
| The chart is **unreleased** | it is a directory in a source tree, versioned with the application |
| No chart versioning | the tag pins the repository, not a chart artefact with its own lifecycle |
| No index, no registry | it cannot be mirrored, and the chart is not signed or digest-pinned |
| A Git dependency in the deploy path | Flux clones GitHub to reconcile |
| **In-tree charts change without notice** | there is no compatibility contract for values between tags |

The version tells the story: **v0.3.0.** This is early software, and the missing chart is a symptom
rather than the problem. Compare the recorded findings on the
[Iceberg REST catalogs](../../metadata-catalog/iceberg/README.md), where the identical complaint
appears against all three implementations — packaging maturity is the deciding factor across this
whole area, and Unity Catalog is behind even those.

### OpenLineage support

Discussion 244 is a **design discussion, not a feature.** That distinction matters when reading
Unity Catalog's positioning, because "lineage" appears in the description of what it does.

[OpenLineage](../../lineage/open-lineage/README.md) is the standard for lineage events, and the
tools this platform runs —
[Airflow](../../../data-engineering/orchestration/airflow/README.md),
[Spark](../../../data-engineering/processing/spark/README.md),
[dbt](../../../analytics-engineering/transform/dbt/README.md) — emit it with configuration rather
than code. A catalog that ingests OpenLineage gets lineage from work already done elsewhere; a
catalog that does not needs its own integration with every engine.

Databricks' *managed* Unity Catalog derives lineage by capturing query plans in its own runtime.
Outside Databricks there is no such runtime, which is exactly why the discussion exists. Read it as
the honest signal: **automatic lineage is a property of the managed product, not of the
open-source server** — for now.

That is the one capability to check before believing the both-catalogs pitch. It is also why
[`../../lineage/README.md`](../../lineage/README.md) matters independently of whatever catalog is
eventually chosen: emitters first, destination second.

### `unitycatalog-python`

The second repository is the Python client, which is how a notebook or a pipeline talks to the
catalog without going through Spark. Worth knowing exists — it is the practical route for
[DuckDB](../../../data-engineering/processing/duckdb/README.md) and pandas workloads that want the
catalog's table registry without a JVM.

### Where it lands

Track it, do not adopt it. The design is the most interesting in this folder and the ambition —
one catalog for engines and people — is the right one. But [`../README.md`](../README.md#how-this-applies-to-pikakube)
puts it plainly: at v0.3.0 with no released chart, this is a project to watch rather than to put in
the query path.

---

[← Data catalogs](../README.md)
