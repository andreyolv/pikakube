[← Cloud storage](../README.md)

# Azure

<https://github.com/kubernetes-sigs/azuredisk-csi-driver>
<https://github.com/kubernetes-sigs/azurefile-csi-driver>
<https://github.com/kubernetes-sigs/blob-csi-driver>
<https://github.com/Azure/azure-storage-fuse>

---

## The problem it solves

On AKS, storage is three CSI drivers and a client SDK. The mapping is the same one every
provider offers, under Azure's names:

| Need | Azure service | Driver | Access mode |
|---|---|---|---|
| A disk for a database | **Azure Disk** (Managed Disks) | `azuredisk-csi-driver` | `ReadWriteOnce` |
| A shared directory across pods | **Azure Files** | `azurefile-csi-driver` | `ReadWriteMany` |
| A lake, backups, chunks | **Blob Storage** | none — call the API | not a PVC |
| Blob presented as a directory | Blob Storage via BlobFuse or NFSv3 | `blob-csi-driver` | RWX-ish, with caveats |

Azure is the one provider that ships a **CSI driver for object storage** as a first-class option,
which makes the fourth row worth its own discussion — see below, because it is the row most
likely to be misused.

All four drivers are AKS managed add-ons. Enable them on the cluster rather than installing charts
by hand; the driver version then tracks the cluster version and the identity wiring is handled.

### Azure Disk: the default

Managed Disks behave like local disks, are `ReadWriteOnce`, and are **zonal** where the cluster
uses availability zones. Everything in [block-storage/](../../block-storage/README.md) applies
unchanged, detach delays included.

The Azure-specific decisions:

| Parameter | Notes |
|---|---|
| `skuName` | `Premium_LRS` for databases; `StandardSSD_LRS` for most other things; `Standard_LRS` (HDD) rarely |
| `Premium_ZRS` / `StandardSSD_ZRS` | **zone-redundant disks** — the interesting one, see below |
| `UltraSSD_LRS` | IOPS and throughput provisioned independently; needs the feature enabled on the node pool |
| `cachingMode` | `ReadOnly` is the default; **`None` for write-heavy databases** |
| `diskEncryptionSetID` | customer-managed keys |
| `fsType` | `ext4` or `xfs` |

Two of these deserve attention.

**ZRS disks are unusual and useful.** A zone-redundant Managed Disk is replicated synchronously
across three availability zones, which means the volume is not pinned to one zone and a pod can
attach it from a node in another. That removes the constraint described in
[cloud §3.3](../README.md#33-zones-are-the-recurring-failure) — a stateful workload on ZRS can
actually move zones. It costs more and has lower peak performance than LRS. Most other providers
have no equivalent, so it is easy to overlook.

**Caching is a correctness-adjacent setting.** `ReadOnly` host caching is the default and is
right for read-heavy workloads. For a database with a write-ahead log it adds a layer you do not
want; `None` is the conventional choice, and Azure's own database guidance says so.

Also: **disk attachment limits are per VM size**, and the same failure mode applies as everywhere
— a node with many stateful pods hits the ceiling and pods sit pending with attach errors that
look like driver faults.

### Azure Files: RWX, and two very different protocols

Azure Files is a managed shared filesystem, and it is the answer to
[file-storage/](../../file-storage/README.md) on AKS: RWX without operating a file server.

It speaks **two protocols**, and choosing between them is the real decision:

| | SMB | NFS v4.1 |
|---|---|---|
| Tier | Standard or Premium | **Premium only** (FileStorage account) |
| POSIX permissions | emulated, with `mountOptions` for uid/gid/file_mode | real |
| Linux workload fit | workable, and the source of most permission complaints | much better |
| Public endpoint | available | requires a private endpoint / VNet restriction |
| Cost | lower | higher, provisioned capacity |

For Linux pods, **NFS is the one you want** where the budget allows. The SMB mode requires
`mountOptions` such as `uid`, `gid`, `dir_mode` and `file_mode` to be set on the StorageClass, and
almost every "permission denied on Azure Files" report traces back to them being absent or
mismatched with the pod's `securityContext`.

Standard tier is billed per GB used; Premium is billed on **provisioned** capacity with a
100 GiB minimum, so a small Premium share costs the same as a 100 GiB one. Size accordingly.

And the rule from [file-storage](../../file-storage/README.md) holds: managed does not change
POSIX semantics over a network. **No databases on Azure Files.**

### Blob Storage, and the driver that mounts it

Blob Storage is the object store — the Azure equivalent of S3, and where the lakehouse, the
[Velero](../../../backup/velero/README.md) backups and the observability chunks belong. This is
what [MinIO](../../object-storage/minio/README.md) substitutes for on-premise, and on AKS there
is no reason to run MinIO.

The `blob-csi-driver` mounts a container as a volume, two ways:

| Mode | Mechanism | Reality |
|---|---|---|
| **BlobFuse** | [azure-storage-fuse](https://github.com/Azure/azure-storage-fuse), a FUSE driver | not a filesystem; caching semantics, no real locking |
| **NFS v3** | the storage account's native NFSv3 endpoint | closer to a filesystem, still object storage underneath |

The existence of a supported CSI driver makes this look like a normal storage choice. It is not.
BlobFuse presents a bucket as a directory, and the warnings in
[object-storage](../../object-storage/README.md) apply in full: no file locking, no atomic
rename, no partial writes, no `fsync` guarantee, and performance unlike a disk. BlobFuse2 is the
current generation and is better at caching, not at semantics.

It is the right tool for one job: giving an application that only knows how to read files access
to data that lives in blob storage — batch jobs reading Parquet, model weights, read-mostly
reference data. It is the wrong tool for anything that writes transactionally.

## When to use it

- **Any AKS cluster**: enable the Azure Disk CSI driver. Without a storage driver, PVCs do not
  bind.
- **Azure Files (NFS) when RWX is genuinely required** and latency is not critical.
- **`Premium_ZRS` disks** for stateful workloads that must survive a zone failure without
  application-level cross-zone replication — the most distinctive option Azure offers here.
- **Blob Storage for everything that is not a PVC**, called through the SDK.
- **blob-csi-driver in read-mostly mode** for applications that cannot be changed to speak the
  Blob API.

## When not to use it

- **Self-hosting Longhorn, Ceph or MinIO on AKS.** Replicating storage that is already replicated
  under an SLA, at full operational cost. Only a named requirement justifies it — see
  [the parent README](../README.md).
- **Azure Files for a database.** Neither protocol changes what a network filesystem is.
- **SMB mode for Linux workloads if NFS is affordable.** The uid/gid `mountOptions` dance is a
  recurring, avoidable source of failure.
- **BlobFuse as a write target** for anything transactional. It is a read convenience.
- **Default host caching for write-heavy databases** — set `cachingMode: None`.
- **LRS disks assuming zone resilience.** They are zonal; ZRS is the option that is not.

## Notes

The recorded notes for this folder, translated and placed — four repository links, which map
exactly onto the three storage shapes plus the FUSE layer:

- **[`azuredisk-csi-driver`](https://github.com/kubernetes-sigs/azuredisk-csi-driver)** — block,
  `ReadWriteOnce`. The `skuName`, `cachingMode` and ZRS decisions above are what this driver's
  StorageClass parameters expose.
- **[`azurefile-csi-driver`](https://github.com/kubernetes-sigs/azurefile-csi-driver)** — file,
  `ReadWriteMany`, over SMB or NFS. The protocol choice is the substance.
- **[`blob-csi-driver`](https://github.com/kubernetes-sigs/blob-csi-driver)** — object storage
  presented as a mount, via BlobFuse or NFSv3. Recorded here because it exists and is supported,
  and flagged because that support makes it look safer than it is.
- **[`azure-storage-fuse`](https://github.com/Azure/azure-storage-fuse)** — BlobFuse itself, the
  FUSE implementation the CSI driver wraps. Useful to know by name: when a blob-backed volume
  behaves strangely, this is the component to read about, and it is where the caching and
  consistency semantics are documented.

**No manifests exist in this folder**, and that is correct — the drivers are AKS add-ons, not
something a Kind cluster deploys. This page is a reference note.

**Identity.** The drivers need permissions on the storage account and the disk resources. Use
**Workload Identity** (or a user-assigned managed identity on the node pool) rather than a
storage account key in a Secret. Account keys grant full control of the account, do not expire,
and are the credential that outlives everyone who remembers creating it. The same applies to
applications reading Blob Storage.

**Snapshots.** The Azure Disk driver implements CSI snapshots; the `VolumeSnapshot` CRDs and the
snapshot controller are a **separate concern** and must be present and reconciling, or snapshot
objects are created and nothing happens. See
[external-snapshotter](../../../backup/external-snapshotter/README.md). Azure Files snapshots
exist at the share level and are not the same mechanism.

**Related work in this repository.** [Velero's Azure notes](../../../backup/velero/azure/README.md)
cover backing up Azure-hosted volumes and file shares, which is the other half of this page —
this one is about provisioning, that one about getting the data back.

---

[← Cloud storage](../README.md)
