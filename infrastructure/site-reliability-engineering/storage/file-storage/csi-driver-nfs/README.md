[← File storage](../README.md)

# csi-driver-nfs

<https://github.com/kubernetes-csi/csi-driver-nfs>
<https://github.com/kubernetes-csi/csi-driver-smb>

Chart values: <https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/charts/latest/csi-driver-nfs/values.yaml>

Upstream examples: <https://github.com/kubernetes-csi/csi-driver-nfs/tree/master/deploy/example>

Deployment shapes: [`nfs-server/`](nfs-server/README.md) — an in-cluster NFS server to point it at

---

## The problem it solves

There is an NFS server. It has been there for years, the storage team runs it, and it is not
going anywhere. Pods need to mount it, and they need PVCs rather than hand-written mount
commands.

`csi-driver-nfs` is that bridge and nothing else. **It stores no data.** It is a CSI driver that:

- mounts an existing NFS export into pods, and
- turns each PVC into a **subdirectory** of that export, created on demand.

| It does | It does not |
|---|---|
| dynamic provisioning — one subdirectory per PVC | store bytes, or manage a server |
| static provisioning — bind a PV to a specific share | create the export, or set quotas |
| `ReadWriteMany`, which is the whole point | enforce the PVC's requested size |
| mount options per StorageClass (`nfsvers`, `hard`, `noatime`) | snapshots on most setups |

That separation is the thing to hold on to, and it is why this folder and
[`nfs-ganesha-server/`](../nfs-ganesha-server/README.md) both exist:

| Question | Answer |
|---|---|
| Who stores the bytes? | **the server** — a filer, a Linux box, or a pod |
| Who turns a PVC into a mount? | **the CSI driver** — this |

If a server already exists, this is all you need. If one does not, you need to run one first, and
that is a different decision with different consequences.

### What "the PVC size is not enforced" means

The driver creates a directory. A directory has no size. The PVC says `10Gi` because Kubernetes
requires a number, and the actual limit is whatever the export has left.

Consequences:

- Ten PVCs of 10Gi each on a 20 GiB export will all bind, and all appear healthy, until the
  export fills.
- When it fills, **every workload on that export fails at once**, with `ENOSPC` from writes that
  had no reason to expect it.
- Expanding the PVC changes a number and nothing else.

Monitor free space on the server. The Kubernetes objects will not tell you.

### Access modes and reclaim

`ReadWriteMany` is what this is for, and it is the reason
[file-storage](../README.md#1-rwx-is-the-entire-reason-this-folder-exists) exists as a folder.
Note that RWX makes concurrent mounting possible; it does not make concurrent writing safe, and
NFS locking is the weakest part of the protocol.

`reclaimPolicy: Delete` here means **recursively deleting a directory tree** on a shared server.
It is quieter than destroying a block volume and exactly as permanent. `Retain` for anything that
matters — the driver supports it, and there is also an `onDelete` parameter that can archive
rather than remove.

Snapshots generally do not work. The driver has some support that depends on the setup, and the
realistic backup path for NFS-backed volumes is file-level:
[Velero](../../../backup/velero/README.md) with Kopia, or
[VolSync](../../../backup/volsync/README.md).

## When to use it

- **An NFS server already exists.** This is the primary case and the strongest one — a NetApp,
  an Isilon, a TrueNAS box, a Linux host with `/etc/exports`. Nothing new to operate.
- **RWX is genuinely required** after asking the questions in
  [file-storage §1.2](../README.md#12-ask-whether-you-need-it-first) and the answer survived.
- **On-premise clusters** where the storage layer is not Kubernetes-shaped and should not become
  Kubernetes-shaped.
- **In front of an in-cluster NFS server** for development and testing — which is exactly what
  [`nfs-server/`](nfs-server/README.md) here is.
- As a replacement for `nfs-subdir-external-provisioner` in existing clusters; see the Notes.

## When not to use it

- **When no NFS server exists.** The driver does not create one. Either run one
  ([`nfs-ganesha-server`](../nfs-ganesha-server/README.md)) and accept the single point of
  failure, or use storage that provides RWX natively.
- **For a database.** NFS locking and `fsync` semantics are not what any database engine assumes,
  and the corruption is silent. This is the rule that matters most in this folder.
- **On a managed cloud cluster** — EFS and Azure Files provide managed RWX with no server. See
  [cloud/](../../cloud/README.md).
- **Assuming the PVC size is a quota.** It is documentation. Enforce it on the server if you need
  it enforced.
- **For latency-sensitive or metadata-heavy workloads** — every `stat` and `readdir` is a network
  round trip.
- **Expecting `VolumeSnapshot` to be your backup story.** Plan file-level backup from the start.

## Notes

The recorded notes for this tool, translated where needed, preserved and explained:

**"Kubernetes generic, using existing on-premise NFS/SMB."** This is the positioning, and it is
exactly right: the driver's purpose is to consume storage that already exists rather than to
provide any. It comes in two flavours:

| Driver | Protocol | Use |
|---|---|---|
| [`csi-driver-nfs`](https://github.com/kubernetes-csi/csi-driver-nfs) | NFS | Linux-native shares; the default |
| [`csi-driver-smb`](https://github.com/kubernetes-csi/csi-driver-smb) | SMB / CIFS | Windows file servers, or Azure Files in SMB mode |

`csi-driver-smb` is the same project family and the same model, pointed at a Windows-shaped
world. It is the answer when the existing on-premise file server is a Windows file server, which
in a lot of enterprises it is. It carries the same uid/gid mapping friction described in
[cloud/azure](../../cloud/azure/README.md).

**[`nfs-subdir-external-provisioner`](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)
— old; `csi-driver-nfs` is newer.** Preserved verbatim because it is a decision, not a
footnote. The subdir provisioner is the widely-copied predecessor: it does the same
subdirectory-per-PVC trick, but as an external provisioner rather than a CSI driver, which means
no CSI ecosystem integration — no snapshot interface, no resizer, no standard topology handling
— and it is in maintenance. It appears in an enormous number of blog posts and Stack Overflow
answers, which is precisely why the note exists. **For new work, use `csi-driver-nfs`.**

**The upstream examples**, kept as links because they are the fastest way to a working test:

- <https://github.com/kubernetes-csi/csi-driver-nfs/blob/master/deploy/example/nfs-provisioner/nfs-server.yaml>
  — the in-cluster NFS server manifest, which is what the [`nfs-server/`](nfs-server/README.md)
  folder here is adapted from.
- <https://github.com/kubernetes-csi/csi-driver-nfs/tree/master/deploy/example> — the full
  example set: StorageClass, dynamic and static PVCs, and the `volumeHandle` format that static
  provisioning needs.

**`local-path-provisioner` with `accessMode: ReadWriteMany`** —
<https://github.com/rancher/local-path-provisioner/blob/master/examples/shared-fs/pvc.yaml>.
Recorded here as an alternative, and it needs a plain caveat because the example is easy to
misread. [local-path-provisioner](../../local/local-path-provisioner/README.md) can serve an RWX
PVC, and what that means is that **several pods on the same node** share a directory on that
node's disk. It is not shared across nodes, because there is nothing shared about it — no server,
no protocol, no network. On a single-node cluster (Kind, k3s on a laptop) it looks identical to
real RWX and behaves identically. On a multi-node cluster it silently is not RWX at all. Useful
for development; never a substitute for this driver.

**How it is deployed here.** A Flux `HelmRelease` named `csi-driver-nfs` in `kube-system`, pinned
to chart version `4.11.0`, with an empty values block. `kube-system` is the conventional
namespace for CSI drivers — they are cluster infrastructure, and the node plugin is a DaemonSet
that needs privileged mounts regardless.

The chart installs the usual CSI shape described in
[block-storage §2](../../block-storage/README.md#2-the-csi-model): a controller Deployment with
the provisioner and resizer sidecars, and a node DaemonSet with the driver registrar. It does
**not** create a StorageClass by default — the server address and share path are deployment
specific, so that is left to you, and a driver installed with no StorageClass is a common reason
for "the driver is running but nothing binds".

**In this repository the driver is paired with an in-cluster server**, which is a test fixture
rather than a design — see [`nfs-server/`](nfs-server/README.md) for what that is and why it is
not something to copy into production.

---

[← File storage](../README.md)
