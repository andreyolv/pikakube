[← Thanos](../README.md)

# MinIO

<https://github.com/minio/minio>

---

## Why it is here

[Thanos](../README.md) stores metric blocks in **S3-compatible object storage**. In a cloud
that is S3, Blob Storage or GCS. On a local or on-prem cluster there is no such service, and
MinIO provides one.

Same role it plays for [Loki](../../../../logs/storage/loki/minio/README.md): the object storage layer
that everything else assumes exists.

## When to use it

- local or on-prem clusters where Thanos, Loki or Tempo need a bucket
- development environments that should behave like production without a cloud account
- air-gapped deployments

## When not to use it

- running in a cloud that already provides object storage — use it rather than operating a
  storage system to reach a service that is already there

## The responsibility it brings

For Thanos specifically, this bucket **is** the long-term metric store. Local Prometheus
retention is short by design, so once blocks are uploaded, MinIO holds the only copy of
anything older than the local window.

That makes replication, capacity and backup for this component a real obligation, not a
detail — and it is easy to overlook when it is filed mentally as "the Thanos backend".

## Operational note

The Thanos compactor must run as a **single instance per bucket**. Two compactors against the
same MinIO bucket corrupt data — see [Thanos](../README.md).

---

[← Thanos](../README.md)
