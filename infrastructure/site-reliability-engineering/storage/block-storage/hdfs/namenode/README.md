[← HDFS](../README.md)

# HDFS NameNode

<https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#NameNode_and_DataNodes>
<https://github.com/big-data-europe/docker-hadoop>

The simpler of the two [HDFS](../README.md) deployment shapes, and the one everything else
depends on. Its counterpart is [`../datanode/`](../datanode/README.md).

---

## The problem it solves

The NameNode is HDFS's **metadata server**. It holds the entire filesystem namespace — every
directory, every file, and the list of blocks each file is made of, together with which
DataNodes currently hold each block.

It holds all of it **in memory**, and persists it as two things on disk:

| File | Contents |
|---|---|
| `fsimage` | a checkpoint of the namespace at a point in time |
| `edits` (the edit log) | every namespace change since that checkpoint |

A client that wants to read a file asks the NameNode where the blocks are, then reads them
directly from the DataNodes. The NameNode never touches file data — only metadata. That
separation is what lets HDFS scale reads: the metadata path is one small server, the data path is
every DataNode in parallel.

### Why it defines the whole system

Three properties follow, and they are the reason this shape gets its own README:

1. **It is a single point of failure.** Without HA — a JournalNode quorum, ZooKeeper and a
   standby NameNode — losing it makes the filesystem unreadable. Every block is still on the
   DataNodes' disks, intact, and nothing in the cluster knows what any of them are.
2. **Its capacity is RAM, not disk.** Roughly 150 bytes of heap per file, directory and block.
   Millions of small files exhaust the NameNode while the DataNodes are still nearly empty. This
   is the "small files problem", and it is the most common way an HDFS cluster hits a wall.
3. **Its volume is the most valuable in the cluster.** Losing the `fsimage` and edit log loses
   the filesystem. Losing a DataNode's disk loses replicas that can be rebuilt.

That third point is the practical instruction: **the NameNode's PVC is what to back up.**

## What this shape adds over the simpler one

There is no simpler one — the NameNode is the floor. Compared to
[`../datanode/`](../datanode/README.md), the differences are deliberate and instructive:

| | NameNode | DataNode |
|---|---|---|
| Kubernetes object | `Deployment` | `StatefulSet` |
| Replicas | 1, and more requires a full HA setup | scales by adding replicas |
| Volume | a single named PVC | a `volumeClaimTemplate`, one PVC per replica |
| Identity | none needed; found by Service name | stable per-replica identity |
| Holds | metadata only | the actual blocks |
| Loss means | the filesystem is unreadable | replicas rebuild, if there are others |

A `Deployment` is the right shape here precisely because there is only ever one, and it is
addressed by a Service rather than by an ordinal hostname. A real HA NameNode pair *is* usually a
`StatefulSet`, because the two members need stable identities to coordinate through the
JournalNodes — another sign that HA is a different deployment, not a replica count change.

## When to use it

- Whenever HDFS is deployed at all. Nothing works without it.
- **As the thing to protect** in any HDFS backup or DR plan: back up the metadata volume, and
  verify a restore, before worrying about DataNode capacity.

## When not to use it

- **With `replicas: 1` for anything that matters.** A single NameNode means the filesystem has an
  outage every time the pod restarts — including for a routine node drain — and an unbounded one
  if its volume is lost.
- **With `replicas: 2` on this manifest, hoping for HA.** Two independent NameNodes with no
  JournalNode quorum is not high availability; it is two servers with divergent views of the same
  namespace, which is worse than one. HA needs JournalNodes, ZooKeeper and the ZKFC controller.
- On storage with no durability guarantee — which, in this repository, is exactly what it is
  running on.

## Notes

**What is deployed here.** A `Deployment` named `namenode` in the `hdfs` namespace, one replica,
running `bde2020/hadoop-namenode` with `CLUSTER_NAME=hdfs-k8s`. It exposes two ports:

| Port | Name | Purpose |
|---|---|---|
| 8020 | `nn-rpc` | the RPC endpoint clients and DataNodes use — this is what `hdfs://namenode:8020` resolves to |
| 50070 | `nn-web` | the web UI, showing cluster health, live DataNodes and block reports |

Port 50070 is the Hadoop 2 default. Hadoop 3 moved the NameNode HTTP UI to 9870, so a manifest
using 50070 is describing a Hadoop 2-era image. Worth knowing when a port-forward to 9870 returns
nothing.

`/hadoop/dfs/name` is mounted from a PVC named `hdfs-namenode` — the metadata directory, holding
`fsimage` and the edit log. That is the volume described above as the most valuable one.

**The PV behind it is a `hostPath`** at `/dags/spark/hdfs`, 1Gi, `ReadWriteOnce`, on the
`standard` StorageClass. Two observations:

- `hostPath` means the metadata lives on one node's filesystem with no replication and no
  meaningful durability. For a Kind-based Spark fixture that is a deliberate, disposable choice;
  it is not a pattern to reuse. See [local/](../../../local/README.md).
- A statically defined `PersistentVolume` carries a `namespace` field in this manifest, which
  Kubernetes ignores — PVs are cluster-scoped. Harmless, and a common copy-paste artefact.

**The static PV plus PVC pairing** is how you bind a claim to a specific volume rather than
letting a provisioner choose. It works, and it means the PVC is tied to whatever the PV points
at — including its node, since a `hostPath` path only exists where it exists.

**What a production NameNode would add**, for contrast with what is here: two NameNodes in a
`StatefulSet`, an odd-numbered JournalNode quorum sharing the edit log, ZooKeeper plus ZKFC for
automatic failover, a heap sized against the expected object count rather than left at default,
and the metadata volume on replicated storage with a tested backup. That list is most of the
reason [the parent README](../README.md) recommends object storage for new work.

---

[← HDFS](../README.md)
