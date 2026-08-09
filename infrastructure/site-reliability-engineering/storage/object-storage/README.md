[← Storage](../README.md)

# Object storage

An HTTP API for storing blobs — not a filesystem, and not a PVC.

Tools covered: [`minio`](minio/README.md) · [`garage`](garage/README.md) · [`seaweedfs`](seaweedfs/README.md) ·
[`rustfs`](rustfs/README.md)

---

## Why this matters more than it looks

Object storage is the substrate under most of the modern data and observability stack:

| Consumer | What it stores there |
|---|---|
| [Loki](../../../observability/logs/storage/loki/README.md) | log chunks |
| [Thanos](../../../observability/metrics/long-term-storage/thanos/README.md) / Mimir | metric blocks |
| [Tempo](../../../observability/tracing/storage/tempo/README.md) | traces |
| Iceberg, Delta, Hudi | the data lake itself |
| [Velero](../../backup/velero/README.md) | backups |

In a cloud this is S3, Blob Storage or GCS and requires no thought. **On-premise it is a
component you have to run**, and it becomes the single most load-bearing piece of storage in
the platform — the place where losing data loses everything at once.

## It is not a filesystem

The most consequential misunderstanding here.

Object storage has no directories, no partial writes, no file locking and no POSIX semantics.
FUSE drivers exist that present a bucket as a mount point, and they are a **convenience for
reading**, not a filesystem.

Running a database, or anything expecting POSIX behaviour, on a FUSE-mounted bucket is a
reliable way to corrupt data. If a PVC is what is needed, that is
[block](../block-storage/README.md) or [file](../file-storage/README.md) storage.

## The tools

| Tool | Notes | Detail |
|---|---|---|
| **MinIO** | the de facto standard, and its open-source position has deteriorated — see its README | [→](minio/README.md) |
| **Garage** | lightweight, designed for geo-distributed self-hosting, Apache-2.0 | [→](garage/README.md) |
| **SeaweedFS** | capable, with documentation problems recorded in its README | [→](seaweedfs/README.md) |
| **RustFS** | newer Rust implementation, with the same documentation caveat | [→](rustfs/README.md) |

## The honest state of this category

> MinIO's open source has effectively died, and the alternatives so far are all weak.

That is the recorded assessment, and it is worth stating plainly rather than presenting four
options as equivalent. The category is in a bad moment: the standard has become
commercially restrictive, and the replacements are less mature, less documented, or both.

Practical consequence: **if a cloud provides object storage, use it.** Self-hosting this is a
real commitment right now, and the usual advice to prefer open source runs into a genuinely
thin field.

Garage is the most promising of the alternatives for a small self-hosted deployment; the
others carry the documentation caveats recorded in their READMEs.

## Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| Mounting a bucket via FUSE for a database | no POSIX semantics; corruption follows | block storage |
| Self-hosting when the cloud already offers it | operating the most load-bearing storage layer for no gain | use the managed service |
| One bucket for everything | lifecycle policies and access control cannot be separated | a bucket per consumer, with its own policy |
| No lifecycle policy | Loki and Thanos chunks accumulate forever | expiry on the bucket, not only in the tool |
| Single-node deployment for real data | it is the substrate for logs, metrics, traces and backups at once | replication, or accept it as a lab |

---

[← Storage](../README.md)
