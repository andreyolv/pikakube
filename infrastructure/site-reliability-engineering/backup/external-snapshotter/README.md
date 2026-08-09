[← Backup](../README.md)

# external-snapshotter

<https://github.com/kubernetes-csi/external-snapshotter>

---

> **Not a choice — a prerequisite.** This is the CSI snapshot controller and the CRDs that make
> `VolumeSnapshot` exist. Without it, every snapshot-based tool in this folder fails.

## What it provides

| Resource | Purpose |
|---|---|
| `VolumeSnapshotClass` | which CSI driver takes the snapshot, and how |
| `VolumeSnapshot` | a request to snapshot a PVC |
| `VolumeSnapshotContent` | the actual snapshot object in the storage backend |

Plus the controller that reconciles them against the CSI driver.

## Why it is separate from Kubernetes

Snapshots are a CSI feature, and the controller ships out of tree. Managed Kubernetes usually
installs it; self-managed clusters and Kind usually do not — which is why the failure appears
suddenly on a cluster where "snapshots worked before".

## The error it explains

```
if kind is a CRD, it should be installed before calling Start
{"kind": "VolumeSnapshot.snapshot.storage.k8s.io",
 "error": "no matches for kind \"VolumeSnapshot\" in version \"snapshot.storage.k8s.io/v1\""}
```

That is [VolSync](../volsync/README.md) starting on a cluster without the snapshot CRDs. The same shape
appears with Velero's CSI plugin, Gemini and anything else that creates `VolumeSnapshot`
objects.

The message points at the consumer, not the cause — which is why it is worth recognising.

## Order of installation

1. **external-snapshotter** — CRDs and controller
2. a `VolumeSnapshotClass` for your CSI driver
3. only then the backup tool

Getting this backwards produces a backup tool that deploys cleanly, reports healthy, and never
successfully snapshots anything.

---

[← Backup](../README.md)
