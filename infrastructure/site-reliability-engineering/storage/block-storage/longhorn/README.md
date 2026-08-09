[← Block storage](../README.md)

# Longhorn

<https://github.com/longhorn/longhorn>
<https://longhorn.io/docs/>
<https://artifacthub.io/packages/helm/longhorn/longhorn>

Chart values: <https://github.com/longhorn/longhorn/blob/master/chart/values.yaml>

---

## The problem it solves

You have a self-managed cluster, several nodes, and disks in those nodes. You need a PVC that
survives losing one of those nodes. There is no cloud provider to ask.

Longhorn turns the local disks of the nodes into **replicated block storage**. A PVC becomes a
volume with N replicas placed on N different nodes, written synchronously. Lose a node and the
volume is still readable from the others; Longhorn rebuilds the missing replica in the
background.

That is the entire pitch, and the reason it is the default recommendation for self-hosted block
storage: it does one thing, and it does it without requiring you to learn a distributed storage
system.

| Concern | How Longhorn answers it |
|---|---|
| Node loss | synchronous replicas on other nodes, automatic rebuild |
| Disk loss | same mechanism; the replica is rebuilt elsewhere |
| Snapshots | in-volume snapshots, plus CSI `VolumeSnapshot` |
| Backup | built in, to an S3-compatible target or NFS — off-cluster, which matters |
| Visibility | a UI that shows replica placement, rebuild progress and volume health |
| DR | volumes can be replicated to a second cluster |

Two of those deserve emphasis.

**The backup target is off-cluster.** Longhorn backs up volumes to S3 or NFS, incrementally, on
a schedule defined per volume or by `RecurringJob`. That is a genuine backup rather than a
snapshot sitting on the same disks as the data — the distinction that makes
[backup/](../../../backup/README.md) a separate folder.

**The UI is a real operational asset.** During an incident, "which replicas are healthy, where
are they, and how far along is the rebuild" is the question you need answered in seconds.
Longhorn shows it. Most storage systems make you assemble that from CLI output, and OpenEBS has
no equivalent.

### What it does not remove

Longhorn replicates the *volume*. It does not change what
[block storage](../README.md#12-the-failure-everyone-meets) is:

- Volumes are still `ReadWriteOnce`. Longhorn does offer an RWX mode, and it works by running an
  NFS server (share-manager) in front of the volume — which is [file storage](../../file-storage/README.md)
  with extra steps, and carries the same single-pod-in-the-write-path caveat.
- A node failure still means waiting for the volume to detach before the pod starts elsewhere.
  Replication protects the data, not the recovery time.

So the correct architecture is still: replicate in the application where possible, and use
Longhorn for the single-instance workloads that cannot.

## When to use it

- **Self-managed Kubernetes on-premise or on VMs**, where block PVCs must survive node loss and
  there is no provider CSI driver — this is the primary case, and Longhorn is the default answer.
- A **single-instance stateful workload** that cannot replicate itself: a lone PostgreSQL, a
  Redis with persistence, a Prometheus TSDB, an artifact store.
- Clusters where **operability matters more than peak performance**. The UI, the built-in
  backups and the small conceptual surface are worth real throughput compared to tuned local
  NVMe.
- When you want **snapshots and off-cluster backup without assembling three projects**. Longhorn
  ships the CSI snapshot support and the S3 backup target together.
- Edge and small clusters. Longhorn came out of Rancher's edge work and the resource footprint
  reflects that; it is far lighter than [Ceph](../../multi-storage/README.md).

## When not to use it

- **On a managed cloud cluster.** EBS and Azure Disk already replicate within a zone, under an
  SLA. Running Longhorn on top means replicating replicated storage and paying twice — see
  [cloud/](../../cloud/README.md).
- **Under a database that already replicates.** CloudNativePG with three instances, a Kafka
  broker set, a Cassandra ring: each replica has its own volume and the cluster heals itself.
  Longhorn underneath adds a network hop and 3× storage for a guarantee you already have. Use
  [OpenEBS Local PV](../openebs/README.md) instead.
- **For latency-critical workloads.** Every write goes over the network to N replicas before it
  is acknowledged. That is the cost of the guarantee, and it is not small.
- **To obtain `ReadWriteMany`.** The RWX mode is an NFS server in front of a volume; if RWX is
  the actual requirement, choose it deliberately in [file-storage/](../../file-storage/README.md).
- **On a single-node cluster, expecting durability.** Three replicas on one node are three copies
  on one disk. The API works; the guarantee does not exist.
- When there is **no spare disk**. Longhorn sharing the same devices as the workload means
  rebuild traffic and application I/O compete during exactly the incident it was installed for.

## Notes

The recorded note for this tool is the upstream repository, <https://github.com/longhorn/longhorn>.
Everything below is the operational context around it.

**How it is deployed here.** A Flux `HelmRelease` in the `longhorn` namespace, pinned to chart
version `1.7.2`, sourced from a `HelmRepository`. The values block is empty apart from a
commented-out `enablePSP`, which is a leftover: PodSecurityPolicy was removed in Kubernetes 1.25
and the setting no longer applies. Pinning is deliberate — a storage driver is the last component
that should upgrade unattended, because the upgrade path touches every attached volume.

**Prerequisites are easy to miss.** Longhorn needs `open-iscsi` installed and running on every
node, and `nfs-common` for the RWX mode. Missing them produces volumes stuck in attaching with
errors that point at the kubelet rather than at the package. Longhorn ships a
`longhorn-iscsi-installer` DaemonSet and an environment check script for this reason.

**Settings that matter more than the defaults suggest:**

| Setting | Why |
|---|---|
| Replica count | 3 is the useful default; 1 is a local volume with extra machinery |
| Replica node/zone anti-affinity | replicas on the same failure domain defeat the purpose |
| Data locality | keeping a replica on the pod's node removes the network from reads |
| Storage over-provisioning percentage | Longhorn thin-provisions; the default lets you oversubscribe the disk |
| Backup target | unset means no backups exist, and nothing warns you |
| `reclaimPolicy` on the StorageClass | the chart's default class is `Delete`; see [block-storage §3.2](../README.md#32-reclaimpolicy) |

The backup-target row is the one that bites. Longhorn installs cleanly, provisions volumes, and
reports healthy with no backup target configured at all. Snapshots taken without one live on the
same disks as the data.

**Version skew and upgrades.** Longhorn upgrades are a two-stage affair — the manager components,
then the engine images per volume — and volumes running an old engine image after an upgrade is a
common state. It is visible in the UI, and it is worth checking rather than assuming.

**In a Kind cluster** this is a demonstration. One node means every replica is on the same disk,
`open-iscsi` availability depends on the node image, and none of the failure behaviour can be
exercised. The value of having it here is the recorded decision for a real cluster, not the
running state — the same caveat that applies to [Rook](../../multi-storage/rook/README.md), with
a much smaller blast radius.

---

[← Block storage](../README.md)
