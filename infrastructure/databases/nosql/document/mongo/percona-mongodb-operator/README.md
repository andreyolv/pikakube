[← MongoDB](../README.md)

# Percona Server for MongoDB Operator

<https://github.com/percona/percona-server-mongodb-operator>

Reference custom resource:
<https://github.com/percona/percona-server-mongodb-operator/blob/main/deploy/cr.yaml>

---

## Why this is usually the answer for self-hosting

**Apache 2.0, with the complete feature set and no commercial tier.**

That combination is what separates it from MongoDB's own operators, where the capabilities that
matter most for running a database in production — backups, point-in-time recovery, sharding —
are either absent or tiered.

| Capability | Community Operator | Percona |
|---|---|---|
| Replica sets | yes | yes |
| **Backups to object storage** | no | **yes** |
| **Point-in-time recovery** | no | **yes** |
| **Sharding** | no | **yes** |
| Licence | free, limited | **Apache 2.0** |
| Monitoring | basic | **PMM integration** |

## What it gives you

| Capability | Detail |
|---|---|
| `PerconaServerMongoDB` CRD | the whole cluster — replica sets, shards, config servers — as one declaration |
| **Scheduled backups** | to S3-compatible storage, including [MinIO](../../../../../site-reliability-engineering/storage/object-storage/minio/README.md) |
| **PITR** | oplog-based recovery to a point in time |
| Automated failover | primary election reflected in the Services |
| Users and roles | as Kubernetes resources |
| TLS | including automatic certificate management |
| Sharding | mongos routers and config servers as part of the topology |
| [PMM](../../../../tooling/monitoring/pmm/README.md) | Percona's monitoring, integrated |

Percona Server for MongoDB is a drop-in distribution of MongoDB Community with additional
enterprise-equivalent features — audit logging, encryption at rest, external authentication —
under an open licence.

## When to use it

- **self-hosting MongoDB** on Kubernetes, which is the default recommendation here
- backups and PITR are required, which they are for anything real
- an Apache licence matters for how the platform ships
- monitoring through [PMM](../../../../tooling/monitoring/pmm/README.md), which also covers
  MySQL and PostgreSQL in a mixed estate

## When not to use it

- **Atlas is the destination**, and consistency with MongoDB's own tooling is worth more —
  [`mongodb-kubernetes/`](../mongodb-kubernetes/README.md)
- a commercial support relationship with MongoDB Inc. is required
- development only, where [plain manifests](../mongodb/README.md) are less to read

## What to configure deliberately

The operator handles the topology. These remain decisions, and the defaults are not obviously
right:

| Setting | Why |
|---|---|
| **Write concern** | `w:1` acknowledges from the primary alone, and a failover can lose it. `w:majority` is what "written" usually means |
| **Read preference** | reading from secondaries means stale reads, which is fine until it is not |
| Backup schedule and retention | a backup configuration with no tested restore is a belief |
| Storage class | MongoDB is disk-latency sensitive |
| Anti-affinity | replica-set members on the same node is not replication |
| Schema validation | JSON Schema per collection — the only thing preventing silent field drift |

## Notes

[`example/mongodb.yaml`](example/mongodb.yaml) is the cluster definition kept here; the
[upstream `cr.yaml`](https://github.com/percona/percona-server-mongodb-operator/blob/main/deploy/cr.yaml)
is the annotated reference showing every available option, and it is the better document to read
when deciding what to set.

For this platform, this is the operator to reach for if MongoDB is ever run here rather than read
from — it backs up to [MinIO](../../../../../site-reliability-engineering/storage/object-storage/minio/README.md),
which already exists, and it monitors through [PMM](../../../../tooling/monitoring/pmm/README.md),
which is already mapped for the Postgres and MySQL side.

The restore caveat from [`storage/`](../../../../../site-reliability-engineering/backup/velero/README.md)
applies here as everywhere: scale the operator to zero before restoring, or it recreates an empty
volume before the restore lands.

---

[← MongoDB](../README.md)
