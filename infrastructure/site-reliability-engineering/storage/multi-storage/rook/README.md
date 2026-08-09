[← Multi-storage](../README.md)

# Rook

<https://github.com/rook/rook>
<https://github.com/ceph/ceph>
<https://rook.io/docs/rook/latest/Getting-Started/intro/>

Upstream examples: <https://github.com/rook/rook/tree/master/deploy/examples>

Deployment shapes: [`rook-ceph/`](rook-ceph/README.md) — the operator and CRDs ·
[`rook-ceph-cluster/`](rook-ceph-cluster/README.md) — the cluster, pools and storage classes

---

## The problem it solves

Ceph gives you block, file and object storage from one cluster of disks. It is also famously
hard to install, configure and keep running, and its operational model — `ceph-deploy`,
`cephadm`, systemd units, a monitor quorum, OSDs bound to physical devices — has nothing in
common with how Kubernetes expects to manage anything.

**Rook is a Kubernetes operator for Ceph.** It does not reimplement storage; Ceph does all of
it. Rook translates custom resources into Ceph configuration, runs the daemons as pods, and
reconciles the gap continuously.

| You declare | Rook produces |
|---|---|
| `CephCluster` | MONs, MGRs, and an OSD per discovered device |
| `CephBlockPool` | a RADOS pool and a StorageClass for **RBD** — `ReadWriteOnce` PVCs |
| `CephFilesystem` | MDS daemons and a StorageClass for **CephFS** — `ReadWriteMany` PVCs |
| `CephObjectStore` | RGW pods and an **S3-compatible** endpoint |
| `CephObjectStoreUser` | S3 credentials, delivered as a Secret |
| `CephBlockPoolRadosNamespace`, `CephNFS`, … | the rest of Ceph's surface, as CRDs |

That table is the whole value proposition: three storage shapes, one set of disks, declared in
YAML and reconciled by a controller. Disk discovery, OSD provisioning, rolling upgrades and
daemon replacement stop being runbooks.

### What Rook does not do

**Rook does not make Ceph simple. It makes Ceph declarative.**

The distinction matters because it sets expectations for the day something breaks. Placement
groups, CRUSH rules, pool sizing, `HEALTH_WARN` states, backfill throttling, OSD flapping — all
of Ceph's concepts are still there, still yours to understand, and the operator will not diagnose
them for you. What you get is a cluster whose *desired state* is in Git; what you still need is
someone who can read `ceph status` and act on it.

The related consequence: **the `toolbox` pod is not optional.** Rook ships a
`rook-ceph-tools` deployment giving you a shell with the `ceph` CLI against the cluster. It is
the primary diagnostic interface, and a Rook installation without it is a Ceph cluster you cannot
inspect.

### The coupling that consolidation buys

Ceph is a quorum system. **Losing MON quorum stops everything** — RBD volumes, CephFS mounts and
the S3 endpoint, simultaneously — no matter how healthy the OSDs are.

That is a stronger failure coupling than running three separate systems, and it is the central
risk of the multi-storage bet. Three independent tools ([Longhorn](../../block-storage/longhorn/README.md),
an NFS export, [MinIO](../../object-storage/minio/README.md)) fail independently. Ceph fails as
one thing. Whether that is a good trade depends on how much you value one upgrade path over three
blast radii.

## When to use it

- **On-premise, on real hardware**: three or more nodes, dedicated raw disks, a network designed
  rather than inherited. This is the case Ceph was built for.
- **When all three shapes are genuinely needed** — block for databases, RWX for shared
  directories, S3 for a lake or for observability chunks — and running three systems is the
  alternative being weighed.
- **When CephFS is the RWX requirement.** It is the strongest self-hosted `ReadWriteMany` option
  available, better than anything in [file-storage/](../../file-storage/README.md).
- **When RGW is wanted as an S3 endpoint**, which is worth knowing given the licence trajectory
  recorded in [object-storage/](../../object-storage/README.md).
- **At scale.** Hundreds of terabytes upward, where the operational cost is amortised against
  something.
- **When there is someone who can operate Ceph.** This is a precondition, not a nice-to-have.

## When not to use it

- **On a single node or a Kind cluster, expecting anything.** The CRDs reconcile, a PVC binds,
  the dashboard loads, and every property Ceph exists for is absent — see
  [multi-storage §3.3](../README.md#33-a-single-node-demonstrates-the-api-and-none-of-the-properties).
- **On a managed cloud cluster**, in the general case. EBS, EFS and S3 already provide all three
  shapes under an SLA; Ceph on top means replicating replicated storage at 3× cost and full
  operational burden. See [cloud/](../../cloud/README.md), and see the Notes for the one recorded
  exception and why it existed.
- **To obtain one access mode.** Adopting a distributed storage system because an application
  wants RWX is a very large lever for a small problem. NFS first.
- **Without dedicated raw disks.** OSDs on volumes from another storage layer stack two
  replication schemes and two failure models.
- **On small clusters or small data.** Below a few terabytes the overhead dominates every
  benefit.
- **Without capacity planning for replication.** `size: 3` means usable capacity is one third of
  raw, and it cannot be changed afterwards without a data migration.
- **Without someone to operate it.** A Ceph cluster nobody understands is a liability with a
  dashboard.

## Notes

The recorded notes for this tool, preserved and explained.

**<https://github.com/rook/rook>** — the operator. CNCF graduated. Note that Rook once supported
several storage backends (EdgeFS, Cassandra, NFS, YugabyteDB); **all of them were removed**, and
Rook today is a Ceph operator exclusively. Older articles describing Rook as a
"storage-orchestrator for many providers" are describing a project that no longer exists, and
that is a live source of confusion when reading anything more than a few years old.

**<https://github.com/ceph/ceph>** — Ceph itself, kept visible deliberately. The most useful
mental correction when working with Rook is that **you are running Ceph**, and the documentation
that answers a real production question is usually Ceph's, not Rook's. When a pool is
`HEALTH_WARN` or PGs are stuck, the answer is in Ceph's docs.

**<https://github.com/rook/rook/tree/master/deploy/examples>** — the upstream example directory,
and the most practically valuable link here. It contains the reference manifests for every CRD:
`cluster.yaml`, `cluster-test.yaml` (the single-node variant), `filesystem.yaml`,
`object.yaml`, `toolbox.yaml`, and the storage class definitions under `csi/`. Two habits worth
adopting: read the examples for the **exact Rook version** you are running, since CRD fields
change across releases, and use `toolbox.yaml` from there rather than inventing one.

**"High Performance Shared File storage on AKS with Rook" —
<https://github.com/evillgenius75/rook-aks>.** Preserved as recorded, and it deserves a plain
comment because it sits in tension with the advice above.

The scenario it addresses is real: on AKS, `ReadWriteMany` means Azure Files, and Azure Files —
over SMB especially — has per-operation latency that makes metadata-heavy workloads painful. See
[cloud/azure](../../cloud/azure/README.md). Running CephFS on AKS, over local NVMe on the node
pool, is a way to get much faster shared file storage than the managed service provides.

So the honest position is: **"do not run Ceph on a managed cluster" is a default, not a law**, and
this is the shape of the exception — a specific, measured performance requirement that the
managed service cannot meet. What it is not is a reason to reach for Rook on AKS generally. If
Azure Files with NFS v4.1 on Premium is fast enough, that remains the right answer, and the
question to settle first is whether the workload's RWX requirement is real at all
([file-storage §1.2](../../file-storage/README.md#12-ask-whether-you-need-it-first)). Treat this
link as a documented precedent for a narrow case, and check its age before following its
configuration.

**How it is deployed here.** Two Flux `HelmRelease` objects, both pinned to chart version
`1.16.0`, both in the `rook-ceph` namespace, matching Rook's own two-chart split:

| Shape | Chart | Role |
|---|---|---|
| [`rook-ceph/`](rook-ceph/README.md) | `rook-ceph` | the operator and the CRDs |
| [`rook-ceph-cluster/`](rook-ceph-cluster/README.md) | `rook-ceph-cluster` | the `CephCluster`, pools and storage classes |

The order is not optional — the CRDs must exist before any `Ceph*` resource can be created. Both
folders carry an identical `CephBlockPool` example with `failureDomain: host`,
`replicated.size: 3` and a `hybridStorage` block mapping the primary copy to SSD and the rest to
HDD.

`failureDomain: host` with three replicas on a Kind cluster is exactly the case described above:
three copies of every object on one machine's disk, and a `hybridStorage` device-class split
across device classes that do not exist. The manifests are correct and the guarantees are
absent — which is the point [multi-storage](../README.md) makes, and the reason this folder is a
decision record rather than a running system.

**Snapshots.** Ceph-CSI implements `CreateSnapshot` for both RBD and CephFS, so
`VolumeSnapshot` genuinely works here — provided the CRDs and the snapshot controller are
installed, which they are not by default. See
[external-snapshotter](../../../backup/external-snapshotter/README.md).

---

[← Multi-storage](../README.md)
