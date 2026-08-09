[← Object storage](../README.md)

# MinIO

<https://github.com/minio/minio>
<https://github.com/minio/operator>

Deployment shapes: [`minio/`](minio/README.md) — the standalone deployment ·
[`minio-operator/`](minio-operator/README.md) — tenants as custom resources

---

## What it is

S3-compatible object storage that runs anywhere — which for a self-hosted platform is the
foundation almost everything else assumes.

The S3 API has become the interface for object storage in the same way SQL became the interface
for relational data. A very large share of modern infrastructure speaks it, and MinIO is what
provides it when there is no cloud provider underneath.

## Why it is load-bearing here

Look at what depends on object storage across this repository:

| Component | Uses it for |
|---|---|
| [Loki](../../../../observability/logs/storage/loki/README.md) | log chunks |
| [Thanos](../../../../observability/metrics/long-term-storage/thanos/README.md) | long-term metrics |
| [Tempo](../../../../observability/tracing/storage/tempo/README.md) | traces |
| [Velero](../../../backup/velero/README.md) | cluster backups |
| [Lakehouse table formats](../../../../data-governance/lakehouse/table-formats/README.md) | the data itself |
| [Litestream](../../../../databases/sql/sqlite/litestream/README.md) | SQLite replication |
| [Databend](../../../../databases/analytical/databend/README.md), [AutoMQ](../../../../data-streaming/event-streaming/automq/README.md) | primary storage |

That list is the argument for treating this as **infrastructure with real availability
requirements**, not as a convenience. If object storage is unavailable, logs stop being queryable,
backups stop running, and the lakehouse stops being readable.

## The two deployment shapes

| Shape | Use |
|---|---|
| [`minio/`](minio/README.md) | a single deployment, or a simple distributed set — configuration in Git |
| [`minio-operator/`](minio-operator/README.md) | **tenants** as custom resources, with erasure coding and lifecycle managed |

The operator's `Tenant` model is the one that matters at any scale: separate tenants for
observability, backups and the lakehouse, each with their own capacity and credentials, rather
than one bucket namespace shared by everything.

## The licence situation

This needs stating plainly, because it is the reason
[`../README.md`](../README.md) describes this category as being in a difficult state.

MinIO is **AGPLv3**. That has always required care for anything distributed, and more recently the
project has moved capabilities — notably parts of the web console — behind its commercial
offering, and reduced what the community edition includes.

For internal platform use AGPL is generally workable. What has changed is the trajectory: features
that were present have been removed from the open edition, which makes future planning harder
regardless of today's terms.

The alternatives in the sibling folders exist largely because of this:
[Garage](../garage/README.md), [SeaweedFS](../seaweedfs/README.md) and
[RustFS](../rustfs/README.md) — see
[`../README.md`](../README.md) for how they compare.

## What to get right

| Concern | Detail |
|---|---|
| **Erasure coding** | the distributed mode's durability mechanism; a single-node deployment has none |
| **Capacity planning** | erasure coding costs overhead, and it cannot be changed later |
| Separate tenants or buckets | observability, backups and data should not share a failure domain |
| **Credentials** | per-consumer access keys with scoped policies, not one root credential everywhere |
| Storage class | it is I/O-bound; the underlying volumes decide its performance |
| Versioning and lifecycle | per bucket, and it is what controls unbounded growth |
| Backups of the backups | Velero writing here means this bucket is the recovery path |

The last row deserves thought. If [Velero](../../../backup/velero/README.md) backs up the cluster
into MinIO running *in* that cluster, the backup does not survive the failure it exists for.

## Notes

The most depended-upon component in this repository that is not Kubernetes itself.

That is worth stating explicitly because it changes how it should be treated: MinIO here is not
"storage for the lakehouse", it is the substrate under observability, backups and data alike. Its
availability requirements are the union of everything that reads from it.

The related decision recorded in [`../README.md`](../README.md): this category is genuinely
unsettled right now, and the licence trajectory is the reason. Knowing the alternatives before
needing them is the point of that folder.

---

[← Object storage](../README.md)
