[← Version control](../README.md)

# lakeFS

<https://github.com/treeverse/lakeFS>
<https://github.com/treeverse/charts>

---

## The problem it solves

Git semantics over **object storage itself** — branch, commit, diff, merge and revert, applied to a
bucket rather than to a table.

The other two options in this folder version things a table format understands.
[Iceberg branching](../iceberg/README.md) versions one table; [Nessie](../nessie/README.md) versions
a catalog of tables. lakeFS versions **everything in the bucket**, including the large fraction of a
data platform that is not a table:

| Content | Iceberg branching | Nessie | lakeFS |
|---|---|---|---|
| One Iceberg table | **yes** | yes | yes |
| Many tables, atomically | no | **yes** | **yes** |
| Delta, Hudi, Paimon tables | no | Iceberg, Delta | **yes** |
| Raw CSV and JSON landing data | no | no | **yes** |
| Parquet files that are not a table | no | no | **yes** |
| ML models, images, artefacts | no | no | **yes** |

The mechanism is a **metadata layer in front of object storage**. lakeFS exposes an S3-compatible
endpoint; clients address `s3://<repo>/<branch>/<path>` and lakeFS resolves that to the real objects
in the underlying bucket. Because objects are immutable and lakeFS tracks which version of each path
belongs to which commit, **branching copies nothing** — it is a metadata operation, the same as it
is in Git.

That design is what makes it work on data of any size, and it is also the source of its one real
cost: **it sits in the data path.** Every read and every write passes through it.

## When to use it

- the thing to version is **not only tables** — raw landing zones, feature files, models, images
- more than one format is in play, or the format is "files"
- a pipeline run touches several datasets and they must be consistent together
- reproducibility across an entire dataset, not a single table, is the requirement
- the S3-compatible interface means existing jobs need only an endpoint change, which is a genuinely
  low-friction way in

## When not to use it

- **a single Iceberg table** — [Iceberg branching](../iceberg/README.md) does it free, with nothing
  in the data path; [`../README.md`](../README.md) lists this as an anti-pattern by name
- tables only, with atomicity across them — [Nessie](../nessie/README.md) is a catalog rather than a
  layer, so it replaces a component instead of adding one
- there is no appetite for a **stateful service on the critical path of every read**, backed by a
  database that must be operated and backed up
- as a backup; commits are metadata over the same bucket, and none of it survives that bucket being
  deleted

## What it costs

| Concern | Detail |
|---|---|
| **In the data path** | if lakeFS is down, the data is unreachable through it — the objects exist, but the paths clients use do not resolve |
| **A database** | metadata lives in PostgreSQL; it must be backed up, and it is a second stateful component |
| Credential indirection | clients authenticate to lakeFS, which holds the storage credentials — better security-wise, one more thing to rotate |
| Path rewriting | every job's paths gain a branch component; migration is mechanical but it is not zero |
| Uncommitted data | writes are invisible to other branches until committed, which is the feature and also a surprise |
| Garbage collection | deleted branches and old commits need reclaiming, or the underlying bucket grows |

## Notes

**The most hands-on work recorded in this folder**, and the state is recorded plainly:

> **DONE** — integration with AWS S3 / MinIO

That is a stronger claim than the rest of [`lakehouse/`](../../README.md) carries. Given the
recurring finding across the table-format notes — *the format is easy, and the S3 integration is
where the time goes* — a storage integration marked done is the note worth trusting most in the
whole folder.

### Reference material recorded

Upstream:

- [treeverse/lakeFS](https://github.com/treeverse/lakeFS)
- [treeverse/charts](https://github.com/treeverse/charts) — the Helm charts, which is what the
  deployment here uses

Sample notebooks from `lakeFS-samples`, which are the material this work was built from:

- [spark-demo.ipynb](https://github.com/treeverse/lakeFS-samples/blob/main/00_notebooks/spark-demo.ipynb)
  — Spark reading and writing through the lakeFS S3 gateway
- [delta-lake.ipynb](https://github.com/treeverse/lakeFS-samples/blob/main/00_notebooks/delta-lake.ipynb)
  — Delta tables on branches, via Spark
- [delta-lake-python.ipynb](https://github.com/treeverse/lakeFS-samples/blob/main/00_notebooks/delta-lake-python.ipynb)
  — the same **without Spark**, using `deltalake` (delta-rs)
- [delta-diff.ipynb](https://github.com/treeverse/lakeFS-samples/blob/main/00_notebooks/delta-diff.ipynb)
  — **diffing a Delta table between two branches**

The last one is the one to look at first. Diffing a *table* across branches is a different thing
from diffing files: it answers "what rows changed on this branch" rather than "which objects
differ", which is what makes a merge reviewable rather than merely atomic.

Client library:

- [`lakefs-client` on PyPI](https://pypi.org/project/lakefs-client/) — used in the notebooks here to
  create repositories and commit programmatically

Spark integration:

```python
.config("spark.jars.packages", "io.lakefs:lakefs-spark-client_2.12:0.12.0")
```

- [io.lakefs:lakefs-spark-client on mvnrepository](https://mvnrepository.com/artifact/io.lakefs/lakefs-spark-client)

**Two different Spark integration paths exist, and the difference matters.** The plain S3A route —
point `fs.s3a.endpoint` at the lakeFS gateway and use `s3a://repo/branch/path` — is the one the
notebooks in `example/` use, and it needs no lakeFS jar at all. The
`lakefs-spark-client` package above is the separate, richer client: it reads lakeFS metadata
directly rather than going through the gateway, which is what garbage collection and bulk metadata
operations need. Note the `_2.12` suffix — it is a **Scala version** in the artefact name, so it
must match the Spark build, and this is the same version-alignment trap the
[MinIO client notes](../../storage/minio/README.md) describe for `hadoop-aws`.

### What is in this folder

| | Content |
|---|---|
| `helm/` | Flux `HelmRelease` for chart `1.0.12` from `charts.lakefs.io`, plus the `HelmRepository` |
| `postgres/` | the PostgreSQL StatefulSet and secret backing lakeFS metadata |
| `example/` | two working notebooks, `CUSTOMER.csv` and `userdata1.parquet` as their input |

The Helm values are the record of the integration that is marked done: `blockstore.type: s3` with
`force_path_style: true`, `discover_bucket_region: false`, and the endpoint pointed at
`minio.minio.svc.cluster.local:9000`, with the storage credentials injected from a Kubernetes
secret rather than written into the values.

Those three settings are exactly the ones a self-hosted S3 backend needs and the ones whose absence
produces confusing failures. `force_path_style` in particular is the same trap documented in
[`storage/minio/`](../../storage/minio/README.md): without it the client treats the bucket name as a
hostname, and the error blames DNS.

### The two example notebooks

**`lakefs-lake-python.ipynb`** — no Spark at all. It creates a repository with `lakefs_client`, then
uses `deltalake` (delta-rs) to write and append a Delta table at `s3a://<repo>/main/userdata/`,
reads back `history()` and `version()`, and commits through the lakeFS API. The storage options
matter: `AWS_ENDPOINT` points at lakeFS rather than at MinIO, and `AWS_ALLOW_HTTP` and
`AWS_S3_ALLOW_UNSAFE_RENAME` are set.

That combination — **lakeFS plus delta-rs, versioning a real Delta table from a plain Python
process** — is the most interesting result recorded here. It removes both the cluster and the JVM
from a workflow that normally assumes Spark, which is the same argument
[`table-formats/delta/`](../../table-formats/delta/README.md) makes for `delta-rs` in general.

**`lakefs-lake-spark.ipynb`** — the Spark route: `hadoop-aws` and `delta-core` packages, `fs.s3a`
pointed at the lakeFS endpoint, then customers and orders tables written as Delta on a `main` branch
and an ETL branch, with helper functions to **compare row counts across branches** and to print the
diff between two refs. That is write-audit-publish in its concrete form — the comparison between
branches is the audit step, expressed as ordinary code.

Note that the notebooks pin repository storage namespaces at `s3://lakehouse/...` and
`s3://mlflow/...` — existing MinIO buckets, which is the detail confirming this ran against the real
platform rather than a sandbox.

### Where it fits here

[`../README.md`](../README.md) records the honest position: the lakehouse substrate here is
**Iceberg on [MinIO](../../storage/minio/README.md)**, which makes Iceberg branching the free
starting point for single-table pipelines and puts lakeFS in the wrong weight class for that job.

lakeFS earns its place when the scope is wider than tables — landing zones, models, artefacts — and
it is the option here with the deepest recorded verification. The credentials in the values and
notebooks are placeholders; the secrets are Kubernetes secrets, and nothing real is committed.

---

[← Version control](../README.md)
