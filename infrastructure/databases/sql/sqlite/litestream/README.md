[← SQLite](../README.md)

# Litestream

<https://github.com/benbjohnson/litestream>

---

## The problem it solves

SQLite's one real weakness for a service is that the data lives in a file on one node. Losing the
node loses the data.

Litestream answers that without changing the application at all: it reads SQLite's **write-ahead
log** and streams it continuously to object storage, giving point-in-time recovery.

| | Plain SQLite | With Litestream |
|---|---|---|
| Survives node loss | no | **yes — restore from object storage** |
| Point-in-time recovery | no | **yes** |
| **Application changes** | — | **none** |
| Extra components | — | one sidecar process |
| Write path impact | — | negligible; it reads the WAL |

The "no application changes" row is what makes it interesting. The application keeps using SQLite
exactly as before; replication is a separate process watching the same file.

## How it works

SQLite in [WAL mode](../sqlite/README.md#configuration-which-is-what-makes-it-production-capable)
appends every change to a write-ahead log. Litestream reads that log, ships the frames to S3-
compatible storage, and periodically writes a full snapshot.

Restoring replays the snapshot plus the frames up to a chosen point:

```bash
litestream replicate /data/app.db s3://bucket/app.db
litestream restore -o /data/app.db s3://bucket/app.db
```

The replication lag is measured in **seconds**, configurable, and it is the amount of data at risk
in a sudden node loss.

## When to use it

- **a single-writer service on Kubernetes** whose data must survive the pod and the node
- the alternative being considered is a PostgreSQL cluster for a service that does not need one
- point-in-time recovery is wanted without a backup system
- edge deployments replicating to a central store

## When not to use it

- **multiple writers** — Litestream does not change SQLite's single-writer limit
- read replicas that must be writable; this is one-way replication
- zero data loss is a requirement — there is a lag window
- the database is not in WAL mode, which it must be

## The Kubernetes shape

This is where it earns its place in a platform repository:

| Element | Detail |
|---|---|
| **Deployment, not StatefulSet** | one replica; the PVC holds the working copy |
| **Sidecar container** | Litestream running `replicate` alongside the application |
| **Init container** | `litestream restore` on startup, so a rescheduled pod rebuilds its database |
| Object storage | [MinIO](../../../../site-reliability-engineering/storage/object-storage/minio/README.md) or S3 |
| `replicas: 1` | **strictly** — two writers corrupt the file |

The init-container pattern is the whole trick: the pod starts, restores from object storage if the
volume is empty, and the application opens a database that is already current. A node failure
becomes a reschedule rather than an incident.

The `replicas: 1` constraint must be enforced deliberately — with a `Recreate` strategy rather
than `RollingUpdate`, or a rollout briefly runs two pods against the same file.

## The argument it makes

Worth stating, because it changes a default.

A great many small services are given a PostgreSQL cluster because "it needs a real database".
Most of them have one writer, modest data, and no requirement that PostgreSQL uniquely satisfies.

SQLite plus Litestream covers that case with: one pod, one PVC, a sidecar, and continuous backup
to storage that already exists — against an operator, a StatefulSet, replicas, a connection
pooler and a backup schedule.

That is not an argument against PostgreSQL for things that need it. It is an argument that the
question *"does this need a database server?"* has a third answer.

## Notes

Mapped as the durability half of [`sqlite/`](../README.md), and the pairing that makes SQLite a
serious option on Kubernetes rather than a development convenience.

The natural fit here is [MinIO](../../../../site-reliability-engineering/storage/object-storage/minio/README.md),
which already exists in this platform — so the storage target requires nothing new.

Worth knowing that the project's development has been intermittent, with the author's attention
partly on a successor design. The tool works and is widely used; as with anything in the critical
path of a service's durability, checking current activity before depending on it is reasonable
diligence.

---

[← SQLite](../README.md)
