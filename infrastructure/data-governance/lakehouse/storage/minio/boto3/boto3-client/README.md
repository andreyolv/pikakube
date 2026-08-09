[← boto3](../README.md)

# boto3 client API

<https://github.com/boto/boto3>

---

## The problem it solves

`boto3.client('s3')` is the **low-level** interface: a verbatim mirror of the AWS S3 API, where
every operation maps to one API call and every response comes back as a **dict** in exactly the
shape the service returned it.

That verbosity is the reason to use it. It covers **every** S3 operation, it is what AWS actively
develops, and the AWS API reference maps onto it one-to-one — so when documentation describes an
operation, the call is already written.

The setup is identical in every notebook here, and the only MinIO-specific part is the endpoint:

```python
s3 = boto3.client('s3',
    endpoint_url=aws_credentials['AWS_ENDPOINT_URL'],
    aws_access_key_id=aws_credentials['ACCESS_KEY_ID'],
    aws_secret_access_key=aws_credentials['SECRET_ACCESS_KEY'])
```

## What each notebook demonstrates

| Notebook | Operations |
|---|---|
| `0-pip-install` | `boto3`, `minio`, `python-dotenv` |
| `01-buckets` | `list_buckets`, `create_bucket`, `head_bucket` — including checking the HTTP status in `response['ResponseMetadata']`, and using `head_bucket` in a `try` as the existence check |
| `02-objects` | `list_objects_v2`, `get_object`, and reading `response["Body"]` — a stream, decoded with `.read().decode()`; then writing JSON back with `put_object` |
| `02.1-files` | `download_file`, `upload_file`, and a loop uploading every JSON in a local directory |
| `03-tags` | `put_bucket_tagging`, `get_bucket_tagging`, `delete_bucket_tagging` |
| `04-policy` | `put_bucket_policy` with a raw IAM policy document, then `get` and `delete` |
| `05-versioning` | `put_bucket_versioning` — `Enabled` then `Suspended` — and `get_bucket_versioning` |
| **`06-lifecycle`** | `put_bucket_lifecycle_configuration` with expiration and transition rules over a prefix |
| `07-lock-config` | `put_object_lock_configuration` — `GOVERNANCE` mode with a default retention in days |
| `08-legal-hold` | `put_object_legal_hold` / `get_object_legal_hold` — `ON` and `OFF` per object |
| `09-retention` | `put_object_retention` with a `RetainUntilDate`, including `BypassGovernanceRetention` |

The last four are the governance operations, and they are the reason this set matters more than the
[resource](../boto3-resource/README.md) one — none of them exist there.

## The three that are worth understanding, not just copying

**`06-lifecycle`** is the S3 equivalent of the Azure work in
[`azure-lifecycle-policy/`](../../../azure-lifecycle-policy/README.md): a rule with a prefix filter,
a `Transition` to a storage class after N days, and an `Expiration`. Different field names, the same
model — and per [`../../../README.md`](../../../README.md), the only mechanism that caps storage
cost without someone remembering to run something.

**Object lock (`07`, `08`, `09`) is not the same thing as a lifecycle rule.** Lifecycle deletes
data on a schedule; object lock **prevents** deletion:

| Mechanism | Effect |
|---|---|
| `GOVERNANCE` mode retention | deletion blocked, but a privileged caller can bypass it — hence `BypassGovernanceRetention=True` in `09` |
| `COMPLIANCE` mode retention | deletion blocked for the period, **with no bypass, by anyone** |
| Legal hold | an indefinite block with no expiry date, toggled `ON` / `OFF` independently of retention |

That distinction is the whole point of the feature. Object lock exists for regulatory retention and
as ransomware protection, and `COMPLIANCE` mode means exactly what it says — **an object written
under it cannot be deleted before its date, including by the account owner.** Setting a long
compliance retention by mistake is not reversible, which is why the notebooks use `GOVERNANCE`.

Object lock must also be **enabled at bucket creation**; it cannot be turned on later.

**`04-policy`** takes a raw JSON policy string — the notebook grants anonymous `s3:GetObject` on the
whole bucket, which is a public bucket. Useful to see working, and not something to leave enabled.

## When to use this set

- **any service or job that will live** — this is the interface AWS develops, and it covers
  everything
- configuring bucket governance from code: versioning, lifecycle, object lock, retention
- checking whether MinIO implements a specific S3 operation, by running it
- when the AWS API reference is the documentation you are working from

## When not to use it

- a throwaway script where the dict handling is noise —
  [`boto3-resource/`](../boto3-resource/README.md) reads better, with the caveat recorded there
- MinIO-specific features: bucket notifications, event streams, encryption and replication
  configuration are in [`minio/`](../minio/README.md)
- as a credential pattern; the shared key from a local `env` file is a notebook convenience

## Notes

Everything is dict-handling, which is the interface's defining characteristic. The `01-buckets`
notebook checks success with:

```python
if response['ResponseMetadata']['HTTPStatusCode'] == 200:
```

That is idiomatic for this API and worth noticing: **the client interface surfaces the HTTP layer
rather than hiding it**, which is exactly the trade being made — more verbosity, complete fidelity
to what the service actually did.

Two rough edges recorded in the notebooks as they stand:

- `06-lifecycle` calls `get_bucket_lifecycle(BUCKET)` and `delete_bucket_lifecycle(BUCKET)`
  positionally; these operations take the keyword form `Bucket=`, and `get_bucket_lifecycle` is
  itself the deprecated predecessor of `get_bucket_lifecycle_configuration`
- `01-buckets` uses a bare `except` around `head_bucket`, which reports "the bucket does not exist"
  for a credential or network failure just as readily

Bucket names (`exemplo`, `plumbers`, `abacate`, `mlflow`, `teste`) and the `/home/jovyan/jsons/`
paths are from the Jupyter container these were run in. The sample data is in
[`jsons/`](../jsons/README.md).

---

[← boto3](../README.md)
