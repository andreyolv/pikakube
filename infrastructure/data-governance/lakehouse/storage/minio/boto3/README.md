[← MinIO](../README.md)

# boto3 and the MinIO SDK

<https://github.com/boto/boto3>
<https://github.com/minio/minio-py>

Notebook sets: [`boto3-client/`](boto3-client/README.md) — the low-level API ·
[`boto3-resource/`](boto3-resource/README.md) — the object-oriented API ·
[`minio/`](minio/README.md) — the native MinIO SDK · [`jsons/`](jsons/README.md) — the sample data

---

## The problem it solves

Three different Python libraries can drive the same S3-compatible storage, they look nothing alike,
and choosing between them is a decision people make by accident. These notebooks run the same
operations through all three, which makes the differences concrete rather than theoretical.

Everything here talks to the in-cluster MinIO endpoint with credentials from a shared `env` file —
see [`../README.md`](../README.md) for the endpoint details and the two different URL forms the
libraries expect.

## boto3 has two API styles, and they are not equivalent

This is the thing worth stating plainly, because the AWS documentation shows both without ever
saying which to use.

| | `boto3.client('s3')` | `boto3.resource('s3')` |
|---|---|---|
| Level | **low-level** | higher-level |
| Shape | a **verbatim mirror of the AWS S3 API** | object-oriented — `Bucket`, `Object`, collections |
| Returns | **dicts**, exactly as the API responds | Python objects with attributes and methods |
| Reads like | `s3.list_objects_v2(Bucket=B)["Contents"]` | `s3.Bucket(B).objects.all()` |
| Coverage | **every S3 operation** | a curated subset |
| Errors | HTTP status in `response['ResponseMetadata']` | raised as exceptions |
| **Status at AWS** | actively developed | **maintenance mode — no new features** |

**`resource` is more pleasant to write and is not the one to build on.** AWS has placed the
resource interface in maintenance mode: it still works, it is not being extended, and newer S3
features never appear in it. Anything long-lived should use `client`.

The practical consequence shows up immediately in these notebooks. The `client` set covers
versioning, lifecycle, object lock, legal hold and retention; the `resource` set covers buckets,
objects and files, and stops — because those are the operations the resource interface exposes.

The mapping between them, for the same three tasks:

| Task | `client` | `resource` |
|---|---|---|
| List buckets | `s3.list_buckets()["Buckets"]` → dicts | `s3.buckets.all()` → objects |
| Upload a file | `s3.upload_file(Filename=f, Bucket=b, Key=k)` | `s3.Bucket(b).upload_file(f, k)` |
| Read an object | `s3.get_object(Bucket=b, Key=k)["Body"].read()` | `s3.Object(b, k).get()["Body"].read()` |

Note the third row: even the resource API drops back to a raw dict for the response body. The
abstraction is partial, which is a fair summary of the whole interface.

## The third option: the native MinIO SDK

[`minio/`](minio/README.md) uses `minio-py` rather than boto3, and it is not merely a stylistic
alternative:

| | boto3 | `minio-py` |
|---|---|---|
| Target | the S3 API generally | **MinIO specifically** |
| Config | `endpoint_url` with scheme | bare `host:port` plus `secure=` |
| Ergonomics | AWS-shaped, verbose | typed config objects — `LifecycleConfig`, `Retention`, `Tags` |
| Portability | **works against any S3 implementation** | tied to MinIO |
| Coverage of MinIO extras | what the S3 API defines | **bucket notifications, `listen_bucket_notification`** |

The last row is the real reason it is here. `listen_bucket_notification` opens a **live event
stream** of object creations and removals — a push mechanism for triggering ingestion when a file
lands, rather than polling a prefix on a schedule. That is not an S3 API operation, and boto3 has
no equivalent.

**The rule of thumb:** boto3 `client` for anything portable, `minio-py` when you want MinIO
features or the typed configuration objects, `resource` for a script you will throw away.

## When to use these notebooks

- deciding which library a new service should use, with the trade-offs visible rather than assumed
- checking whether MinIO actually supports a given S3 feature — running the call is a faster answer
  than reading either project's documentation
- configuring bucket governance from code: versioning, lifecycle, object lock, retention, tags
- as a copy-paste source for the awkward parts — lifecycle rule structure and object lock
  configuration in particular

## When not to use them

- as a production credential pattern; a shared key in a local `env` file is a notebook convenience
- for reading or writing **table** data — use the [table format](../../../table-formats/README.md)
  libraries; writing objects by hand into a table's prefix corrupts it
- as a MinIO administration reference; these are data-plane APIs, and cluster operations belong to
  [the infrastructure page](../../../../../site-reliability-engineering/storage/object-storage/minio/README.md)

## Notes

The three sets overlap deliberately — the same numbered notebooks (`01-buckets`, `02-objects`,
`03-tags`, …) appear in more than one folder, so the same operation can be compared across
libraries side by side. That symmetry is the point of the layout, and where a number is missing
from a set, that absence is itself informative: it means the library does not cover it.

Coverage across the three:

| Operation | [`boto3-client/`](boto3-client/README.md) | [`boto3-resource/`](boto3-resource/README.md) | [`minio/`](minio/README.md) |
|---|---|---|---|
| Buckets, objects, files | yes | yes | yes |
| Tags, policies | yes | — | yes |
| Versioning, lifecycle | yes | — | yes |
| Object lock, legal hold, retention | yes | — | yes |
| Encryption, replication, notifications | — | — | **yes** |

Dependencies are installed in `0-pip-install.ipynb`: `boto3`, `minio` and `python-dotenv`.

The sample data is in [`jsons/`](jsons/README.md), and the notebooks reference it under
`/home/jovyan/jsons/` — the Jupyter container's home directory, which is where they were run. Bucket
names are exploratory (`teste`, `abacate`, `plumbers`, `my-bucket`); the API calls are the part that
matters and they are correct.

The governance operations in these notebooks are not incidental. **Versioning, lifecycle, object
lock and retention are the bucket-level controls** that [`../../README.md`](../../README.md) argues
are the only things capping storage cost and the only enforceable form of a retention policy. These
notebooks are where those controls are actually exercised.

---

[← MinIO](../README.md)
