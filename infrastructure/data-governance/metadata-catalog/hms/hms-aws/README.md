[← Hive Metastore](../README.md)

# HMS on S3 / MinIO

<https://github.com/mykidong/hive-on-spark-with-spark-operator/tree/master/hive-metastore>

---

## The problem it solves

The [Hive Metastore](../README.md) needs to reach the object store where the warehouse lives. That
is not a property of HMS — it is a property of the Hadoop filesystem layer inside it, and it is
configured entirely differently per cloud. This variant is the **S3-compatible** one: AWS S3, or
MinIO running in the cluster — see [`lakehouse/`](../../../lakehouse/README.md).

| Manifest | Role |
|---|---|
| [`namespace.yaml`](namespace.yaml) | the `hive-metastore` namespace |
| [`mysql/statefulset.yaml`](mysql/statefulset.yaml) | MySQL 5.7 with a 1Gi PVC — the metastore's own database |
| [`mysql/service.yaml`](mysql/service.yaml) | `mysql.hive-metastore.svc:3306` |
| [`init-schema/job.yaml`](init-schema/job.yaml) | `schematool -initSchema -dbType mysql`, creating `metastore_db` |
| [`hive/configmap.yaml`](hive/configmap.yaml) | `core-site.xml` (S3 access) + `metastore-site.xml` (JDBC, Thrift port) |
| [`hive/secret.yaml`](hive/secret.yaml) | the S3 access key and secret key |
| [`hive/deployment.yaml`](hive/deployment.yaml) | the metastore itself, `mykidong/hivemetastore:v3.0.0`, port 9083 |
| [`hive/service.yaml`](hive/service.yaml) | Thrift endpoint for the query engines |

The ordering matters and is not enforced by anything here: **the schema-init Job must complete
before the Deployment starts.** A metastore pointed at an empty database does not create its own
schema; it fails.

## How it differs from the Azure variant

The only real difference is the filesystem driver and how it authenticates — and that difference
is large enough to require a different container image:

| | **hms-aws** | [**hms-azure**](../hms-azure/README.md) |
|---|---|---|
| Storage | S3 or MinIO | ADLS Gen2 |
| Driver | `s3a` — `org.apache.hadoop.fs.s3a.S3AFileSystem` | `abfs` |
| Credentials | **static access key / secret key** | **OAuth client credentials** (tenant, client id, client secret) |
| Extra JARs | none — `hadoop-aws` ships in the image | **`hadoop-azure` must be added** — hence a custom image |
| Image | `mykidong/hivemetastore:v3.0.0`, as published | `andreyolv/hive-azure`, built here |
| Secret handling | credentials in a `Secret`, injected as env vars | client secret inline in the ConfigMap |

The S3 side gets the easier deal on both counts: the driver is already in the image, and static
keys are the mechanism every S3-compatible store supports.

## Notes

**MinIO is configured with path-style access and TLS off.**
[`hive/configmap.yaml`](hive/configmap.yaml) sets `fs.s3a.endpoint` to
`http://minio.minio.svc.cluster.local:9000`, with `fs.s3a.path.style.access=true` and
`fs.s3a.connection.ssl.enabled=false`. Both are required for MinIO and both are wrong for real S3
— path-style is deprecated on AWS, and disabling TLS on a cloud endpoint is not an option. Point
this at AWS and those two properties are the first things to change.

**Credentials are supplied twice, through two mechanisms.** They are in `core-site.xml` as
`fs.s3a.access.key` / `fs.s3a.secret.key`, *and* injected into the pod as `AWS_ACCESS_KEY_ID` /
`AWS_SECRET_ACCESS_KEY` from the `my-s3-keys` Secret. The explicit `core-site.xml` values win, so
the Secret is effectively decorative here. Removing the config-file values is what makes the
Secret the real source — and is what would make an IRSA or workload-identity setup possible later.

**The lab credentials are literal.** `pikakube`/`pikakube` for MinIO, `root`/`root` for MySQL,
with the MySQL password in plain text in both the StatefulSet and the metastore ConfigMap. Correct
for a lab, and the first thing to replace with External Secrets before this is shared — note that
the [Lakekeeper](../../iceberg/lakekeeper/README.md) deployment in this repo already does exactly
that, generating and storing its PostgreSQL password through an `ExternalSecret`.

**MySQL 5.7 is end of life** and runs here as a single-replica StatefulSet with a 1Gi volume and no
backup. Section 6 of [`../../README.md`](../../README.md#6-anti-patterns) names this directly: the
metastore database holds the definitions without which the files in the bucket are not tables.
Losing it is not losing a cache.

**The JDBC driver class is `com.mysql.jdbc.Driver`**, the pre-8.x name. It works with the driver
bundled in this image and is deprecated in favour of `com.mysql.cj.jdbc.Driver` — worth knowing
when the image is bumped.

---

[← Hive Metastore](../README.md)
