[← boto3](../README.md)

# MinIO Python SDK

<https://github.com/minio/minio-py>

---

## The problem it solves

`minio-py` is MinIO's own client. It talks to the same storage as
[boto3](../boto3-client/README.md), and it is not merely a stylistic alternative — it reaches
things the S3 API does not define, and it replaces raw dicts with **typed configuration objects**.

```python
client = Minio(
    aws_credentials['MINIO_ENDPOINT_URL'],   # bare host:port, no scheme
    access_key=..., secret_key=..., secure=False)
```

Note the endpoint form. boto3 takes a full URL with a scheme; `minio-py` takes `host:port` plus a
separate `secure=` flag. That difference is the first thing to check when one library connects and
the other does not — and it is why the `env` file next to these notebooks carries both
`MINIO_ENDPOINT_URL` and `AWS_ENDPOINT_URL`.

| | boto3 | `minio-py` |
|---|---|---|
| Target | the S3 API generally | **MinIO specifically** |
| Configuration | dicts matching the API's JSON | **typed objects** — `LifecycleConfig`, `Retention`, `Tags`, `SSEConfig` |
| Portability | **any S3 implementation** | tied to MinIO |
| Beyond the S3 API | nothing | **bucket notifications and a live event stream** |

The typed objects are the ergonomic win. Compare a lifecycle rule expressed as
`Rule(ENABLED, rule_filter=Filter(prefix="logs/"), expiration=Expiration(days=1))` against the
nested dict the same rule requires in boto3 — the mistakes it prevents are the ones that otherwise
fail at the API with a schema error.

## What each notebook demonstrates

| Notebook | Operations |
|---|---|
| `01-buckets` | `make_bucket`, `list_buckets`, `bucket_exists`, `remove_bucket`, and a first look at `listen_bucket_notification` |
| `02-objects` | `list_objects` with `prefix=` and `recursive=` |
| `02.1-files` | `fput_object` and `fget_object` — file-to-object and back |
| `03-tags` | `Tags.new_bucket_tags()` and `Tags.new_object_tags()`, set / get / delete — **both bucket and object level** |
| `04-policy` | `set_bucket_policy` with a JSON policy document, then get and delete |
| `05-versioning` | `VersioningConfig(ENABLED)`, and reading back `config.status` |
| **`06-lifecycle`** | `LifecycleConfig` with `Rule`, `Filter`, `Transition(days=30, storage_class="GLACIER")` and `Expiration(days=1)` |
| `07-lock-config` | `make_bucket(..., object_lock=True)`, then `ObjectLockConfig(GOVERNANCE, 15, DAYS)` |
| `08-object-legal-hold` | `enable_object_legal_hold`, `is_object_legal_hold_enabled`, `disable_object_legal_hold` |
| **`09-encryption`** | `set_bucket_encryption(SSEConfig(Rule.new_sse_s3_rule()))` — default server-side encryption |
| **`10-replication`** | `ReplicationConfig` with `Destination`, `DeleteMarkerReplication` and an `AndOperator` filter |
| **`11-notification`** | `NotificationConfig` with `QueueConfig`, plus `listen_bucket_notification` |
| `12-retention` | `Retention(GOVERNANCE, utcnow() + timedelta(...))`, set and get |

The four in bold are the ones with no counterpart in either boto3 set, and they are the reason to
know this library exists.

## The event stream is the real differentiator

`listen_bucket_notification` opens a **live stream** of bucket events:

```python
with client.listen_bucket_notification(
        bucket_name=BUCKET, prefix="abc/",
        events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"]):
```

That turns object storage from something you poll into something that **pushes**. A pipeline can
react when a file lands rather than listing a prefix every five minutes — which matters more than
it sounds, because prefix listing is the operation that gets expensive first as a bucket grows (see
[`../../../README.md`](../../../README.md#5-the-small-files-problem-from-the-storage-side)).

`11-notification` shows the durable version of the same idea: `set_bucket_notification` with a
`QueueConfig` pointing at a queue ARN, so events are delivered to a broker rather than to a
long-lived Python process. **That is the production shape** — the streaming listener is a
connection that dies with the process, while queued notifications survive it.

The queue target has to exist and be configured in MinIO first; the notebook leaves
`"QUEUE-ARN-OF-THIS-BUCKET"` as a placeholder, which is honest about where the real work is.

## Replication and encryption, briefly

**`10-replication`** configures bucket-to-bucket replication with a rule filter and explicit
handling of delete markers. Whether deletes replicate is a deliberate choice and the notebook
disables it — replicating deletions means a mistaken delete propagates to the copy, which
disqualifies replication as a backup. The role and destination bucket ARN are placeholders,
correctly: both are prerequisites configured outside this API.

**`09-encryption`** sets default SSE-S3 on a bucket, so objects are encrypted at rest with
server-managed keys and no client change. That is the cheap tier of encryption; a KMS-backed
alternative exists and is a key-management decision rather than a storage one.

## When to use it

- MinIO is the storage and will remain so
- you want **bucket notifications** or the event stream — boto3 has no equivalent
- encryption or replication configuration
- the typed configuration objects are worth the coupling, which for lifecycle and retention rules
  they frequently are

## When not to use it

- code that must also run against AWS S3 or another implementation — use
  [`boto3-client/`](../boto3-client/README.md)
- an existing codebase already standardised on boto3, for one feature's sake
- table data; that belongs to the [table format](../../../../table-formats/README.md) libraries

## Notes

The most complete of the three sets — thirteen notebooks against the client interface's eleven and
the resource interface's three — which is unsurprising for the vendor's own SDK against its own
product.

Two details worth carrying:

**`object_lock=True` at bucket creation.** `07-lock-config` creates the bucket with object lock
enabled, because it **cannot be enabled afterwards**. Same constraint as S3, and the same trap:
discovering the requirement after the bucket is in use means creating a new bucket and copying.

**Governance mode has a bypass; compliance mode does not.** These notebooks use `GOVERNANCE`
throughout, which is the reversible choice. A compliance-mode retention cannot be shortened or
removed by anyone, including the account owner, until it expires — see
[`boto3-client/`](../boto3-client/README.md) for the same distinction from the S3 API side.

Bucket names (`my-bucket`, `my-bucket3`, `teste`, `mlflow`) and the `/home/jovyan/jsons/` paths are
from the Jupyter container these were run in. The sample data is in [`jsons/`](../jsons/README.md).

---

[← boto3](../README.md)
