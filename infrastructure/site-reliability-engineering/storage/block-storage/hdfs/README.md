[← Block storage](../README.md)

# HDFS

<https://github.com/apache/hadoop>
<https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html>

Deployment shapes: [`namenode/`](namenode/README.md) — the metadata server ·
[`datanode/`](datanode/README.md) — the block servers

---

> **This is the odd one out in this folder.** HDFS is not a Kubernetes block provisioner. It
> does not implement CSI, does not provision PersistentVolumes and does not give any pod a PVC.
> It is a distributed filesystem from the Hadoop era that *consumes* PVCs. It is filed here
> because it is block-shaped storage for a data platform, not because it belongs to the same
> category as [Longhorn](../longhorn/README.md) and [OpenEBS](../openebs/README.md).

## The problem it solves

HDFS — the **Hadoop Distributed File System** — was built for one workload: storing files far
larger than any single machine's disk, on a cluster of commodity servers, and reading them
sequentially at high throughput from compute that runs next to the data.

Its design decisions all follow from that:

| Design choice | Reason |
|---|---|
| Very large block size (128 MB default) | minimises metadata; suits sequential scans, terrible for small files |
| Write-once, append-only | no random writes; simplifies consistency enormously |
| Replication, 3 copies by default | commodity disks fail; the filesystem tolerates it |
| **Data locality** | schedule the computation on the node holding the block |
| A single metadata server | one authority for the namespace, held entirely in memory |

Data locality was the whole point in 2010. Network bandwidth was the bottleneck, so moving a
MapReduce task to the data beat moving the data to the task. Hadoop, Hive, HBase and early Spark
were all built on that assumption.

**That assumption no longer holds.** Networks got fast, storage and compute separated, and object
storage arrived with an API that every engine now speaks. The architecture HDFS optimised for is
not the architecture anyone builds today.

### The NameNode is the architecture

Everything about running HDFS reduces to one component.

The **NameNode** holds the entire filesystem namespace — every directory, file and block
location — **in memory**. DataNodes hold the actual blocks and report in. A client asks the
NameNode where a file's blocks are, then reads them directly from DataNodes.

The consequences:

- **The NameNode is a single point of failure.** Without HA (which requires a JournalNode
  quorum, ZooKeeper and a standby NameNode) losing it makes the entire filesystem unreadable.
  Every block is still sitting on the DataNodes' disks, intact and unreachable, because nothing
  else knows what they are.
- **Metadata capacity is bounded by RAM.** Roughly 150 bytes per object. Millions of small files
  exhaust the NameNode long before the DataNodes run out of disk — the "small files problem"
  that dominates HDFS operations.
- **It is a slow, expensive restart.** Loading `fsimage`, replaying the edit log and waiting for
  DataNodes to report their blocks takes minutes on a real cluster.

This is the same architectural pattern as [JuiceFS's metadata engine](../../file-storage/juicefs/README.md)
and [MooseFS's master](../../on-premisse/README.md#21-moosefs-and-glusterfs): one component that
knows where everything is, and whose loss makes the data unreadable even though every byte
survives. Recognising the pattern is more useful than any individual tool here.

### Why object storage replaced it

For any new data platform, the answer is [object storage](../../object-storage/README.md):

| | HDFS | S3-compatible object storage |
|---|---|---|
| Metadata | a NameNode you keep alive | the service's problem |
| Scaling | add DataNodes; NameNode RAM is the ceiling | effectively unbounded |
| Small files | a real operational limit | irrelevant |
| Compute coupling | designed for co-located compute | separated, which is what people want now |
| Ecosystem | Hadoop-era tools | Spark, Trino, DuckDB, Iceberg, Delta, Hudi — everything |
| On Kubernetes | an application to operate | a bucket, or [MinIO](../../object-storage/minio/README.md) |

Table formats — Iceberg, Delta Lake, Hudi — reintroduced the transactional and schema features
that people used HDFS-plus-Hive for, on top of object storage, without a metadata server to keep
alive. That combination is what closed the question.

## When to use it

The honest list is short:

- **An existing Hadoop estate.** Jobs, tooling and institutional knowledge already built on
  `hdfs://` paths, where migration is a project rather than a decision.
- **Compatibility testing** — verifying that a Spark job which reads `hdfs://` still works, or
  reproducing a production issue locally, which is what the manifests in this folder are for.
- **Learning the architecture.** Understanding NameNode/DataNode separation makes the metadata-
  server pattern legible everywhere else it appears.
- A genuinely on-premise, very large sequential-scan workload where object storage is not
  available and the team already runs Hadoop. This is rare and shrinking.

## When not to use it

- **Any new data platform.** Object storage plus a table format is the answer, and it has been
  for years. See [object-storage](../../object-storage/README.md) and
  [lakehouse table formats](../../../../data-governance/lakehouse/table-formats/README.md).
- **Expecting it to provide PVCs.** It provisions nothing. It needs PVCs from a real block
  provisioner underneath — which is exactly what this folder's other tools are for.
- **Many small files.** The NameNode's memory is the limit, and it is reached far earlier than
  intuition suggests.
- **On Kubernetes, without a very good reason.** Running HDFS in pods means operating a stateful
  distributed system with a memory-bound single metadata node, on top of a storage layer you also
  operate. The layering is the argument against it.
- **Without NameNode HA, for anything that matters.** A single NameNode means the filesystem has
  a scheduled outage every time that pod restarts, and an unbounded one if its volume is lost.
- As a general-purpose filesystem. It is write-once and append-only; random writes are not
  supported, and nothing that expects POSIX will work.

## Notes

The recorded note for this folder is the upstream repository,
<https://github.com/apache/hadoop>. Everything below is the context around it and around what is
actually deployed.

**What the manifests here are.** A minimal two-part HDFS, built from the `bde2020/hadoop-*`
community images:

| Shape | Kubernetes object | Storage |
|---|---|---|
| [NameNode](namenode/README.md) | a `Deployment`, replicas 1, ports 8020 (RPC) and 50070 (web UI) | a PVC bound to a `hostPath` PV at `/dags/spark/hdfs` |
| [DataNode](datanode/README.md) | a `StatefulSet`, replicas 1, with a `volumeClaimTemplate` | 1Gi RWO per replica, plus a `hostPath` PV at `/dags/spark/datanode` |

Both PVs are `hostPath`, `ReadWriteOnce`, 1Gi, on the `standard` StorageClass. The DataNode is
configured with `CORE_CONF_fs_defaultFS: hdfs://namenode:8020`, so the two find each other by
Service name.

**Read this as a Spark fixture, not a storage design.** The `hostPath` paths — `/dags/spark/...`
— give away the intent: this exists so
[Spark](../../../../data-engineering/processing/spark/README.md) jobs have an `hdfs://` target to
read and write during experiments. One NameNode with no HA, one DataNode, replication that
cannot happen, and `hostPath` volumes that vanish with the Kind node. That is fine for its
purpose and is not a template for anything.

**The `hostPath` PV choice is worth flagging** rather than copying. As covered in
[local/](../../local/README.md), a `hostPath`-backed PV has no meaningful durability and, unlike
a proper `local` PV, the pattern is easy to get wrong in ways that silently hand a pod an empty
directory. Here it is deliberate and disposable.

**The filename `stefulset.yaml`** in the DataNode folder is a typo for `statefulset.yaml`. It has
no functional effect — Kubernetes reads the object's `kind`, not the filename — but it is worth
knowing when grepping for it.

**Real HDFS on Kubernetes needs much more** than these two objects: a JournalNode quorum and
ZooKeeper for NameNode HA, a `StatefulSet` with a headless Service and stable identities for the
NameNodes, rack-awareness configuration to make replication meaningful, and a DataNode per
storage node. If that list reads as a lot of machinery to obtain a filesystem, that is the
correct reaction, and it is the argument in favour of object storage restated as an operations
problem.

---

[← Block storage](../README.md)
