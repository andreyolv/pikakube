[← Backup](../README.md)

# Velero

<https://github.com/vmware-tanzu/velero>
<https://github.com/vmware-tanzu/helm-charts>
<https://velero.io/docs/>

Plugins: [CSI](https://github.com/vmware-tanzu/velero-plugin-for-csi) ·
[AWS](https://github.com/vmware-tanzu/velero-plugin-for-aws) ·
[Azure](https://github.com/vmware-tanzu/velero-plugin-for-microsoft-azure)

UI: <https://github.com/seriohub/velero-ui> · file-level engine:
[Kopia](https://github.com/kopia/kopia)

Provider notes: [`aws/`](aws/) · [`azure/`](azure/README.md)

---

## The problem it solves

Backs up **both halves** of a Kubernetes workload: the API objects and the persistent volumes
behind them — and can restore either into a different cluster.

That cross-cluster restore is what makes it the default. Volume snapshots alone are usually
tied to the storage provider and cannot be recovered anywhere else, which fails exactly in the
scenario people buy backups for.

| Capability | Why it matters |
|---|---|
| Object + volume in one backup | a restore brings back a working workload, not orphaned data |
| File-level backup (Kopia/Restic) | portable, and survives losing the cluster entirely |
| CSI snapshots | fast, when the storage layer supports it |
| **Backup hooks** | freeze and flush before the snapshot — the difference between a restorable database and a corrupt one |
| Selective restore | by namespace, label or resource type |

## When to use it

- **the default** for Kubernetes backup — CNCF, broad provider support, and the only common tool that does objects and volumes together
- disaster recovery where the cluster itself may be gone
- migrating workloads between clusters, which is the same operation as a restore

## When not to use it

- application-specific backup logic is the requirement — [Kanister](../kanister/README.md) models that properly
- you want a supported commercial product with policy management — [K10](../k10/README.md)
- continuous replication rather than point-in-time backup — [VolSync](../volsync/README.md)

## Upgrade note

Recorded in [`tools-update/`](../../tools-update/README.md): update the Velero **image only
when it is compatible with the plugin versions**. The plugins version independently, and a
mismatch is a backup system that appears healthy and fails on restore.

---

## Notes

### Restoring Strimzi — the operator has to be paused

When restoring a PVC that an operator manages, the operator will recreate an empty one before
the restore lands. Scale it to zero first:

```bash
kubectl scale deploy/strimzi-cluster-operator --replicas=0
```

A volume created automatically by the operator can then be deleted and restored properly.

This generalises to **every operator-managed workload** — CloudNativePG, Elastic, anything with
a controller reconciling volumes.

### Azure

Azure Files snapshot support: <https://github.com/vmware-tanzu/velero/issues/3151>

The recommendation is **CSI Snapshot Data Movement** or File System Backup, with CSI Snapshot
Data Movement preferred for data consistency reasons.

### UI

<https://github.com/seriohub/velero-ui/blob/main/tmp/helm/seriohub-velero/values.yaml>

### Design and open issues worth reading first

<https://github.com/vmware-tanzu/velero/tree/main/design/Implemented>

- <https://github.com/vmware-tanzu/velero/discussions/7196>
- <https://github.com/vmware-tanzu/velero/issues/6195>
- <https://github.com/vmware-tanzu/velero/issues/4802>
- <https://github.com/vmware-tanzu/velero/discussions/4786>
- <https://github.com/vmware-tanzu/velero/discussions/8794>
- <https://github.com/vmware-tanzu/velero/issues/3151>
- <https://github.com/vmware-tanzu/velero/issues/7139>
- <https://github.com/vmware-tanzu/velero/issues/2957>
- <https://github.com/vmware-tanzu/velero/discussions/9050>

Worth reviewing before depending on it: backup tools fail in ways that are only visible at
restore time, and this list is where those edges are documented.

---

[← Backup](../README.md)
