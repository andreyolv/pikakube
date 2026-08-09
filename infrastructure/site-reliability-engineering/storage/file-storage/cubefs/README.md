[← File storage](../README.md)

# CubeFS

<https://github.com/cubefs/cubefs>
<https://github.com/cubefs/cubefs-helm>
<https://cubefs.io/docs/master/overview/introduction.html>

---

## The problem it solves

You need a distributed filesystem — real `ReadWriteMany` at scale, across many nodes, with
replication and no single server in the write path — and the two obvious answers are both
unattractive. NFS is one box. [Ceph](../../multi-storage/README.md) is a large operational
commitment.

CubeFS is a CNCF **graduated** distributed storage system that occupies the space between them.
It came out of JD.com, runs at that scale, and provides both a POSIX filesystem and an
S3-compatible object interface from the same cluster.

Its architecture is worth knowing because it explains the behaviour:

| Component | Role |
|---|---|
| **Master** | metadata about the cluster itself — nodes, volumes, partitions. Raft-replicated, so an odd number |
| **MetaNode** | the filesystem metadata — the directory tree, inodes. **In memory**, Raft-replicated |
| **DataNode** | the actual file contents, in replicated or erasure-coded partitions |
| **ObjectNode** | the S3-compatible gateway |
| **Client** | a FUSE mount, or the CSI driver in Kubernetes |

Two design choices set it apart from Ceph.

**Metadata is in memory and horizontally sharded.** Where Ceph's CephFS uses MDS daemons over
RADOS, CubeFS puts filesystem metadata in dedicated MetaNodes that hold it in RAM and shard it
across many of them. That makes metadata operations — `stat`, `readdir`, `create` — fast, which
is the operation class where network filesystems normally hurt, and it means metadata capacity
scales by adding MetaNodes rather than by growing one server's heap. The cost is RAM, and the
usual caveat about in-memory metadata: it is Raft-replicated and persisted, but the sizing
question is memory, not disk.

**Two storage engines, chosen per volume.** A multi-replica engine for latency-sensitive data,
and a blobstore/erasure-coded engine for capacity-efficient cold data. That is a per-volume
decision rather than a cluster-wide one.

### Where it sits against the alternatives

| | CubeFS | [Ceph/Rook](../../multi-storage/README.md) | [JuiceFS](../juicefs/README.md) | [NFS](../csi-driver-nfs/README.md) |
|---|---|---|---|---|
| Stores data itself | yes | yes | **no** — uses object storage |
| External dependency | none | none | **object store + metadata database** |
| Block (RWO) | no | **yes** (RBD) | no | no |
| File (RWX) | yes | yes (CephFS) | yes | yes |
| S3 | yes | yes (RGW) | yes (gateway) | no |
| Operational weight | high | **highest** | medium, moved onto the metadata DB |
| Community outside China | **modest** | very large | growing | universal |

The row that decides most evaluations is the last one. CubeFS is technically credible — CNCF
graduation is not given away, and the scale it runs at is real — but the pool of people who have
operated it, the volume of English-language troubleshooting material, and the odds that the next
engineer has seen it are all much smaller than for Ceph or NFS. For a component whose failure
mode is "the filesystem is unavailable", that is a legitimate part of the decision rather than
snobbery.

Note also what it does **not** do: no block volumes. If RWO for databases is also needed, CubeFS
is not a one-system answer, and [Rook/Ceph](../../multi-storage/README.md) is the folder for
that.

## When to use it

- **Large-scale on-premise RWX**, where a single NFS server is genuinely insufficient and the
  data volume justifies a distributed filesystem.
- **Metadata-heavy workloads** — many files, deep trees, frequent directory operations — where
  NFS latency is the bottleneck. This is CubeFS's strongest technical claim.
- **When file and S3 access to the same data are both required**, from one system.
- **As a lighter alternative to Ceph** when block storage is not needed and the operational
  weight of Ceph is the blocker.
- Where **erasure coding for cold data** and replication for hot data are both wanted, selected
  per volume.

## When not to use it

- **When NFS would do.** Most RWX requirements are a shared directory for a handful of pods.
  Deploying a distributed filesystem for that is the mistake this folder warns about repeatedly —
  see [file-storage §1.2](../README.md#12-ask-whether-you-need-it-first).
- **On a managed cloud cluster.** EFS and Azure Files provide RWX with no cluster to run. See
  [cloud/](../../cloud/README.md).
- **When block storage is also needed.** CubeFS has no RBD equivalent; you would still need
  [Longhorn](../../block-storage/longhorn/README.md) or Ceph alongside it.
- **On small clusters.** Master quorum, MetaNodes and DataNodes are several stateful components
  before a single byte is stored. Below a few terabytes the overhead dominates.
- **Without someone to operate it.** Distributed storage rewards expertise, and here the expertise
  is scarcer than for Ceph.
- **For a database.** It is a network filesystem; the rule in
  [file-storage §4](../README.md#4-what-breaks-on-a-network-filesystem) applies unchanged.
- **On a single node**, expecting anything. Replication across one machine is copies on one disk
  — the same caveat as [Rook](../../multi-storage/rook/README.md).

## Notes

The recorded notes for this tool are the two upstream repositories, and the split between them is
itself informative:

- **[`cubefs`](https://github.com/cubefs/cubefs)** — the storage system: Master, MetaNode,
  DataNode, ObjectNode, the client and the CSI driver.
- **[`cubefs-helm`](https://github.com/cubefs/cubefs-helm)** — a **separate repository** holding
  the Helm charts. That separation is why this folder installs from a `GitRepository` rather than
  a `HelmRepository`: there is no packaged chart registry to pull from, so Flux clones the chart
  repository directly.

**How it is deployed here.** A Flux `GitRepository` pointing at
`https://github.com/cubefs/cubefs-helm.git`, pinned to tag `v3.3.2.150.0`, with an `ignore`
block that excludes everything except the `/cubefs` chart directory — the repository's standard
pattern for charts that live inside a project's source tree, used the same way for
[Garage](../../object-storage/garage/README.md),
[RustFS](../../object-storage/rustfs/README.md) and
[local-path-provisioner](../../local/local-path-provisioner/README.md). A `HelmRelease` in the
`cubefs` namespace consumes it, with an empty values block and the upstream values file
referenced in a comment.

**The empty values block is the whole deployment decision, deferred.** For CubeFS more than most
charts, the values are where the cluster is actually described: which nodes run Masters, which
run MetaNodes, which run DataNodes, which disks each uses, and the replica counts. CubeFS's chart
selects components onto nodes by **node labels**, so a real deployment starts by labelling
nodes, not by editing YAML. An install with default values on an unlabelled cluster does not
produce a working filesystem.

**Version pinning.** `v3.3.2.150.0` is the chart repository tag, and CubeFS's version numbering
does not match the main project's release tags one-to-one. Check which CubeFS version a chart tag
deploys rather than inferring it from the number — that mismatch is a small but reliable source
of confusion.

**Prerequisites.** The FUSE client needs `fuse` on the nodes, and the CSI driver runs a node
DaemonSet with the usual privileged mount requirements. MetaNodes need RAM proportional to the
number of files, which is a capacity-planning input that does not exist for NFS and surprises
people who size only for data.

**In this repository it is an evaluation entry.** Nothing in the Kind sandbox can exercise a
distributed filesystem meaningfully — one node, no spare disks, no node labels. What this folder
records is that CubeFS was considered as the large-scale RWX option for the on-premise case in
[`on-premisse/`](../../on-premisse/README.md), and the assessment above: technically strong,
CNCF-graduated, and carrying a real community-size risk that belongs in the decision.

---

[← File storage](../README.md)
