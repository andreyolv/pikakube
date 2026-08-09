[← csi-driver-nfs](../README.md)

# In-cluster NFS server

<https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/deploy/example/nfs-provisioner/nfs-server.yaml>
<https://github.com/kubernetes-csi/csi-driver-nfs/tree/master/deploy/example>
<https://hub.docker.com/r/itsthenetwork/nfs-server-alpine>

The test target for [`csi-driver-nfs`](../README.md) — a server to point the driver at when no
real one exists.

---

## The problem it solves

[`csi-driver-nfs`](../README.md) stores nothing. It needs an NFS server, and in a sandbox there
is not one.

This folder supplies the missing half: a single pod exporting a directory over NFS, plus a
Service so the driver can reach it by DNS name, plus a small nginx workload that mounts the
result and proves the whole chain works.

That chain is worth naming, because it is the thing being demonstrated:

```
nginx pod
  → PVC  (pvc-nginx)
    → PV  (pv-nginx, csi driver nfs.csi.k8s.io)
      → Service  (nfs-server.nfs-server.svc.cluster.local)
        → NFS server pod
          → hostPath on the node
```

Five hops to reach a directory on the node's disk. That is not a criticism — it is exactly what
makes it a useful demonstration, because every one of those hops exists in a real deployment too,
with only the last two replaced by a real filer.

## What this shape adds over the simpler one

The parent folder installs the driver. This folder adds **the storage the driver has no opinion
about**, and the contrast is the lesson:

| | [`csi-driver-nfs`](../README.md) (parent) | `nfs-server/` (here) |
|---|---|---|
| Installed as | a Flux `HelmRelease`, pinned chart | plain manifests |
| Role | mount an existing export as PVCs | **be** the export |
| Durability | inherited from the server | a `hostPath` on one node |
| Production shape | yes — point it at a real filer | **no** |
| Needed when | a server already exists | nothing else provides NFS |

The other shape of "run your own NFS server" is
[`nfs-ganesha-server`](../../nfs-ganesha-server/README.md), and the difference is real: Ganesha's
provisioner is a Helm-installed, PVC-backed, StorageClass-providing component intended for actual
use, whereas this is a single privileged pod on a `hostPath` copied from the driver's example
directory. Both put one pod in the write path of everything that mounts them; only one of them is
trying to be a product.

## When to use it

- **Testing the driver.** Confirming that `csi-driver-nfs` is installed, that a StorageClass or
  static PV binds, and that a pod can actually write to it.
- **Local development on Kind**, where an NFS export is needed and there is no server to borrow.
- **Learning the static-provisioning path.** The PV here spells out the `volumeHandle` format,
  which is the part of static NFS provisioning people get wrong.
- **CI**, where a disposable RWX target is needed for an integration test.

## When not to use it

- **For any data you would miss.** A single pod, no replicas, `hostPath` storage, no backup. When
  the node goes, so does everything.
- **In production, in any form.** One pod is in the synchronous write path of every workload that
  mounts it. It is not a service, it is a fixture.
- **As a template for a production NFS server.** `securityContext.privileged: true` and a
  `hostPath` mount are what make it work in a sandbox and what make it unacceptable outside one.
- **To decide whether RWX is right for a workload.** On a single node it will look fast and
  behave well; on a real network filesystem across real nodes it will not.

## Notes

**What is deployed here.**

| Object | Detail |
|---|---|
| `Namespace` | `nfs-server` |
| `Deployment` | `nfs-server`, 1 replica, image `itsthenetwork/nfs-server-alpine:latest`, `nodeSelector: kubernetes.io/os=linux` |
| `Service` | exposes TCP 2049 (NFS) and UDP 111 (rpcbind) |
| `PersistentVolume` | `pv-nginx`, 10Gi, `ReadWriteOnce`, CSI driver `nfs.csi.k8s.io` |
| `PersistentVolumeClaim` | `pvc-nginx`, 10Gi, bound explicitly by `volumeName` |
| `Pod` | an nginx pod mounting the PVC |

The server container runs with `SHARED_DIRECTORY=/exports`, backed by a `hostPath` volume at
`/nfs-vol` with `type: DirectoryOrCreate` — the manifest carries an upstream comment noting that
this path is the thing to change.

**`privileged: true` is not optional here.** An NFS server needs to bind privileged ports and
manipulate kernel NFS state, so the container runs privileged. That is one of the two reasons
this is a fixture rather than a deployment — a privileged pod is a meaningful escalation path, and
any Pod Security admission policy above `privileged` will reject it.

**The `hostPath` at `/nfs-vol` is the other reason.** As covered in
[local/](../../../local/README.md), a `hostPath` volume has no node affinity and no durability.
If this Deployment is rescheduled to a different node, it starts serving an empty directory, and
every PVC mounted from it appears to have lost its data — with no error anywhere. On a
single-node Kind cluster that cannot happen, which is exactly why the pattern survives in
examples.

**The `volumeHandle` format is the interesting part of the PV.** The manifest carries the
upstream comment:

> `volumeHandle` format: `{nfs-server-address}#{sub-dir-name}#{share-name}` — make sure this
> value is unique for every share in the cluster

and uses `nfs-server.nfs-server.svc.cluster.local/share##` with `server` and `share: /` in
`volumeAttributes`, plus `mountOptions: [nfsvers=4.1]`. Two things worth extracting:

- **Uniqueness is load-bearing.** The CSI spec treats `volumeHandle` as the volume's identity.
  Two PVs sharing one handle produce attach and detach behaviour that is very hard to diagnose,
  because Kubernetes believes they are the same volume.
- **`nfsvers=4.1`** is the mount option that decides protocol behaviour, including how locking
  works. It belongs on the StorageClass or PV, not left to the client default.

**The nginx PVC asks for `ReadWriteOnce`, not `ReadWriteMany`** — and it also sets
`storageClassName: ""` with an explicit `volumeName`, which is the correct way to bind a claim to
one specific pre-created PV and stop the default StorageClass from provisioning something else.
The RWO access mode on an NFS-backed volume is a little odd given that RWX is the reason to use
NFS at all; it works because access modes are declarations that Kubernetes enforces, not
capabilities it discovers. For a single test pod it makes no difference. For anything real,
declare RWX, because the field is **immutable** and changing it later means a new PVC.

**The 10Gi is fiction**, in the sense described in
[the parent README](../README.md#what-the-pvc-size-is-not-enforced-means): the driver creates a
directory, and the real limit is whatever the node's disk has left under `/nfs-vol`.

**Upstream is the source.** This is adapted from the driver's own example directory, linked at
the top. When the driver version changes, check those examples rather than assuming these
manifests still match — particularly the `volumeHandle` format, which has changed shape across
driver versions.

---

[← csi-driver-nfs](../README.md)
