[← Velero](../README.md)

# Velero on Azure

Provider-specific configuration for [Velero](../README.md).

Plugin: <https://github.com/vmware-tanzu/velero-plugin-for-microsoft-azure>

---

## Azure Files snapshots

Support is limited — see <https://github.com/vmware-tanzu/velero/issues/3151>.

The recommended approaches are **CSI Snapshot Data Movement** or **File System Backup**.

## Which of the two

**CSI Snapshot Data Movement is preferred**, per the documentation, for **data consistency**
reasons.

The distinction:

| | CSI Snapshot Data Movement | File System Backup |
|---|---|---|
| What is read | a point-in-time **snapshot** of the volume | the live filesystem |
| Consistency | the snapshot freezes the state before copying | files may change while being read |
| Requires | CSI driver with snapshot support, plus [external-snapshotter](../../external-snapshotter/README.md) | nothing beyond the node agent |

File System Backup reading a live filesystem is exactly the case where a database backup looks
successful and restores to a corrupt state — which is why the consistency argument decides it.

## Related

Azure storage drivers: [`storage/cloud/azure/`](../../../storage/cloud/azure/README.md)

---

[← Velero](../README.md)
