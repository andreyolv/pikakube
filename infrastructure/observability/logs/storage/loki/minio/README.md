[← Loki](../README.md)

# MinIO

<https://github.com/minio/minio>

---

## Why it is here

[Loki](../README.md) stores its chunks in **S3-compatible object storage**. In a cloud that
means S3, Blob Storage or GCS. On a local or on-prem cluster there is no such service — and
MinIO fills that gap.

It is not a logging component. It is the object storage backend that makes Loki's design work
outside a cloud, and the same role applies to
[Thanos](../../../../metrics/long-term-storage/thanos/), Tempo and anything else that expects
a bucket.

## When to use it

- local or on-prem clusters where Loki, Thanos or Tempo need a bucket and no cloud provides one
- development environments that should behave like production without a cloud account
- air-gapped deployments

## When not to use it

- running in a cloud that already offers object storage — use it; there is no reason to operate a storage system to reach a service that already exists
- you need the durability guarantees of a managed provider without operating for them

## What it costs you

Object storage is where the data actually lives. Running it yourself means owning replication,
capacity and backup for the layer everything else assumes is reliable — which is a real
responsibility, and easy to skip past when it is "just the Loki backend".

---

## Notes

Python client reference: <https://github.com/boto/boto3>

MinIO speaks the S3 API, so `boto3` works against it unchanged — which is what makes it a
faithful local stand-in for S3 in pipelines and tests as well as for Loki.

---

[← Loki](../README.md)
