[← File storage](../README.md)

# NFS Ganesha server and external provisioner

<https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner>
<https://github.com/nfs-ganesha/nfs-ganesha>

Chart values: <https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner/blob/master/charts/nfs-server-provisioner/values.yaml>

Test manifests: [`test/`](test/README.md)

---

## The problem it solves

You need `ReadWriteMany` and every StorageClass in the cluster gives `ReadWriteOnce`. There is no
filer, no EFS, no Ceph, and adopting a distributed filesystem to solve one access-mode problem is
absurd.

`nfs-server-provisioner` **converts RWO into RWX**. That single sentence is the whole tool.

How it does it:

1. It runs a pod with **NFS Ganesha** — a userspace NFS server — inside it.
2. That pod claims one ordinary `ReadWriteOnce` PVC from whatever block storage you already have.
3. It exports subdirectories of that PVC over NFS.
4. It registers a StorageClass, so PVCs asking for `ReadWriteMany` get one of those
   subdirectories.

The result is a cluster where RWX works, built entirely from block storage you already had.

| Layer | What it is |
|---|---|
| Consumers | pods with RWX PVCs, on any node |
| Provisioner | watches PVCs, creates an export per claim |
| Ganesha | a **userspace** NFS server — no kernel NFS module needed |
| Backing store | one `ReadWriteOnce` PVC, on the block storage of your choice |

Ganesha running in userspace is what makes this possible at all: a kernel NFS server in a
container needs kernel modules and privileges that a normal cluster will not give it. Ganesha
needs neither, which is why this is packaged as an ordinary Helm chart.

### The cost, which is not hidden

**One pod is in the synchronous write path of everything that mounts it.**

| Event | Consequence |
|---|---|
| The pod restarts | every RWX mount in the cluster stalls, then recovers if clients are `hard`-mounted |
| The node holding it fails | the backing RWO PVC must detach first — minutes, per [block-storage §1.2](../../block-storage/README.md#12-the-failure-everyone-meets) |
| The backing PVC fills | every RWX consumer gets `ENOSPC` at the same moment |
| The backing PVC is lost | every RWX volume in the cluster is lost together |

Scaling the `StatefulSet` to more replicas does not fix this. Each replica is an independent NFS
server with its own backing PVC serving its own exports — it is sharding, not high availability.
A given volume still lives behind exactly one pod.

That is the honest trade: RWX for a single point of failure with a several-minute recovery. For a
shared config directory it is fine. For anything on the critical path it is not, and the answer
is a real filer, CephFS via [Rook](../../multi-storage/README.md), or
[cloud file storage](../../cloud/README.md).

### Capacity is real here, unlike most NFS provisioning

An unusual and useful property: because every export is a subdirectory of **one PVC of a known
size**, the total is genuinely bounded. That is stricter than
[`csi-driver-nfs`](../csi-driver-nfs/README.md) against a large filer, where the PVC size is
documentation.

It is bounded, not enforced per volume. One greedy consumer fills the shared PVC and everyone
else fails. Size the backing PVC for the sum, and alert on its free space — the individual PVC
sizes tell you nothing.

## When to use it

- **RWX is genuinely needed, on-premise, with no file server** — the primary case, and a
  legitimate one. Config directories, shared DAGs, a scratch space several pods write to.
- **Small clusters** where adding Ceph or a NAS is not proportionate to the problem.
- **Development and staging**, where a single point of failure is an acceptable trade for having
  RWX at all.
- **Migrating a legacy application** that hard-codes a filesystem path and expects several
  instances to see the same files, while the real fix is scheduled.
- **As a stepping stone.** It makes RWX available now, and it does not lock anything in — the
  consumers see an ordinary StorageClass.

## When not to use it

- **On a managed cloud cluster.** EFS and Azure Files provide RWX with no server, no single point
  of failure and an SLA. See [cloud/](../../cloud/README.md).
- **When an NFS server already exists.** Point [`csi-driver-nfs`](../csi-driver-nfs/README.md) at
  it and skip this entirely.
- **For anything whose availability matters.** One pod, one backing PVC, minutes to recover from
  a node failure.
- **For a database.** The standard rule: NFS locking and `fsync` semantics are not what any
  engine assumes.
- **For large or high-throughput data.** Everything funnels through one pod's network stack and
  one PVC's IOPS.
- **Believing more replicas means HA.** They shard; they do not fail over.
- **As the cluster's default StorageClass**, unless you have thought about it hard — see the
  Notes, because that is what this repository's values do.

## When not to confuse it with the other NFS folder

Both put NFS in the cluster, and they are different things:

| | `nfs-ganesha-server` (here) | [`csi-driver-nfs/nfs-server`](../csi-driver-nfs/nfs-server/README.md) |
|---|---|---|
| Nature | a packaged component with a chart and a StorageClass | a fixture copied from the driver's examples |
| Backing store | an ordinary RWO PVC | a `hostPath` on the node |
| Privileges | ordinary pod; Ganesha is userspace | `privileged: true` |
| Provisioning | dynamic, via its own provisioner | static PVs written by hand |
| Intended for | actual, if limited, use | testing the driver |

## Notes

The recorded notes for this tool are the two upstream repositories, and the pairing is the
point:

- **[`nfs-ganesha-server-and-external-provisioner`](https://github.com/kubernetes-sigs/nfs-ganesha-server-and-external-provisioner)**
  — the Kubernetes SIG project. The name is literal: it is *both* halves in one deployment, which
  is precisely what distinguishes it from [`csi-driver-nfs`](../csi-driver-nfs/README.md), where
  the server is someone else's problem. Note that it is an **external provisioner**, not a CSI
  driver — the older extension mechanism. In practice that means no CSI snapshot interface, no
  external-resizer, and no `VolumeSnapshot` path; back it up at file level with
  [Velero](../../../backup/velero/README.md) and Kopia or with
  [VolSync](../../../backup/volsync/README.md).
- **[`nfs-ganesha`](https://github.com/nfs-ganesha/nfs-ganesha)** — the NFS server itself, an
  independent project. Worth keeping visible because it explains the architecture: Ganesha is a
  userspace NFS server with pluggable backends (FSAL), which is why it can run in an unprivileged
  container and why it also turns up inside Ceph's NFS gateway and other storage products.

**How it is deployed here.** A Flux `HelmRelease` named `nfs-server-provisioner` in
`kube-system`, pinned to chart version `1.8.0`, with values worth reading carefully:

| Value | Set to | Comment |
|---|---|---|
| `persistence.enabled` | `true` | without this the backing store is `emptyDir` — **everything is lost on restart** |
| `persistence.storageClass` | `standard` | the backing RWO class |
| `persistence.size` | `4Gi` | the total capacity of every RWX volume in the cluster, combined |
| `storageClass.defaultClass` | **`true`** | makes this the **cluster default StorageClass** |
| `nodeSelector` | `agentpool: system` | an AKS-style node pool label |

Three observations.

**`persistence.enabled: true` is the single most important line.** The chart's default is an
`emptyDir`, so an unconfigured install produces an NFS server whose data vanishes when the pod
restarts — while behaving perfectly until then. Setting it is correct and setting it explicitly
is worth doing even where it is already the default.

**`defaultClass: true` deserves scrutiny.** It means every PVC in the cluster that does not name
a StorageClass lands on NFS, including databases, which is the exact opposite of what
[file-storage](../README.md#4-what-breaks-on-a-network-filesystem) recommends. Whether that is
intended depends on the cluster; in a repository whose sandbox default is
[local-path-provisioner](../../local/local-path-provisioner/README.md), it is a meaningful
override. If you take one thing from this file, make it this: **the default StorageClass should
be block storage**, and RWX should be requested by name.

**`nodeSelector: agentpool: system`** pins the server to an AKS system node pool. It is a
leftover from a real Azure deployment and will match nothing on Kind — which, given the previous
paragraph, is a benign accident. It is also a reminder that on AKS the better answer is Azure
Files; see [cloud/azure](../../cloud/azure/README.md).

**4Gi is small.** As the parent section notes, that number is the ceiling for every RWX volume in
the cluster added together, no matter what the individual PVCs claim. The
[`test/`](test/README.md) PVC requesting `1Mi` against it makes the arithmetic visible.

---

[← File storage](../README.md)
