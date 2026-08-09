[← Backup](../README.md)

# K8up

<https://github.com/k8up-io/k8up>

---

## The problem it solves

Scheduled volume backups to object storage, driven by CRDs and built on **Restic** — so the
backup format is well understood, deduplicated, encrypted and readable by the `restic` CLI
outside the cluster.

That last property is underrated. A backup you can inspect and restore with a standard tool,
without the operator that created it, is a meaningfully safer position than one locked inside
a proprietary format.

| CRD | Purpose |
|---|---|
| `Schedule` | recurring backup, prune and check |
| `Backup` | one-off |
| `Restore` | recovery |
| `Archive` | long-term copy |
| `Check` | verify repository integrity |

The `Check` resource is the one worth noticing — it verifies the repository rather than
assuming it is fine, which is the closest thing here to an automated restore test.

## When to use it

- straightforward scheduled volume backups to S3-compatible storage
- Restic's format matters: deduplication, encryption, and CLI access independent of the cluster
- a small footprint compared with a full backup platform

## When not to use it

- **cluster objects** also need protecting — K8up handles volumes only, [Velero](../velero/README.md) does both
- cross-cluster restore of whole workloads is the requirement
- application-consistent database backup — [Kanister](../kanister/README.md)

## Where it fits

Good in a cluster that is already fully described in Git. If Flux recreates every object, the
only thing genuinely at risk is the data — and this backs up exactly that, with nothing extra
to operate.

---

[← Backup](../README.md)
