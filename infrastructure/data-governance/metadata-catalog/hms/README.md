[← Metadata catalog](../README.md)

# Hive Metastore

<https://github.com/apache/hive>

Deployment variants here: [`hms-aws/`](hms-aws/README.md) — S3 and MinIO ·
[`hms-azure/`](hms-azure/README.md) — Azure Data Lake Storage

---

## The problem it solves

A query engine that is handed a bucket full of Parquet files knows nothing. It does not know which
files form a table, what the columns are called, where the partitions are, or whether another
writer is halfway through replacing them.

The Hive Metastore is the service that answers those questions. It is a **Java service backed by a
relational database** — MySQL or PostgreSQL — holding the definitions of databases, tables,
columns, partitions and their locations, and it is the reason Hive, Spark, Trino, Flink and
Presto can all resolve the same table name to the same files.

| Piece | What it is |
|---|---|
| **The service** | a JVM process speaking **Thrift** on port 9083 |
| **The database** | MySQL or PostgreSQL holding the actual metadata, in the Hive schema |
| **The schema tool** | `schematool -initSchema`, which creates that schema before first start |
| **The Hadoop config** | `core-site.xml`, which tells it how to reach object storage |

The important structural fact: HMS does not store metadata. **The database does.** HMS is a
Thrift front end over a relational schema, which is why the schema-init job is a hard prerequisite
and why a lost database means the tables are gone even though every file is still in the bucket.

It has been the de facto standard for over a decade. Everything reads it, which is its single
strongest argument.

## When to use it

- there is an **existing Hive or Spark estate** already resolving tables through it — migrating a
  live metastore is a project, not a config change
- the table format is **Hudi or Paimon** and the engines in use still expect a metastore; see
  [`lakehouse/table-formats/`](../../lakehouse/table-formats/README.md)
- an engine in the stack has **no Iceberg REST client** — the REST catalog is only useful if
  everything that queries can speak it
- something must work now, and it does: it is the option in this folder with no packaging
  problem, because it is deployed as plain manifests rather than a chart

## When not to use it

- the tables are **Iceberg** and every engine speaks REST — then use one of the
  [Iceberg REST catalogs](../iceberg/README.md), which is where this is going
- the deployment has to cross **proxies, gateways or a service mesh** — Thrift is not HTTP, and
  everything in a Kubernetes ingress path assumes HTTP
- **access control** is a requirement of the catalog itself — HMS has none natively, and
  authorisation is bolted on by whatever queries it (Ranger, engine-level rules)
- nobody wants to operate **another relational database** with its own backup, monitoring and
  migration story, for what is fundamentally a lookup table

### The Iceberg mismatch, stated plainly

HMS models a table as **a directory, whose partitions are subdirectories.** That was Hive's
design and it is coherent on its own terms: to list a partition you list a path.

Iceberg's entire premise is the opposite — the list of files that make up a table lives in a
manifest written by the writer, not in whatever happens to be on the filesystem. HMS can hold an
Iceberg table by storing the pointer to the current metadata file, but it is then being used as a
key-value store with a very elaborate schema attached. It works, and it is not what it was built
for.

That is the substance behind "HMS is being replaced". Not that it is old — that its data model
disagrees with the table format the industry has settled on.

## Notes

### Deployment references

The manifests here were assembled from these, none of which is an official Apache-published
deployment — because there is not one:

| Reference | What it contributed |
|---|---|
| <https://github.com/joshuarobinson/trino-on-k8s> | HMS running under Trino on Kubernetes, and the `joshuarobinson/hivemetastore` image |
| <https://itnext.io/hive-on-spark-in-kubernetes-115c8e9fa5c1> | the write-up behind the approach used here |
| <https://github.com/mykidong/hive-on-spark-with-spark-operator/tree/master/hive-metastore> | the manifests this deployment is closest to; the `mykidong/hivemetastore:v3.0.0` image |
| <https://github.com/Gradiant/bigdata-charts/tree/master/charts/hive-metastore> | a Helm chart alternative |
| <https://github.com/slamdev/helm-charts/tree/master/charts/hive-metastore> | a second Helm chart alternative |

The significance of that list is the list itself. **There is no official Hive Metastore container
image and no official Helm chart.** Everyone deploying HMS on Kubernetes is running a
community-built image — here `mykidong/hivemetastore` and `cloudcheflabs/hivemetastore` — and
assembling the Deployment, ConfigMap, schema-init Job and database themselves.

For the most widely deployed metadata service in the data ecosystem, that is a genuinely poor
packaging story, and it is worth weighing against the packaging complaints recorded for the
[REST catalogs](../iceberg/README.md). The difference is that HMS's manifests are simple enough
to own outright; a half-finished Helm chart is not.

### Inspecting the metastore database

Recorded from opening the metastore's own database to see what it holds:

```sql
mysql -u root -p mysql

SHOW DATABASES;
USE mysql;
SHOW TABLES;

SELECT * FROM DBS;

SELECT * FROM CTLGS;
SELECT * FROM TBLS;
```

**What those tables are.** They are not Hive data. They are the **Hive Metastore's own relational
schema** — the tables created by `schematool -initSchema`, in which the metastore records
everything it knows:

| Table | What each row is |
|---|---|
| `CTLGS` | a **catalog** — the top level added in Hive 3, above databases; usually one row, `hive` |
| `DBS` | a **database** (namespace), with its owner and its warehouse location |
| `TBLS` | a **table** — its name, its owning database, its type, and its storage descriptor |

Alongside them the schema carries `SDS` (storage descriptors: format, location, SerDe), `COLUMNS_V2`,
`PARTITIONS`, `PARTITION_KEYS` and `TABLE_PARAMS` — which is where an Iceberg table's
`metadata_location` pointer ends up.

This is the concrete answer to *"why does a metastore need a database?"* The metadata **is** a
normalised relational schema, queried with joins, updated transactionally. HMS is the Thrift
service in front of it. Reading `DBS` and `TBLS` directly is the fastest way to confirm what a
metastore actually contains when an engine says a table does not exist.

Two practical corrections when running the above against this deployment:

- the `USE mysql` line selects MySQL's own system database. The Hive schema here is created in
  **`metastore_db`** — see the `-url` argument in
  [`hms-aws/init-schema/job.yaml`](hms-aws/init-schema/job.yaml) — so that is the database to
  select before `SELECT * FROM DBS;`
- the credentials are `root`/`root` in both variants, which is fine for a lab and is exactly what
  should not survive into a shared cluster

The folder also keeps [`metadados.JPG`](metadados.JPG), a screenshot from that inspection.

### Storage integration

Two integrations were recorded, and they are the whole reason there are two variants:

> - Integration with AWS S3 / MinIO
> - Integration with Azure Data Lake Storage

HMS needs storage access itself — it is not only a name server. It reads and writes the warehouse
directory, validates locations, and for non-Iceberg tables it lists partition directories. So the
Hadoop filesystem layer has to be configured inside the metastore, with credentials, and that
configuration is entirely different per cloud:

| Variant | Storage | Filesystem driver | Credentials |
|---|---|---|---|
| [`hms-aws/`](hms-aws/README.md) | S3 or MinIO | `s3a` | static access key / secret key |
| [`hms-azure/`](hms-azure/README.md) | ADLS Gen2 | `abfs` | OAuth client credentials (Entra ID service principal) |

This is precisely the problem that **credential vending** in the
[Iceberg REST catalogs](../iceberg/README.md) exists to remove: with HMS, every engine *and* the
metastore itself holds long-lived storage credentials in a config file.

## Where it fits here

It is what currently works, and the folder is honest about that. From
[`../README.md`](../README.md#7-how-this-applies-to-pikakube), HMS is the only entry in this
capability with no packaging blocker — while [Polaris](../iceberg/polaris/README.md),
[Lakekeeper](../iceberg/lakekeeper/README.md) and [Gravitino](../iceberg/gravitino/README.md) all
have one.

The direction is still the REST catalog. This is the incumbent that keeps queries answerable
until one of them is deployable.

---

[← Metadata catalog](../README.md)
