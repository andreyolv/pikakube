[← Block storage](../README.md)

# OpenEBS

<https://github.com/openebs/openebs>
<https://openebs.io/docs>
<https://artifacthub.io/packages/helm/openebs/openebs>

Chart values: <https://github.com/openebs/openebs/blob/main/charts/values.yaml>

Engines: <https://github.com/openebs/mayastor> · <https://github.com/openebs/lvm-localpv> ·
<https://github.com/openebs/zfs-localpv> · <https://github.com/openebs/dynamic-localpv-provisioner>

---

## The problem it solves

The same problem as [Longhorn](../longhorn/README.md) — PVCs on a cluster with no provider CSI
driver — but answered differently, and the difference is the only thing worth remembering about
OpenEBS.

**OpenEBS is not one storage system. It is an umbrella over several independent engines**, and
they have almost nothing in common beyond the name and the installer. Any sentence of the form
"OpenEBS is faster/slower/more reliable than X" is meaningless until the engine is named.

| Engine | What a volume actually is | Replicated | Snapshots | Use it when |
|---|---|---|---|---|
| **Local PV hostpath** | a directory on the node's disk | **no** | no | the simplest node-local volume; barely more than local-path-provisioner |
| **Local PV LVM** | an LVM logical volume on the node | **no** | yes (LVM) | node-local speed, with real quotas and thin provisioning |
| **Local PV ZFS** | a ZFS dataset on the node | **no** | yes (ZFS) | node-local, plus compression and `send`/`recv` |
| **Local PV device** | a whole raw block device | **no** | no | one disk, one PVC, no indirection |
| **Mayastor** | NVMe-oF replicated volume, SPDK-based | **yes**, synchronous | yes | low-latency replicated block on NVMe hardware |
| Jiva / cStor | the older replicated engines | yes | yes | legacy only; superseded by Mayastor |

The split that matters is the third column. **Four of these do not replicate anything.** They
produce a volume pinned to one node, and losing that node loses the volume — permanently, with
the PV's `nodeAffinity` pointing at a machine that is gone.

That is not a defect. It is the point.

### Why unreplicated storage is the right answer sometimes

A CloudNativePG cluster with three instances, a Kafka broker set with replication factor three,
a Cassandra ring, an Elasticsearch cluster: each of these already keeps N copies of the data on N
machines and heals itself when one is lost.

Putting replicated storage underneath such a system means:

- 3 application replicas × 3 storage replicas = **9 copies** of every byte.
- Every write crosses the network twice — once for the application's replication, once for the
  storage layer's.
- The recovery path becomes two systems rebuilding at the same time.

Local PV removes the second layer entirely. Writes go straight to the node's disk with no network
in the path, capacity is what the disk holds, and when a node dies the database does what it was
designed to do: promote a replica and rebuild the lost member elsewhere.

So the honest positioning is:

| Situation | Answer |
|---|---|
| Single-instance workload that must survive node loss | [Longhorn](../longhorn/README.md) |
| Self-replicating database, and you want speed | **OpenEBS Local PV (LVM or ZFS)** |
| Replicated block on NVMe with latency requirements | **OpenEBS Mayastor** |
| Managed cloud cluster | [cloud/](../../cloud/README.md) CSI drivers |

### Mayastor is a different commitment

Mayastor is the replicated engine, built on SPDK and NVMe-over-Fabrics, and it is genuinely fast.
It is also the most demanding thing in this folder to run:

- **NVMe devices**, not spinning disks, and ideally dedicated.
- **Hugepages** configured on every storage node (2 GiB is the usual starting point).
- Specific kernel modules (`nvme_tcp`) and a kernel version it approves of.
- A meaningful CPU reservation — the I/O engine polls rather than sleeps.

None of that is a drop-in. Treat Mayastor as a hardware decision, not a Helm install.

## When to use it

- **Under a self-replicating database on real hardware.** This is the strongest case: Local PV
  LVM or ZFS gives node-local write latency with enforced capacity, thin provisioning and
  snapshots, and the application handles durability. Nothing else in this folder does that as
  well.
- **When you want ZFS properties in Kubernetes** — compression, checksums, cheap snapshots,
  `zfs send` for replication — exposed as ordinary PVCs.
- **When you want LVM's quotas and thin provisioning** without adopting a distributed storage
  system.
- **Low-latency replicated block, with NVMe available and hugepages configurable** — Mayastor,
  chosen deliberately after reading its prerequisites.
- Replacing raw `hostPath` or `local` PVs on bare metal with something that has a real
  provisioner behind it — see also
  [sig-storage-local-static-provisioner](../../on-premisse/README.md#31-sig-storage-local-static-provisioner).

## When not to use it

- **When you cannot say which engine you mean.** "We use OpenEBS" is not a storage decision. If
  the engine is unspecified, the durability properties are unspecified.
- **Expecting Local PV to survive node loss.** It does not. There is no rebuild, no failover and
  no restore except from a backup taken elsewhere — the same argument as
  [local/](../../local/README.md), which applies in full here.
- **As a general-purpose replicated storage layer for single-instance workloads.** Longhorn does
  that job with a fraction of the decision surface and a UI that makes replica state legible
  during an incident.
- **Mayastor without meeting its prerequisites.** Without NVMe and hugepages it either refuses to
  start or performs badly, and the diagnosis is unpleasant.
- **On a managed cloud cluster** for replication — the provider already replicates. Local PV on
  cloud instance storage is a narrower but legitimate exception for self-replicating databases on
  NVMe instance types.
- **When operability matters most.** There is no equivalent of Longhorn's UI. Observability of
  volume health is per engine, and mostly through metrics and `kubectl`.

## Notes

The recorded note for this tool is the upstream repository,
<https://github.com/openebs/openebs>. Everything below is the context around it.

**How it is deployed here.** A Flux `HelmRelease` in the `openebs` namespace, pinned to chart
version `3.10.0`, with an empty values block and the upstream values file referenced in a
comment. An empty values block matters more for OpenEBS than for most charts, because **the
values are where the engine is selected** — which engines are enabled, and whether their
prerequisites are met, is not something the chart can infer.

**The 3.x versus 4.x reorganisation.** OpenEBS restructured substantially between major
versions: the umbrella chart was reworked, the legacy engines (Jiva, cStor) were split out, and
Local PV plus Mayastor ("Replicated PV Mayastor") became the two headline offerings. Chart
`3.10.0` is on the older side of that boundary. Documentation and blog posts from either era
describe different products under the same name, which is a persistent source of confusion when
searching — check which version a page is describing before following it.

**Prerequisites are per engine and easy to skip:**

| Engine | Needs on the node |
|---|---|
| Local PV LVM | LVM2 installed, a volume group created |
| Local PV ZFS | ZFS installed, a zpool created |
| Local PV device | a raw, unformatted block device |
| Mayastor | NVMe devices, hugepages, `nvme_tcp`, a supported kernel |

The volume group or zpool is created by you, not by OpenEBS. The provisioner carves from what
already exists.

**StorageClass settings still apply.** `volumeBindingMode: WaitForFirstConsumer` is effectively
mandatory for every Local PV engine — binding `Immediate` would place a volume on an arbitrary
node before the scheduler placed the pod, and the pod would be unschedulable. `reclaimPolicy` and
`allowVolumeExpansion` behave as described in
[block-storage §3](../README.md#3-storageclass-the-three-fields-that-decide-everything). LVM and
ZFS support expansion; hostpath's reported size is not enforced at all.

**Backups.** Local PV volumes have no off-cluster backup mechanism of their own — unlike
[Longhorn](../longhorn/README.md), which ships one. LVM and ZFS snapshots are local to the node
and disappear with it. The backup path is file-level:
[Velero](../../../backup/velero/README.md) with Kopia, or
[VolSync](../../../backup/volsync/README.md). This is the most commonly missed consequence of
choosing Local PV.

**In a Kind cluster** none of the engines are meaningful: there is no volume group, no zpool, no
spare device and one node. The install reconciles and that is all it proves.

---

[← Block storage](../README.md)
