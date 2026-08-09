[← PostgreSQL](../README.md)

# PostgreSQL operators

Running Postgres on Kubernetes without writing the failover logic yourself.

Tools covered: [`cnpg`](cnpg/README.md) · [`crunchydata`](crunchydata/README.md) ·
[`stackgres`](stackgres/README.md) · [`zalando`](zalando/README.md)

---

## What an operator actually does

A StatefulSet gives you a running Postgres. It does not give you a **database**:

| Concern | Without an operator |
|---|---|
| **Failover** | someone promotes a replica, by hand, at 3am |
| Replication setup | configured manually, and drifts |
| **Backup and PITR** | a CronJob someone wrote, tested once |
| Minor upgrades | rolling restart in the right order, by hand |
| Connection routing | clients need to know which pod is primary |
| Certificates | issued and rotated manually |

An operator encodes all of that as controller logic. That is the entire value, and it is why
running Postgres on Kubernetes stopped being a bad idea.

## The tools

| Operator | Backing | Shines when | Detail |
|---|---|---|---|
| **CloudNativePG** | EDB, CNCF | **the current default** — no external dependencies, clean design, native backup to object storage | [→](cnpg/README.md) |
| **Crunchy Postgres** | Crunchy Data | you want a commercially supported operator with a long track record | [→](crunchydata/README.md) |
| **StackGres** | OnGres | you want extensions, pooling, monitoring and backup bundled as one opinionated stack | [→](stackgres/README.md) |
| **Zalando** | Zalando | large existing deployments; it was the standard for years | [→](zalando/README.md) |

### Why CloudNativePG became the default

It runs **without Patroni, without etcd and without a separate consensus layer** — using the
Kubernetes API itself for coordination. Fewer moving parts than the generation before it, and
backup to object storage is a first-class feature rather than a sidecar.

Zalando's operator was the standard for a long time and carries that architecture; StackGres
bundles more and is more opinionated; Crunchy is the commercial option.

For a new cluster, CNCF governance plus the simpler architecture is why CNPG is the usual
answer now.

## What to verify, whichever you pick

| Check | Why |
|---|---|
| **Restore, actually performed** | with the operator scaled to zero, or it recreates an empty volume first |
| Backup destination outlives the cluster | object storage, not a PVC in the same cluster |
| PITR works, not just full backups | recovering to *before* the bad migration is the real requirement |
| Minor upgrade path | how a version bump happens, and what it interrupts |
| Connection pooling | see [`tooling/pooler/`](../../../tooling/pooler/README.md) |

The first row is the one that is skipped. An operator that takes backups and has never been
restored from is a hypothesis — see
[`backup/`](../../../../site-reliability-engineering/backup/README.md).

---

[← PostgreSQL](../README.md)
