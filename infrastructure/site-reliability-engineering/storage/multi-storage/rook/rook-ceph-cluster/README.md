[← Rook](../README.md)

# rook-ceph-cluster

<https://github.com/rook/rook>
<https://artifacthub.io/packages/helm/rook/rook-ceph-cluster>

Chart values: <https://github.com/rook/rook/blob/master/deploy/charts/rook-ceph-cluster/values.yaml>

Upstream examples: <https://github.com/rook/rook/tree/master/deploy/examples>

The second of the two [Rook](../README.md) deployment shapes. It requires
[`../rook-ceph/`](../rook-ceph/README.md) to be installed first.

---

## The problem it solves

[`rook-ceph`](../rook-ceph/README.md) installs an operator that understands `CephCluster` and
waits. This chart is what it waits for: **the actual Ceph cluster, and everything you consume from
it.**

What it creates:

| Resource | Effect |
|---|---|
| `CephCluster` | MON quorum, MGRs, and an **OSD per disk** — the cluster comes into existence |
| `CephBlockPool` | a RADOS pool, plus a StorageClass for **RBD** (`ReadWriteOnce`) |
| `CephFilesystem` | MDS daemons, plus a StorageClass for **CephFS** (`ReadWriteMany`) |
| `CephObjectStore` | RGW pods, plus an **S3-compatible** endpoint and a bucket StorageClass |
| Toolbox | optionally, the `ceph` CLI pod |
| Dashboard, monitoring | the Ceph dashboard and Prometheus rules |

This is where multi-storage stops being an idea. One `CephCluster` over one set of disks, and
three StorageClasses come out of it.

## What this shape adds over the simpler one

The comparison is the clearest way to understand why Rook ships two charts:

| | [`rook-ceph`](../rook-ceph/README.md) (operator) | `rook-ceph-cluster` (here) |
|---|---|---|
| Installs | CRDs, controller, CSI drivers | `CephCluster`, pools, filesystems, object stores |
| Consumes disks | none | **all of the ones you give it** |
| Stateful | no | **yes — this is the data** |
| Safe to reinstall | yes | **no** |
| Deleting it | breaks reconciliation, keeps the data | **can destroy the data** |
| Configuration | mostly defaults are fine | **every meaningful decision lives here** |
| Upgrade cadence | follows Rook releases | follows your data |

Three things follow from the "stateful" row, and they are the reason this shape needs its own
page.

**The values in this chart are the storage design.** Which nodes contribute disks, which devices,
replica counts, failure domains, whether CephFS and RGW exist at all, and what the StorageClasses
look like — all of it is here. An empty values block installs a cluster whose shape was chosen by
someone else.

**Deletion is dangerous.** `CephCluster` has a `cleanupPolicy` field, and Rook's finalizers exist
to stop an accidental removal from wiping OSD disks. A Helm uninstall or a Flux prune of *this*
release is not a routine operation — and after any cluster removal, the OSD disks must be wiped
before they can be reused, because Ceph refuses to adopt a device that still carries another
cluster's metadata. Rook's own uninstall documentation exists for a reason; read it before
needing it.

**Upgrades touch every OSD.** The Ceph image version is set here, not in the operator chart, and
changing it triggers a rolling restart of every daemon in the cluster. Upgrade Rook first, then
Ceph, and only between supported combinations.

### The three StorageClasses, and what they are for

| Source resource | StorageClass provides | Access mode | Use |
|---|---|---|---|
| `CephBlockPool` | RBD volumes | `ReadWriteOnce` | databases — see [block-storage](../../../block-storage/README.md) |
| `CephFilesystem` | CephFS volumes | **`ReadWriteMany`** | shared directories — see [file-storage](../../../file-storage/README.md) |
| `CephObjectStore` | S3 buckets, via `ObjectBucketClaim` | not a PVC | lakes, backups — see [object-storage](../../../object-storage/README.md) |

The middle row is the strongest self-hosted RWX option available, and the bottom row is a genuine
alternative to [MinIO](../../../object-storage/minio/README.md) for anyone already committed to
Ceph — worth remembering given the licence trajectory recorded in that folder.

Note that each additional shape costs daemons: CephFS needs MDS pods (memory-hungry, and you want
at least an active/standby pair), RGW needs gateway pods. Enable what you use.

## When to use it

- **After the operator, whenever Rook is deployed.** There is no storage without it.
- **When the cluster's storage design has actually been decided** — nodes, devices, replica
  counts, failure domains. That is what this chart's values express.
- **To add a shape later.** Enabling `CephFilesystem` or `CephObjectStore` on an existing cluster
  is a values change, which is the payoff of the whole multi-storage argument.
- In **external mode**, pointing at a Ceph cluster operated outside Kubernetes — you get the
  StorageClasses without Rook running any daemons.

## When not to use it

- **On a single node, expecting durability.** `replicated.size: 3` on one machine is three copies
  on one disk. See
  [multi-storage §3.3](../../README.md#33-a-single-node-demonstrates-the-api-and-none-of-the-properties).
- **With default values on real hardware.** The defaults will happily consume devices you did not
  intend to give it, or none at all.
- **Without capacity planning.** `size: 3` means usable capacity is one third of raw, and
  changing replication afterwards is a data migration.
- **Where it may be pruned by automation.** Flux prune, a namespace deletion, or a
  `helm uninstall` against this release is a data-loss event, not a rollback.
- **Before the CRDs exist.** Install [`rook-ceph`](../rook-ceph/README.md) first.
- **On a managed cloud cluster**, in the general case — see [cloud/](../../../cloud/README.md)
  and the recorded AKS exception in [the parent Notes](../README.md#notes).

## Notes

**How it is deployed here.** A Flux `HelmRelease` named `rook-ceph-cluster` in the `rook-ceph`
namespace, pinned to chart version `1.16.0`, from the `rook-release` `HelmRepository`, with an
empty values block and the upstream values file referenced in a comment.

**The empty values block is the significant fact about this folder.** For the operator chart,
defaults are defensible. For this one they are the storage design, deferred. A real deployment
starts by answering:

| Question | Values field |
|---|---|
| Which nodes and which devices? | `cephClusterSpec.storage` — `useAllNodes`, `useAllDevices`, `nodes`, `deviceFilter` |
| How many MONs? | `cephClusterSpec.mon.count` — **odd**, 3 or 5 |
| Which Ceph version? | `cephClusterSpec.cephVersion.image` |
| Which shapes are needed? | `cephBlockPools`, `cephFileSystems`, `cephObjectStores` |
| Replication and failure domain | per pool, in each of those lists |
| Which StorageClass is default? | `isDefault` on one of them |
| `reclaimPolicy` | per StorageClass — `Retain` for anything stateful, per [block-storage §3.2](../../../block-storage/README.md#32-reclaimpolicy) |
| Monitoring and dashboard | `monitoring.enabled`, `cephClusterSpec.dashboard` |
| The toolbox | `toolbox.enabled` — turn it on; it is how you inspect the cluster |

`useAllDevices: true` deserves a specific warning: it means exactly what it says, and on a node
with an unmounted disk holding something you cared about, Rook will consume it. Prefer explicit
device lists or a `deviceFilter` on real hardware.

**The `example/` folder holds a `CephBlockPool`**, identical to the one under
[`../rook-ceph/example/`](../rook-ceph/README.md):

- `failureDomain: host` — replicas on distinct hosts. Correct on a multi-node cluster; on one
  node it silently degenerates, because there is one host.
- `replicated.size: 3` — three copies; usable capacity is one third of raw.
- `hybridStorage` with `primaryDeviceClass: ssd` and `secondaryDeviceClass: hdd` — the primary
  copy on SSD for read latency, the rest on HDD for cost. This requires **device classes that
  exist in the CRUSH map**, which means genuinely mixed hardware; on uniform or virtual disks
  Ceph sees one class and the setting cannot be satisfied.

Applying it standalone is also a useful illustration of the ordering rule: a `CephBlockPool`
without a `CephCluster` has nothing to create a pool in.

Note that the chart can create pools through its own `cephBlockPools` values, which is the
GitOps-friendly path — a standalone CR alongside a chart that also manages pools is two owners
for one concern, and worth avoiding once the values are filled in.

**Snapshots work here**, which is not true of most of this repository's storage. Ceph-CSI
implements `CreateSnapshot` for RBD and CephFS, so `VolumeSnapshot` is real — provided the CRDs
and the snapshot controller are installed, which they are not by default. Rook's chart can create
the `VolumeSnapshotClass` resources; the controller itself comes from
[external-snapshotter](../../../../backup/external-snapshotter/README.md).

**In this repository this is a decision record, not a running system.** On a single Kind node the
chart reconciles and produces a cluster with none of Ceph's properties. What it captures is the
shape consolidated storage would take for the on-premise case in
[`on-premisse/`](../../../on-premisse/README.md) — and the values block being empty is an honest
signal that the design has not been committed to.

---

[← Rook](../README.md)
