[← boto3](../README.md)

# boto3 resource API

<https://github.com/boto/boto3>

---

## The problem it solves

`boto3.resource('s3')` is the **object-oriented** interface over the same API. Instead of calling
operations and unpacking dicts, you get Python objects — `Bucket`, `Object`, and collections you
can iterate and filter.

It is genuinely more pleasant to write:

| Task | [`client`](../boto3-client/README.md) | `resource` |
|---|---|---|
| List buckets | `s3.list_buckets()["Buckets"]` → dicts | `for b in s3.buckets.all(): b.name` |
| Delete a bucket | `s3.delete_bucket(Bucket=b)` | `s3.Bucket(b).delete()` |
| Upload a file | `s3.upload_file(Filename=f, Bucket=b, Key=k)` | `s3.Bucket(b).upload_file(f, k)` |
| List objects by prefix | `s3.list_objects_v2(Bucket=b, Prefix=p)["Contents"]` | `s3.Bucket(b).objects.filter(Prefix=p)` |
| Read an object | `s3.get_object(Bucket=b, Key=k)["Body"].read()` | `s3.Object(b, k).get()["Body"].read()` |

The collection model is the best part. `bucket.objects.all()` and `.filter(Prefix=...)` are lazy
and handle pagination themselves — with the client interface, iterating past 1,000 objects means
dealing with continuation tokens by hand.

The setup differs from the client version by one word:

```python
s3 = boto3.resource('s3', endpoint_url=..., aws_access_key_id=..., aws_secret_access_key=...)
```

## The thing to know before using it

**AWS has put the resource interface in maintenance mode.** It still works and is not being
removed, but it receives no new features, and S3 capabilities added since then do not appear in it.

That is not a stylistic footnote; it decides where the interface belongs:

| | Verdict |
|---|---|
| Exploratory scripts, notebooks, one-off jobs | fine, and nicer to write |
| **Anything long-lived** | use [`client`](../boto3-client/README.md) |
| Anything needing a recent S3 feature | it will not be there |

The evidence is visible in this folder without reading any release notes. The client set has eleven
notebooks; this one has three. **Tags, policies, versioning, lifecycle, object lock, legal hold and
retention are all absent** — not because they were skipped, but because the resource interface does
not expose them. Every governance operation that
[`../../../README.md`](../../../README.md) argues is the point of configuring buckets at all is
missing from the friendlier API.

## What each notebook demonstrates

| Notebook | Operations |
|---|---|
| `01-buckets` | `s3.buckets.all()` and `bucket.name`, `create_bucket`, and `s3.Bucket(b).delete()` |
| `02-objects` | nested iteration over every bucket and its objects; `objects.filter(Prefix=...)`; reading through both `s3.Bucket(b).Object(k).get()` and `s3.Object(b, k).get()` |
| `02.1-files` | `Bucket.download_file` and `Bucket.upload_file`, plus a loop uploading a local directory of JSON |

The two access paths in `02-objects` — `Bucket(b).Object(k)` and `Object(b, k)` — are equivalent.
The first reads better when a bucket object already exists in scope; the second is shorter.

## When to use it

- exploratory work, notebooks and scripts, where iterating collections is most of the job
- paginating large listings without writing continuation-token handling
- code whose readability matters more than its lifespan

## When not to use it

- **production services** — maintenance mode means no new features, and eventually a wall
- versioning, lifecycle, object lock, retention, tags or policies — none of them are here; use
  [`boto3-client/`](../boto3-client/README.md)
- MinIO-specific features — [`minio/`](../minio/README.md)
- table data; that belongs to the [table format](../../../../table-formats/README.md) libraries

## Notes

The comparison this folder makes is the reason to keep it. The same operations exist in
[`boto3-client/`](../boto3-client/README.md) under the same notebook numbers, so the two interfaces
can be read side by side — and the honest conclusion is that **the nicer API is the one not to
build on.**

Worth noticing in `02-objects`: even the resource interface returns a raw dict from `.get()`, so
reading a body is still `["Body"].read().decode()`. The abstraction is partial, which is a fair
summary of the interface as a whole.

Bucket names (`teste`, `temp`) and the `/home/jovyan/jsons/` paths are from the Jupyter container
these were run in. The sample data is in [`jsons/`](../jsons/README.md).

---

[← boto3](../README.md)
