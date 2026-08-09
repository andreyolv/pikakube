[← Hive Metastore](../README.md)

# HMS on Azure Data Lake Storage

<https://github.com/cloudcheflabs/dataroaster/blob/master/components/hive/hive-metastore/docker/Dockerfile>

---

## The problem it solves

The same [Hive Metastore](../README.md), pointed at **ADLS Gen2** instead of S3. The metastore
itself is unchanged; what changes is the Hadoop filesystem driver it uses to reach the warehouse
and how that driver authenticates.

Two things follow from that, and they are the whole content of this variant:

1. the `abfs` driver lives in **`hadoop-azure`**, which is not in the upstream metastore image —
   so the image has to be built
2. ADLS authenticates with **OAuth client credentials** against Entra ID, not with a static key
   pair

| Manifest | Role |
|---|---|
| [`docker/Dockerfile`](docker/Dockerfile) | adds `hadoop-azure` 3.3.5 to `cloudcheflabs/hivemetastore:v3.3.5` |
| [`docker/build.sh`](docker/build.sh) | builds, tags and pushes `andreyolv/hive-azure` |
| [`mysql/statefulset.yaml`](mysql/statefulset.yaml) | MySQL 5.7 with a 1Gi PVC |
| [`mysql/service.yaml`](mysql/service.yaml) | `mysql.hive-metastore.svc:3306` |
| [`init-schema/job.yaml`](init-schema/job.yaml) | `schematool -initSchema -dbType mysql` into `metastore_db` |
| [`hive/configmap.yaml`](hive/configmap.yaml) | `core-site.xml` (OAuth) + `metastore-site.xml` (JDBC, Thrift port) |
| [`hive/deployment.yaml`](hive/deployment.yaml) | the metastore, `andreyolv/hive-azure`, port 9083 |
| [`hive/service.yaml`](hive/service.yaml) | Thrift endpoint for the query engines |

There is no `namespace.yaml` in this variant — it reuses the `hive-metastore` namespace created by
[`hms-aws/namespace.yaml`](../hms-aws/namespace.yaml). The two variants are alternatives, not
things to run side by side: same namespace, same MySQL service name, same Deployment name.

## How it differs from the AWS variant

| | [**hms-aws**](../hms-aws/README.md) | **hms-azure** |
|---|---|---|
| Storage | S3 or MinIO | **ADLS Gen2** |
| Driver | `s3a` | **`abfs`** |
| Auth type | static access key / secret key | `fs.azure.account.auth.type=OAuth` |
| Token provider | — | `ClientCredsTokenProvider` |
| Settings needed | endpoint, access key, secret key, path-style | tenant OAuth endpoint, client id, client secret |
| Image | `mykidong/hivemetastore:v3.0.0`, upstream | **`andreyolv/hive-azure`, built here** |
| Where credentials sit | a `Secret`, plus values in the ConfigMap | **inline in the ConfigMap** |

`ClientCredsTokenProvider` means a **service principal**: an app registration in Entra ID with a
client secret, granted *Storage Blob Data Contributor* on the storage account. The metastore
exchanges those credentials for a token on every filesystem operation.

## Notes

**The image is built here because `hadoop-azure` is missing upstream.** The Dockerfile downloads
`hadoop-azure-3.3.5.jar` from Maven Central into two directories — `$HADOOP_HOME/share/hadoop/common/lib`
and `$HADOOP_HOME/opt/hive-metastore/lib` — because the metastore and the Hadoop libraries load
from different classpaths and it is not obvious which one takes effect. Writing the JAR to both is
the pragmatic answer, and the pinned `3.3.5` must match the Hadoop version in the base image or
the class loads and then fails at runtime.

The base image is `cloudcheflabs/hivemetastore:v3.3.5` and the Dockerfile cites its origin,
[DataRoaster](https://github.com/cloudcheflabs/dataroaster). Note that the schema-init Job still
uses `cloudcheflabs/hivemetastore:v3.0.0` — `schematool` only talks to MySQL and needs no Azure
JAR, but the version skew between init and runtime is worth being deliberate about rather than
accidental.

**The build script pushes to a personal Docker Hub account.** `andreyolv/hive-azure:latest`, with
a `:latest` tag and no digest pinning. In a GitOps setup that is a mutable dependency in the query
path — a rebuild changes what the cluster runs without any manifest changing. A versioned tag and
an internal registry are what this needs before it is more than a lab.

**The credentials are placeholders, and in the wrong object.** The tenant OAuth endpoint, client
id and client secret are all `XXXXXXXX` in [`hive/configmap.yaml`](hive/configmap.yaml), and the
Deployment carries the author's own note on this — a commented-out volume mounting a
`metastore-cfg-secret` instead, with the remark that *the ConfigMap contains sensitive data, a
Secret would be better.* That comment is correct and the fix is unfinished: a client secret in a
ConfigMap is readable by anything with namespace read access and is not redacted anywhere.

The better answer on AKS is to skip the client secret entirely and use **workload identity**,
which trades the secret for a federated service-account token and removes the credential from the
manifests altogether.

**Everything else carries over from the AWS variant** — MySQL 5.7 with `root`/`root` and no
backup, the deprecated `com.mysql.jdbc.Driver` class, and the requirement that the schema-init Job
finishes before the Deployment starts. Those notes are on
[`hms-aws/README.md`](../hms-aws/README.md) and are not repeated here.

**The structural point.** Two variants exist because HMS holds storage credentials itself. Every
new storage backend means new driver JARs, new authentication configuration, and possibly a new
image. This is the cost that **credential vending** in the
[Iceberg REST catalogs](../../iceberg/README.md) is designed to remove.

---

[← Hive Metastore](../README.md)
