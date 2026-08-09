[← Backup](../README.md)

# VolSync

<https://github.com/backube/volsync>

---

## The problem it solves

Most tools here **back up** a volume — a copy you restore from later. VolSync **replicates**
one: asynchronous, scheduled synchronisation of a PVC to another cluster or another storage
backend, using Restic, Rclone or rsync.

The difference is what it is for. A backup answers "get it back". Replication answers "have it
already there", which is a different recovery objective and a much shorter one.

## When to use it

- **disaster recovery across clusters** where the volume must already exist on the other side
- a meaningfully short RPO — replication runs on a schedule measured in minutes
- moving persistent data between clusters as an ongoing arrangement rather than a one-off

## When not to use it

- point-in-time restore is what you need — [Velero](../velero/README.md) has proper backup semantics
- cluster **objects** also need protecting; this handles volumes only
- a one-off volume copy — [pv-migrate](../pv-migrate/README.md) is the simpler tool for that

---

## Notes

### It fails without the snapshot CRDs

```
2024-11-25T23:37:08.958Z ERROR controller-runtime.source.EventHandler
if kind is a CRD, it should be installed before calling Start
{"kind": "VolumeSnapshot.snapshot.storage.k8s.io",
 "error": "no matches for kind \"VolumeSnapshot\" in version \"snapshot.storage.k8s.io/v1\""}
```

Install [external-snapshotter](../external-snapshotter/README.md) first. The message names VolSync, but
the cause is that the cluster has no `VolumeSnapshot` type at all — common on Kind and on
self-managed clusters, where nothing installs the CSI snapshot controller by default.

---

[← Backup](../README.md)
