[← HDFS](../README.md)

# HDFS DataNode

<https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#Data_Replication>
<https://github.com/big-data-europe/docker-hadoop>

The scaling half of [HDFS](../README.md). Its counterpart is
[`../namenode/`](../namenode/README.md), which must exist first.

---

## The problem it solves

DataNodes hold the actual file blocks. Where the
[NameNode](../namenode/README.md) knows *what* exists, DataNodes hold *the bytes* — and they are
the component you add more of when the cluster needs capacity or throughput.

What a DataNode does:

| Job | Detail |
|---|---|
| Store blocks | 128 MB by default, as ordinary files on its local disk |
| Serve reads | clients contact it **directly** after asking the NameNode for locations |
| Accept writes | in a **pipeline** — the client writes to one DataNode, which forwards to the next replica |
| Heartbeat | every 3 seconds, so the NameNode knows it is alive |
| Block report | periodically lists every block it holds, which is how the NameNode rebuilds its location map |

The block report is the part worth understanding: **the NameNode does not persist block
locations.** It persists the namespace, and it learns where the blocks are by being told, on
every DataNode startup. That is why a NameNode restart on a real cluster takes minutes — it is
waiting for every DataNode to report in before it will leave safe mode.

### Replication is a DataNode property

HDFS's durability comes from writing each block to N DataNodes, three by default, chosen by the
NameNode using rack-awareness: two replicas in one rack, one in another, so a rack losing power
does not take all copies.

Two consequences that matter here:

- **Replication needs DataNodes to replicate to.** With one DataNode, `dfs.replication: 3` is
  simply unsatisfiable — the NameNode reports under-replicated blocks forever and the guarantee
  does not exist.
- **Rack-awareness needs configuration.** Without a topology script, HDFS thinks every node is in
  the same rack, and the placement policy that the durability argument rests on degenerates.

## What this shape adds over the simpler one

This is the second of the two [HDFS](../README.md) deployment shapes, and the comparison is the
clearest illustration of why Kubernetes has two stateful controllers:

| | [NameNode](../namenode/README.md) | DataNode |
|---|---|---|
| Object | `Deployment` | **`StatefulSet`** |
| Replicas | exactly 1 (HA is a different deployment) | **scales — this is the point** |
| Volumes | one named PVC, shared by whatever pod runs | **`volumeClaimTemplate`** — one PVC per replica, created automatically |
| Identity | none; reached by Service name | stable ordinal hostname, via a headless Service |
| On rescheduling | any pod can take the volume | replica *N* reattaches to *its own* volume |

The `volumeClaimTemplate` is what the shape adds. Scaling a `StatefulSet` from 1 to 3 creates
`hdfs-data-datanode-0`, `-1` and `-2` — three independent PVCs, each permanently bound to its
replica. That is exactly the model a distributed storage daemon needs, and it is why every
storage system in this repository that scales horizontally uses a `StatefulSet`.

It also carries the standard `ReadWriteOnce` consequence: each replica's volume is attached to
one node, so a node failure means waiting out the detach timers before that replica returns. See
[block-storage §1.2](../../README.md#12-the-failure-everyone-meets).

## When to use it

- Whenever HDFS is deployed. A NameNode with no DataNodes is a namespace with nowhere to put
  data.
- **Scale it, not the NameNode**, when capacity or read throughput is the constraint. Adding
  DataNodes is the supported growth path; the NameNode grows by heap, not by replicas.
- With **at least three replicas on distinct nodes** if replication is meant to mean anything.

## When not to use it

- **With one replica, expecting durability.** One DataNode is one copy on one disk. The default
  replication factor of 3 cannot be met, and the NameNode will say so.
- **Several replicas on a single Kubernetes node.** Three DataNode pods on one machine are three
  copies on one disk. Pod anti-affinity is what makes replica count mean something; without it,
  scaling produces the appearance of durability and none of the substance.
- **Without rack-awareness on real hardware.** The block placement policy is the durability
  argument, and it needs a topology configuration to work.
- On storage that already replicates. DataNodes on Longhorn volumes means HDFS's 3× replication
  on top of Longhorn's 3× — nine copies. Under a self-replicating system, node-local storage is
  correct: [OpenEBS Local PV](../../openebs/README.md) or a
  [static local provisioner](../../../on-premisse/README.md#31-sig-storage-local-static-provisioner).

## Notes

**What is deployed here.** A `StatefulSet` named `datanode` in the `hdfs` namespace, one replica,
`serviceName: datanode`, running `bde2020/hadoop-datanode`. It finds the NameNode through
`CORE_CONF_fs_defaultFS: hdfs://namenode:8020` — an environment variable that the `bde2020`
images translate into `core-site.xml` entries, which is the convention that image family uses for
all Hadoop configuration.

`/hadoop/dfs/data` is backed by a `volumeClaimTemplate` named `hdfs-data`: 1Gi,
`ReadWriteOnce`. There is also a static `hostPath` `PersistentVolume` at `/dags/spark/datanode`,
1Gi, `ReadWriteOnce`, on the `standard` StorageClass.

Note that the template does not name a `storageClassName`, so the PVC binds through the default
class — which in Kind is
[local-path-provisioner](../../../local/local-path-provisioner/README.md), not the static PV
sitting alongside it. Whether the `hostPath` PV is actually used depends on which claim binds
first; a `volumeClaimTemplate` without an explicit class will generally take the dynamic path.
This is worth knowing rather than assuming, and it is a good illustration of why an unnamed
StorageClass is a source of surprise.

**`resources: {}`** leaves the container with no requests or limits, so it lands in the
`BestEffort` QoS class and is the first thing evicted under node pressure. Acceptable in a
sandbox; not a pattern for a storage daemon, which is exactly the workload you least want
evicted.

**The filename is `stefulset.yaml`** — a typo for `statefulset.yaml`. Functionally irrelevant,
since Kubernetes reads the object's `kind`, but it defeats a `find`-by-name.

**Read this as a Spark fixture.** One DataNode, one replica, `hostPath` paths under
`/dags/spark/`, on a Kind node. It exists so
[Spark](../../../../../data-engineering/processing/spark/README.md) jobs have a working
`hdfs://` endpoint to read and write during experiments. It demonstrates the DataNode's role and
the `StatefulSet` shape, and it demonstrates none of HDFS's durability properties — the same
honest caveat that applies to [Longhorn](../../longhorn/README.md) and
[Rook](../../../multi-storage/rook/README.md) in this repository.

**What a real deployment would add:** three or more replicas with pod anti-affinity across nodes,
a rack topology configuration, one volume per physical disk rather than one per pod, node-local
storage instead of a replicated CSI driver underneath, and resource requests sized so the
DataNode is not the first casualty of memory pressure.

---

[← HDFS](../README.md)
