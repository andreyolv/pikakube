[← Local storage](../README.md)

# local-path-provisioner

<https://github.com/rancher/local-path-provisioner>

Chart values: <https://github.com/rancher/local-path-provisioner/blob/master/deploy/chart/local-path-provisioner/values.yaml>

RWX example: <https://github.com/rancher/local-path-provisioner/blob/master/examples/shared-fs/pvc.yaml>

---

## The problem it solves

A cluster with no storage system still needs PVCs to bind. Otherwise every chart with
`persistence.enabled: true` — which is most of them — hangs at `Pending`, and nothing in the
platform can be exercised at all.

local-path-provisioner is the smallest possible answer. A PVC arrives, it runs a helper pod on
the node the workload was scheduled to, creates a directory (`/opt/local-path-provisioner/<pv>`
by default), and writes a PV pointing at it with `nodeAffinity` set to that node.

That is the entire mechanism. No CSI driver, no network, no replication, no storage system —
a directory and a PV object.

**It is the default StorageClass in Kind and in k3s.** Anyone who has run `kubectl apply` against
either and watched a PVC bind has used it, usually without noticing. That ubiquity is the reason
this file matters more than the tool's simplicity suggests: it is the storage layer underneath
almost every local Kubernetes experiment in existence, including everything in this repository.

### What it gets right

Two things, and they are not trivial:

- **`volumeBindingMode: WaitForFirstConsumer`.** The directory cannot be created until the node
  is known, so binding waits for the pod to be scheduled. This is the correct setting and the one
  described in [block-storage §3.1](../../block-storage/README.md#31-volumebindingmode) — an
  `Immediate` local provisioner would be broken by construction.
- **A real `nodeAffinity` on the PV.** Unlike a raw `hostPath` volume, the PV is pinned to the
  node holding the data. A rescheduled pod is held unschedulable rather than silently starting
  against an empty directory somewhere else. That failure — silent, data-loss-shaped, no error
  anywhere — is the one `hostPath` produces and this avoids.

### What it does not do

| Feature | Status |
|---|---|
| Replication | **none** |
| Snapshots | none — there is no CSI snapshot interface to call |
| Volume expansion | not meaningfully |
| **Enforced capacity** | **no** — the PVC's size is a number nobody checks |
| High availability | no; the volume lives on one node |
| Backup | none of its own |

Two of those cause real incidents.

**Capacity is not enforced.** A PVC requesting `1Gi` can fill the node's entire filesystem. What
fails is not the pod — it is the kubelet, which reports disk pressure and evicts everything on
the node. A single runaway workload takes out unrelated ones, and the PVC objects give no hint
that this was possible.

**There are no snapshots.** Snapshot-based backup tools have nothing to call, so a
`VolumeSnapshot` produces an object that is never reconciled. The backup path is file-level:
[Velero](../../../backup/velero/README.md) with Kopia, or
[VolSync](../../../backup/volsync/README.md). See
[external-snapshotter](../../../backup/external-snapshotter/README.md) for why the silence is
total.

### Fine in development, dangerous in production

The danger is specifically that **it works**. A production cluster with this as the default class
behaves normally for months. PVCs bind, pods start, the database runs, nothing warns anybody.

Then a node is drained for a kernel upgrade:

1. The pod is rescheduled elsewhere.
2. Its PV has `nodeAffinity` on the node being drained.
3. The pod is unschedulable — correctly, and permanently.
4. If the node is gone rather than drained, the data is gone with it.

There is no degraded mode, no rebuild and no restore except from a backup that somebody set up
independently — and if nobody chose this StorageClass deliberately, nobody did.

The full version of that argument, including the one legitimate production case, is in
[the parent README](../README.md).

## When to use it

- **Kind, k3s, minikube, CI.** This is what it is for, and for that it is exactly right.
- **Local development of anything in this repository.** Every PVC here binds against it.
- **Ephemeral clusters** that are recreated rather than repaired.
- **Scratch space** where losing the data is a non-event: build caches, test fixtures, temporary
  extracts.

## When not to use it

- **As a production default StorageClass.** The failure is total and the warning arrives
  afterwards.
- **Under anything stateful you would miss.** No replication, no snapshots, no backup, no restore
  path.
- **For production node-local storage.** If node-local is genuinely the right choice — under a
  self-replicating database — use [OpenEBS Local PV](../../block-storage/openebs/README.md)
  (LVM or ZFS) or the
  [static local provisioner](../../on-premisse/README.md#31-sig-storage-local-static-provisioner)
  instead. Same model, plus enforced quotas, snapshots and thin provisioning.
- **To test an operator's failover behaviour.** Node-local volumes make the failure untestable,
  so a passing test proves nothing.
- **Where the PVC size is expected to be a quota.** It is not.
- **Expecting the RWX example to be cross-node RWX.** See the Notes; it is not.

## Notes

The recorded notes for this tool, preserved and explained.

**<https://github.com/rancher/local-path-provisioner>** — the upstream project, from Rancher. It
came out of the k3s work, which is why it is optimised for "make a small cluster work with no
infrastructure" rather than for durability.

**`local-path-provisioner` with `accessMode: ReadWriteMany` —
<https://github.com/rancher/local-path-provisioner/blob/master/examples/shared-fs/pvc.yaml>.**
This note is recorded here and also in
[csi-driver-nfs](../../file-storage/csi-driver-nfs/README.md), and it needs a clear caveat
because the example is very easy to misread.

The provisioner **can** serve a PVC declared `ReadWriteMany`. What that means in practice:

| | Reality |
|---|---|
| Several pods **on the same node** share the directory | **yes** — this works, and it is what the example demonstrates |
| Pods **on different nodes** share the directory | **no** — there is no server, no protocol, nothing shared |
| On a single-node cluster (Kind, k3s laptop) | indistinguishable from real RWX |
| On a multi-node cluster | silently not RWX at all; each node gets its own directory |

Kubernetes does not verify that a driver can deliver an access mode — access modes are
declarations that the API enforces on binding, not capabilities it discovers. So the PVC binds,
the pods start, and the illusion holds right up until the cluster has a second node.

This makes it genuinely useful for developing an RWX-dependent application locally, and never a
substitute for [file storage](../../file-storage/README.md). Real RWX across nodes needs
[csi-driver-nfs](../../file-storage/csi-driver-nfs/README.md),
[nfs-ganesha-server](../../file-storage/nfs-ganesha-server/README.md),
[JuiceFS](../../file-storage/juicefs/README.md), CephFS or a cloud file service.

**How it is deployed here.** A Flux `GitRepository` pointing at
`https://github.com/rancher/local-path-provisioner.git`, pinned to tag `v0.0.30`, with an
`ignore` block that excludes everything except `/deploy/chart/local-path-provisioner`, and a
`HelmRelease` in the `local-path-provisioner` namespace referencing that chart path
(`./deploy/chart/local-path-provisioner`). This is the repository's standard pattern for charts
that live inside a project's source tree rather than in a Helm registry — the same shape used for
[CubeFS](../../file-storage/cubefs/README.md),
[Garage](../../object-storage/garage/README.md) and
[RustFS](../../object-storage/rustfs/README.md).

**Installing it explicitly on Kind is slightly redundant and still worth doing**, because it makes
the dependency visible in Git rather than inherited invisibly from the cluster provisioner. Note
that Kind's built-in `standard` StorageClass is its own copy, so a cluster can end up with two
provisioners; check which class is marked default before assuming which one a PVC used.

**Configuration worth knowing:**

| Setting | Note |
|---|---|
| `nodePathMap` | which directory on which nodes; `DEFAULT_PATH_FOR_NON_LISTED_NODES` covers the rest |
| `storageClass.defaultClass` | whether this becomes the cluster default — set it deliberately |
| `storageClass.reclaimPolicy` | `Delete` by default; here that removes the directory |
| `sharedFileSystemPath` | the setting behind the RWX example above |
| helper pod image | a small busybox that does the `mkdir`/`rm`; it needs to be pullable, and in air-gapped clusters frequently is not |

The helper-pod detail is a real source of confusion: when provisioning fails in a restricted
environment, the error surfaces on the PVC while the actual problem is a helper pod that cannot
pull its image.

---

[← Local storage](../README.md)
