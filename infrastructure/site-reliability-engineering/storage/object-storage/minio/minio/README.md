[← Object storage](../../README.md)

# MinIO

<https://github.com/minio/minio>
<https://github.com/minio/mc>

---

> **The open-source version has effectively died** — and the alternatives evaluated so far are
> all weak. That is the state of the category, not a preference.

## What it is

The de facto S3-compatible object storage for self-hosted environments. High performance,
simple to deploy, and the assumed backend for a large share of the tooling in this
repository — [Loki](../../../../../observability/logs/storage/loki/README.md),
[Thanos](../../../../../observability/metrics/long-term-storage/thanos/README.md),
[Velero](../../../../backup/velero/README.md), and any local lakehouse.

## The licensing situation

Features have been progressively moved out of the open-source distribution, and the community
edition has been reduced in ways that make it hard to recommend for new self-hosted
deployments.

Relevant threads:

- <https://github.com/minio/minio/issues/21647>
- <https://github.com/minio/minio/issues/21714>
- <https://github.com/coollabsio/minio> — a community fork

## What to do about it

| Situation | Answer |
|---|---|
| Running in a cloud | use S3, Blob Storage or GCS. There is no reason to operate this |
| Local development or a lab | MinIO is still the path of least resistance, and this is where it stays fine |
| Self-hosted, production, new | evaluate [Garage](../../garage/README.md) first; check the current licence terms of whatever you pick |
| Existing MinIO deployment | it keeps working — the issue is the trajectory, not a sudden break |

## The uncomfortable conclusion

The usual advice is to prefer open source. Here the field is genuinely thin: the standard has
become restrictive, and the replacements are less mature or poorly documented — see
[SeaweedFS](../../seaweedfs/README.md) and [RustFS](../../rustfs/README.md).

For a platform that needs object storage to be boring and reliable, the honest answer today is
usually a managed service.

## Related

Operator: [`../minio-operator/`](../minio-operator/README.md) · client: `mc`
(<https://github.com/minio/mc>)

---

[← Object storage](../../README.md)
