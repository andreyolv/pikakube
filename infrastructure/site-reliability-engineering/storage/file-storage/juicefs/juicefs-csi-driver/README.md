[← JuiceFS](../README.md)

# JuiceFS CSI driver

<https://github.com/juicedata/juicefs-csi-driver>
<https://juicefs.com/docs/csi/introduction>

Chart values: <https://github.com/juicedata/charts/blob/main/charts/juicefs-csi-driver/values.yaml>

The PVC-facing shape of [JuiceFS](../README.md). Its counterpart is
[`../juicefs-s3-gateway/`](../juicefs-s3-gateway/README.md).

---

## The problem it solves

[JuiceFS](../README.md) is a filesystem you mount. The CSI driver is what turns that into
something Kubernetes understands: a StorageClass, PVCs that bind, and `ReadWriteMany` volumes
mounted into pods on any node.

Without it you would run `juicefs mount` on every node by hand and reference host paths — which
is how the FUSE-mount-in-a-DaemonSet pattern usually ends, and it is worse in every respect.

What the driver does:

| Job | Detail |
|---|---|
| Dynamic provisioning | a PVC becomes a **subdirectory** of one JuiceFS filesystem |
| Static provisioning | a PV bound to a specific existing subdirectory |
| RWX | the reason to be here; any number of pods, any number of nodes |
| Mount lifecycle | starts and stops the FUSE mount that backs each volume |
| Cache management | per-node local disk cache, which is where the performance comes from |

### Mount pod versus sidecar, and why it matters

This is the driver's one genuinely important configuration decision, and it is unusual enough to
be worth understanding before deploying.

The FUSE mount has to live somewhere. The driver offers two placements:

| Mode | Where the mount runs | Consequence |
|---|---|---|
| **Mount pod** (default) | a **separate pod** per (node, volume), managed by the driver | one mount shared by every pod using that volume on that node |
| **Sidecar** | an injected container inside each application pod | mount lifetime matches the pod exactly |

Mount pod mode is the default and is normally right: one mount serves many consumers, and the
cache is shared. It has one behaviour that surprises people — **if the mount pod is killed, every
application pod using that volume on that node loses its mount**, and processes see I/O errors on
a directory that was working a moment ago. The driver recreates the mount pod and can recover the
mount, but in-flight file descriptors do not always survive.

Sidecar mode avoids the shared-fate problem at the cost of one FUSE process and one cache per
application pod, which multiplies memory and cache usage. It exists mainly for environments
where a privileged mount pod is not acceptable.

The practical instruction: **the mount pods are part of your production topology.** They appear
in the driver's namespace, they need resource requests, and they should not be casually deleted
during a cleanup.

## What this shape adds over the simpler one

Compared to [`../juicefs-s3-gateway/`](../juicefs-s3-gateway/README.md), which serves the same
filesystem over HTTP:

| | CSI driver (here) | [S3 gateway](../juicefs-s3-gateway/README.md) |
|---|---|---|
| Interface | a mounted directory — a PVC | an S3 API endpoint |
| Consumer | anything that reads files | anything that speaks S3 |
| Runs as | controller + node DaemonSet + mount pods | an ordinary Deployment |
| Needs privileges | yes — FUSE mounts on the node | no |
| Node coupling | mounts on each node that uses it | none; it is just a service |
| POSIX semantics | yes, including locking | no — it is object storage again |

They are not alternatives so much as two doors into the same data, and running both is normal:
legacy applications get PVCs, modern ones get an S3 endpoint, and both see the same files.

## When to use it

- **Whenever JuiceFS is used from Kubernetes at all** and pods need it as a filesystem. This is
  the primary shape.
- **Large shared datasets read by many pods** — the per-node cache means the second reader on a
  node does not go back to object storage.
- **Migrating an application that expects a filesystem** onto object-storage economics without
  changing the application.
- **When RWX with real POSIX locking is needed**, which NFS provides less reliably.

## When not to use it

- **Without the metadata engine question answered.** The driver inherits every property of
  [JuiceFS](../README.md#the-metadata-engine-is-a-hard-dependency-and-a-single-point-of-failure),
  including that a lost metadata database is a lost filesystem. The driver makes it easy to
  provision volumes on top of a Redis nobody is backing up.
- **For a database, a queue, or anything with a write-ahead log.** POSIX compliance is not the
  same as local-disk semantics.
- **For latency-sensitive small-file access.** Every metadata call is a database round trip.
- **In clusters that forbid privileged pods.** FUSE needs mount privileges; sidecar mode reduces
  but does not eliminate the requirement.
- **When a simpler RWX answer exists** — an NFS export via
  [csi-driver-nfs](../../csi-driver-nfs/README.md), or
  [EFS/Azure Files](../../../cloud/README.md) on a managed cluster.

## Notes

**How it is deployed here.** A Flux `HelmRelease` named `juicefs-csi-driver` in the `juicefs`
namespace, pinned to chart version `0.28.4`, from the `juicefs` `HelmRepository`
([`juicedata/charts`](https://github.com/juicedata/charts)).

The values define one StorageClass:

| Field | Value here |
|---|---|
| `name` | `juicefs-sc` |
| `backend.name` | `<name>` |
| `backend.metaurl` | `<meta-url>` |
| `backend.storage` | `<storage-type>` |
| `backend.bucket` | `<bucket>` |
| `backend.accessKey` / `secretKey` | `<access-key>` / `<secret-key>` |

**Every backend value is a placeholder, and that is the correct state for this repository.** The
metadata engine URL and the bucket are the two deployment-specific decisions in all of JuiceFS —
there is no sensible default for either, and committing real ones would be committing a design
this repository has not made. See
[the parent README](../README.md#choosing-the-metadata-engine) for how to choose them.

**`metaurl` is a credential.** It is a connection string — `redis://user:password@host:6379/1`,
`postgres://user:password@host/db` — carrying the password to the database that *is* the
filesystem. When these placeholders become real values they belong in a Kubernetes Secret
referenced by the chart, never inline in a `HelmRelease` committed to Git. The same applies to
`accessKey` and `secretKey`. The chart supports both `backend` (which creates a Secret for you)
and pointing at an existing Secret; prefer the latter, or a SOPS/SealedSecrets-style flow
consistent with the rest of the repository.

**`storage` names the object-storage type** — `s3`, `minio`, `oss`, `gs`, `wasb`, and so on —
and it changes how `bucket` is interpreted. Against
[MinIO](../../../object-storage/minio/README.md) the bucket value is a full URL including the
endpoint, not a bare bucket name. That mismatch is a common first-attempt failure.

**Formatting happens once.** A JuiceFS filesystem must be `format`ted against its metadata engine
and bucket before it can be mounted; the chart's `backend` block does this on first use. The
important consequence is that **the format parameters — chunk size, compression, encryption,
block size — are fixed at format time** and cannot be changed later without creating a new
filesystem and copying. That puts them in the same category as `storageClassName` and
`accessModes` in [storage §3](../../../README.md#3-the-immutable-fields-that-trap-you): decide
once, at the start.

**What gets installed.** The usual CSI shape described in
[block-storage §2](../../../block-storage/README.md#2-the-csi-model) — a controller Deployment
with the provisioner sidecar, and a node DaemonSet with the registrar — plus the mount pods
described above, which are specific to this driver and are the part that is easy to overlook when
capacity-planning a node.

**Caching is where the performance is.** The node-local cache directory and its size are the
settings that decide whether this feels like a filesystem or like HTTP. The default cache path
lives on the node's root filesystem, which is rarely what you want on a real node — point it at a
dedicated disk and size it against the working set. Also budget for it: an aggressive cache on
every node is real disk consumption that nothing in the PVC objects accounts for.

---

[← JuiceFS](../README.md)
