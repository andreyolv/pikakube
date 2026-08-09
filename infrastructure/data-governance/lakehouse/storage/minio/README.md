[← Storage](../README.md)

# MinIO — client access

<https://github.com/minio/minio>
<https://github.com/boto/boto3>
<https://github.com/minio/minio-py>

---

## The problem it solves

Everything above the storage layer eventually has to open a bucket. This folder is the **client
side** of that: how a Python process, a notebook or a Spark job actually talks to MinIO, and what
breaks the first time.

**The storage system itself is documented elsewhere** — erasure coding, tenants, capacity planning,
the AGPL licence trajectory and the alternatives are all in
[`site-reliability-engineering/storage/object-storage/minio/`](../../../../site-reliability-engineering/storage/object-storage/minio/README.md).
Read that for whether and how to run MinIO. Read this for how to use it.

What is here:

| | Content |
|---|---|
| [`boto3/`](boto3/README.md) | three notebook sets — the low-level `client` API, the `resource` API, and the native MinIO SDK — covering buckets, objects, tags, policies, versioning, lifecycle, object lock, encryption, replication and notifications |
| `parquet.ipynb` | a [Spark](../../../../data-engineering/processing/spark/README.md) round-trip: build a DataFrame, write Parquet to `s3a://`, read it back |

## The endpoint is the whole trick

MinIO speaks the S3 API, so the AWS SDK works against it unchanged. The only differences are the
endpoint and, on the JVM side, path-style addressing.

From Python:

```python
s3 = boto3.client('s3',
    endpoint_url='http://minio.minio.svc.cluster.local:9000',
    aws_access_key_id=...,
    aws_secret_access_key=...)
```

From Spark, via the S3A connector — the configuration recorded in `parquet.ipynb`:

```python
.config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1,"
                               "com.amazonaws:aws-java-sdk-bundle:1.12.709")
.config("spark.hadoop.fs.s3a.endpoint", "http://minio.minio:9000")
.config("spark.hadoop.fs.s3a.path.style.access", True)
.config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
```

Four things in there are worth knowing individually, because each is a distinct failure:

| Setting | What goes wrong without it |
|---|---|
| **`path.style.access`** | the client addresses `bucket.minio.minio:9000` as a hostname, DNS fails, and the error names DNS rather than configuration |
| **`hadoop-aws` version** | it must match the Hadoop version Spark was built against; a mismatch fails at class-load time with an unhelpful trace |
| `aws-java-sdk-bundle` version | it must match the `hadoop-aws` release, not the newest available |
| `fs.s3a.impl` | older Spark images do not resolve the S3A filesystem without it |

**The version-alignment row is where the time actually goes.** This is the concrete form of the
finding recorded across [`table-formats/`](../../table-formats/README.md): the format is the easy
part, and the storage integration is where the days disappear. The connector jars are the storage
integration.

The notebook also sets `fast.upload`, a 100 MB `multipart.size` and a connection maximum of 100 —
throughput tuning for writing large Parquet files, not correctness settings.

## When to use these examples

- wiring a new Python service, notebook or job to MinIO for the first time
- checking whether a specific S3 feature is actually supported by MinIO before designing on it —
  the notebooks call the APIs directly, which is a faster answer than the documentation
- configuring bucket-level governance from code: versioning, lifecycle, object lock, retention
- as the reference for the S3A settings a Spark job needs

## When not to use them

- deciding whether to run MinIO at all, or how — that is
  [the infrastructure page](../../../../site-reliability-engineering/storage/object-storage/minio/README.md),
  and the licence situation there is part of the decision
- reading and writing **tables** — use the [table format](../../table-formats/README.md) libraries,
  which manage the files; hand-managed object writes into a table's prefix will corrupt it
- as a production credential pattern; every example loads a shared key from a local `env` file,
  which is fine for a notebook and not for a service

## Notes

The notebooks are real working material against the in-cluster endpoint
(`minio.minio.svc.cluster.local:9000`), not illustrative snippets. Two practical details:

**Credentials come from an `env` file** next to the notebooks, loaded with `python-dotenv`, holding
`ACCESS_KEY_ID`, `SECRET_ACCESS_KEY`, `MINIO_ENDPOINT_URL` and `AWS_ENDPOINT_URL`. Note that the
two endpoint values differ in form: the MinIO SDK takes a bare `host:port` with a separate
`secure=False`, while `boto3` takes a full URL with the scheme. That is a real difference between
the two libraries and the first thing to check when one works and the other does not.

**Both endpoints and both key styles appear** because the notebooks predate any of this being
tidied — buckets named `teste`, `abacate` and `plumbers` are evidence of that. They are exploratory
material kept because the API calls in them are correct, and correct calls are the useful part.

The sample data is JSON records under [`boto3/jsons/`](boto3/jsons/README.md), and the notebooks
read from `/home/jovyan/...` paths — the Jupyter container's home directory, which is where they
were run.

The wider point about this component is made on
[the infrastructure page](../../../../site-reliability-engineering/storage/object-storage/minio/README.md)
and is worth repeating here: MinIO is the most depended-upon thing in this repository that is not
Kubernetes. Its availability requirements are the union of everything reading from it — the
lakehouse, observability, and backups alike.

Two neighbours that build directly on this: [`../README.md`](../README.md) for the lifecycle and
governance rules that keep the bucket from growing forever, and
[lakeFS](../../version-control/lakefs/README.md), which sits in front of this same MinIO and
versions the bucket — its integration here is recorded as done.

---

[← Storage](../README.md)
