[← Version control](../README.md)

# Project Nessie

<https://github.com/projectnessie/nessie>

---

## The problem it solves

A **versioned catalog**: branches, tags, commits and merges applied to the catalog itself, so a
branch spans **every table in it** and a merge is atomic across all of them.

That is the gap the other two options leave.
[Iceberg branching](../iceberg/README.md) is per table — five tables branched in one pipeline run
are five independent merges, and a failure between the second and the third leaves the warehouse in
a state no query expects. [lakeFS](../lakefs/README.md) solves it by versioning the whole bucket,
which means adding a service to the data path.

Nessie takes the third route: **the catalog is the thing that gets versioned.** Since the catalog is
already what tells engines which table is where, versioning it makes "the set of tables as of commit
X" a first-class concept.

| | [Iceberg branching](../iceberg/README.md) | Nessie | [lakeFS](../lakefs/README.md) |
|---|---|---|---|
| Scope | one table | **a catalog of tables** | the whole bucket |
| Multi-table atomic merge | no | **yes** | yes |
| Non-table files | no | no | **yes** |
| Extra component | **none** | a catalog — which you needed anyway | a service in the data path |
| In the read path | no | metadata only | **yes, every byte** |

**The fourth row is the argument for it.** Iceberg requires a catalog regardless — see
[`metadata-catalog/`](../../../metadata-catalog/README.md), and
[`table-formats/iceberg/`](../../table-formats/iceberg/README.md) is explicit that this is a
production dependency of every query, not an optional convenience. Nessie is a catalog. Choosing it
therefore adds versioning without adding a component, which is a materially different proposition
from adding a layer in front of storage.

Its own metadata is stored in a version store — the deployment here uses PostgreSQL over JDBC — and
it exposes a Git-like model over it: named references, commits, merge and transplant.

## When to use it

- one pipeline run updates **several tables** that must be consistent together
- a catalog is being chosen anyway and versioning is wanted — this is the cheapest moment to get it
- multi-table experimentation: branch the catalog, run the whole pipeline, compare, merge or discard
- reproducibility across a set of tables rather than one, via a tag on the catalog

## When not to use it

- **one table per pipeline run** — [Iceberg branching](../iceberg/README.md) is free and needs
  nothing deployed; this is the common case and it should be exhausted first
- non-table content is in scope — raw landing files, models, artefacts — that is
  [lakeFS](../lakefs/README.md)
- a catalog is already chosen and working, and multi-table atomicity is not an actual requirement;
  replacing a catalog is not a small change
- the engines in use do not support the Nessie catalog well — verify the specific engine and
  version, which is the standing caveat across
  [`table-formats/`](../../table-formats/README.md)
- as a backup; branches and tags are metadata, and none of it survives a deleted bucket

## The catalog decision comes first

Worth being blunt about, because Nessie is easy to evaluate in the wrong frame. It is not a
versioning feature bolted onto a platform — **it is a catalog**, and adopting it is a catalog
decision with versioning as a consequence.

That means it competes with the options in
[`metadata-catalog/`](../../../metadata-catalog/README.md) on catalog terms first: engine support,
REST catalog compatibility, authentication, availability, and who operates the database behind it.
Versioning is the differentiator only once those are acceptable.

## Notes

Recorded from working with it:

- Integration with **AWS S3 / MinIO**
- Integration with **Iceberg**

Both are the right two things to record, and the second is the more meaningful. Nessie's versioning
model rests on Iceberg's snapshot mechanism — a commit references table metadata pointers — so
"integration with Iceberg" is not one integration among several, it is the substance of what the
product does. Iceberg is also the recorded default across
[`lakehouse/`](../../README.md), which puts these two on the same side of the platform's main
decision.

The S3/MinIO note lands in the same place as everywhere else in this folder: the recurring finding
is that **the format is easy and the storage integration is where the time goes**, so an
S3-compatible integration that has been exercised is worth more than a feature list. Note that
[lakeFS](../lakefs/README.md) records its equivalent as **done** while this one is recorded as
attempted — a real difference in confidence between the two pages.

### What is in this folder

| | Content |
|---|---|
| `helm/` | Flux `HelmRelease` for chart `0.81.0` from `charts.projectnessie.org`, plus the `HelmRepository` |
| `postgres/` | Deployment, PVC, Service and secret for the version store |
| `nessie.py` | a PySpark session configured against Nessie, Iceberg and MinIO |

The Helm values set `versionStoreType: JDBC` against PostgreSQL, with credentials from a Kubernetes
secret. **The version store is the thing to think about operationally**: it holds every commit,
branch and tag, so it is a stateful dependency of the catalog, and the catalog is a dependency of
every query. Backing it up is not optional.

`nessie.py` is the useful artefact, because it shows what a client actually needs — and how many
pieces have to agree:

```python
.config("spark.sql.catalog.owshq", "org.apache.iceberg.spark.SparkCatalog")
.config("spark.sql.catalog.owshq.catalog-impl", "org.apache.iceberg.nessie.NessieCatalog")
.config("spark.sql.catalog.owshq.uri", "http://<nessie>:19120/api/v1")
.config("spark.sql.catalog.owshq.ref", "main")
.config("spark.sql.catalog.owshq.warehouse", "s3a://lakehouse/production/iceberg/")
```

Three things are visible in that:

**`ref` is the branch.** A Spark session is pinned to a reference, so pointing a job at a branch is
a configuration change rather than a code change — which is what makes write-audit-publish
practical across a whole pipeline rather than per statement.

**The warehouse is still object storage.** Nessie versions the catalog; the data files live in
MinIO exactly as before, alongside the `fs.s3a` settings the same session configures.

**The Spark extensions line is the trap.** The file sets `spark.sql.extensions` twice — once for
Iceberg's extensions and once for Nessie's — and the second call **overwrites the first** rather
than adding to it. Both belong in a single comma-separated value. It is also version-coupled: the
Nessie extension class in that file names a specific Spark version, which is the same
version-alignment problem the
[MinIO client notes](../../storage/minio/README.md) describe for `hadoop-aws`, and the reason
"verify the specific engine and version" keeps appearing in this repository.

The endpoints and keys in the file are from an external tutorial environment — public IPs and
`minio`/`minio123` — not from this platform. It is reference material, not a deployment.

### Where it fits here

[`../README.md`](../README.md) records the sequence, and Nessie is step four: adopt it **only if a
pipeline run must update several tables atomically.** Until that is true, Iceberg branching on
[MinIO](../../storage/minio/README.md) covers the case for nothing, and a catalog swap is a large
change to make for a requirement nobody has yet.

---

[← Version control](../README.md)
