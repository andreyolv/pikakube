[← Backup](../README.md)

# Gemini

<https://github.com/FairwindsOps/gemini>
<https://github.com/FairwindsOps/charts>

---

## The problem it solves

`VolumeSnapshot` is a one-off request. Kubernetes has no built-in way to say "snapshot this
PVC every hour and keep the last 24".

Gemini adds that: a `SnapshotGroup` CRD with a schedule and a retention policy, creating and
expiring `VolumeSnapshot` objects.

Deliberately small — it schedules snapshots and nothing else.

## When to use it

- you want **scheduled local snapshots** for fast rollback, with retention handled
- the CSI driver supports snapshots and [external-snapshotter](../external-snapshotter/README.md) is installed
- the requirement is genuinely just scheduling, and a full backup platform is more than needed

## When not to use it

- **disaster recovery.** Snapshots usually live with the volume, in the same storage account —
  losing it loses both. This is fast rollback, not recovery
- cross-cluster restore
- cluster objects, or application consistency

## The distinction worth keeping

| Need | Tool |
|---|---|
| Undo a bad migration five minutes ago | **Gemini** — fast, local, cheap |
| Recover after losing the cluster or the account | [Velero](../velero/README.md) or [K8up](../k8up/README.md), to object storage |

Both are legitimate, and they are not substitutes. Treating scheduled snapshots as a backup
strategy is the mistake — they are excellent at the first row and useless at the second.

---

[← Backup](../README.md)
