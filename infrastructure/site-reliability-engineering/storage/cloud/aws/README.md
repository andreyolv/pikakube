[← Cloud storage](../README.md)

# AWS

<https://github.com/kubernetes-sigs/aws-ebs-csi-driver>
<https://github.com/kubernetes-sigs/aws-efs-csi-driver>

S3 as a filesystem: <https://github.com/awslabs/mountpoint-s3> ·
<https://github.com/s3fs-fuse/s3fs-fuse>

Recorded issue: <https://github.com/kubernetes-sigs/aws-efs-csi-driver/issues/511>

---

## The problem it solves

On EKS, storage is not something you build. It is two CSI drivers and an SDK call:

| Need | AWS service | Driver | Access mode |
|---|---|---|---|
| A disk for a database | **EBS** | `aws-ebs-csi-driver` | `ReadWriteOnce` |
| A shared directory across pods | **EFS** | `aws-efs-csi-driver` | `ReadWriteMany` |
| A lake, backups, chunks | **S3** | none — it is an API | not a PVC |

Installing these replaces everything in [block-storage/](../../block-storage/README.md),
[file-storage/](../../file-storage/README.md) and much of
[object-storage/](../../object-storage/README.md). That is the argument made in full in
[the parent README](../README.md), and this page is the AWS-specific detail underneath it.

Both drivers are **EKS add-ons**, which is the way to install them: managed lifecycle, versions
tied to the cluster version, and IAM wiring that AWS documents. Installing them by Helm is
supported and gives you the upgrade problem back.

### EBS: the default, with decisions in it

EBS volumes behave like local disks and are **zonal**. Everything in
[block-storage](../../block-storage/README.md) applies unchanged, including the detach delay
after node failure — EKS does not make that faster.

What is specific to EBS:

| Parameter | Notes |
|---|---|
| `type` | `gp3` is the sensible default; `gp2` is the legacy one many clusters are still on |
| `iops` / `throughput` | on `gp3`, **provisioned separately from capacity** |
| `io2` / `io2 Block Express` | when you genuinely need very high, guaranteed IOPS |
| `encrypted` + `kmsKeyId` | set it in the StorageClass; there is no reason not to |
| `fsType` | `ext4` or `xfs` |

The `gp3` split is the one that catches people. On `gp2`, IOPS scaled with size, so
over-provisioning capacity was how you bought performance. On `gp3`, a 20 GiB volume and a 2 TiB
volume both start at 3,000 IOPS and 125 MB/s, and more is a separate parameter. A database
migrated from `gp2` to a same-sized `gp3` can therefore get *slower* if the old volume was large
enough to have earned IOPS from its size. Size for IOPS first.

Also worth knowing: **the number of volumes that can attach to a node is limited** and depends on
the instance type, and on Nitro instances the ENIs count against the same budget. A node running
many stateful pods hits it, and the symptom is pods stuck pending with attach errors that look
like a driver fault.

### EFS: RWX with no server to run

EFS is a managed NFS filesystem, **regional** rather than zonal, and it is the strongest single
argument in this folder: the entire [file-storage/](../../file-storage/README.md) folder exists to
avoid operating a file server, and here there is not one.

Two provisioning modes:

| Mode | What happens |
|---|---|
| **Static** | you create the filesystem, the PV references its ID, PVCs bind to it |
| **Dynamic** | the driver creates an **access point** per PVC, each a subdirectory with its own POSIX identity |

Dynamic provisioning via access points is the mode most people want, and the one with the most
sharp edges — access points enforce a UID/GID and a root directory, which interacts with pod
`securityContext` in ways that produce permission errors reading as application bugs.

The properties to internalise before choosing EFS:

- **Latency is NFS latency**, and EFS's is high per operation. Workloads with heavy metadata
  traffic — many small files, directory scans, compilation, `node_modules` — feel it immediately
  and dramatically.
- **Throughput mode matters.** Elastic throughput is the current default and bills per use;
  Bursting mode accumulates credits and can exhaust them, at which point performance collapses
  and the cause is invisible unless you are watching `BurstCreditBalance`.
- **It is still not a database's home.** Managed does not change POSIX semantics over a network.
- **Cost is per GB stored and, in Elastic mode, per GB transferred** — considerably more than
  EBS per GB. EFS used as a dumping ground is a recurring bill surprise.

### S3 is not a PVC

S3 is where the lake, the backups and the observability chunks belong, and applications should
call the API. This is what [MinIO](../../object-storage/minio/README.md) exists to imitate
on-premise, and on EKS there is no reason to run MinIO at all.

The FUSE options exist for applications that only know how to read files:

| Tool | Nature | Verdict |
|---|---|---|
| [Mountpoint for S3](https://github.com/awslabs/mountpoint-s3) | official; read-optimised, sequential-write only, deliberately incomplete | the right choice when a mount is genuinely needed |
| [s3fs-fuse](https://github.com/s3fs-fuse/s3fs-fuse) | community; implements much more of POSIX, less reliably | avoid for new work |

Mountpoint's refusal to implement random writes, `rename` on files, hard links and directory
semantics is the honest design: it does not pretend. s3fs implements more, which produces
applications that appear to work and then encounter the parts that do not. There is also a
`mountpoint-s3-csi-driver` that exposes it as a Kubernetes volume.

The rule from [object-storage](../../object-storage/README.md) stands: **never run a database, a
queue or anything with a write-ahead log on a FUSE-mounted bucket.**

## When to use it

- **Any EKS cluster.** Install the EBS CSI driver as an add-on and use it. This is not a
  decision, it is a prerequisite — a modern EKS cluster ships no in-tree storage driver, so
  without it PVCs simply do not bind.
- **EFS when RWX is genuinely required** and the workload is not latency-sensitive: shared config
  directories, a handful of pods reading the same reference data, legacy applications with a
  hard-coded path.
- **S3 for everything that is not a PVC** — Loki chunks, Thanos blocks, Velero backups, the
  lakehouse, artifacts.
- **Mountpoint for S3** for read-mostly file access from applications that cannot be changed to
  speak S3.

## When not to use it

- **Self-hosted storage instead of these.** Longhorn, Ceph or MinIO on EKS means operating
  distributed storage on top of storage that is already distributed and under an SLA, at
  multiplied cost. Only a named requirement — data residency, cross-cloud portability, a cost
  model that genuinely breaks — justifies it.
- **EFS as a general-purpose filesystem.** Its per-operation latency makes it a poor fit for
  anything metadata-heavy, and the cost per GB makes it a poor fit for bulk data. Use it for
  sharing, not for storing.
- **EFS for a database.** Ever.
- **EBS expecting zone-level resilience.** Volumes are zonal; a stateful workload on EBS is
  pinned to a zone, and surviving a zone failure requires replication in the application.
- **s3fs-fuse for new work** — Mountpoint is the maintained, honest option.
- **A FUSE mount as a write target** for anything transactional.

## Notes

The recorded notes for this folder, translated and placed:

- **[`aws-ebs-csi-driver`](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)** — the block
  driver. Covered above; the `gp3` IOPS split and the per-node attachment limit are the two
  things most often discovered late.
- **[`aws-efs-csi-driver`](https://github.com/kubernetes-sigs/aws-efs-csi-driver)** — the RWX
  driver.
- **[`aws-efs-csi-driver` issue #511](https://github.com/kubernetes-sigs/aws-efs-csi-driver/issues/511)**
  — recorded deliberately as a known-issues pointer. Keeping a specific issue link in a storage
  note is a useful habit, and the reason it is worth doing for this driver in particular is that
  the EFS driver is the least boring component in this folder. Its recurring problem classes are
  worth knowing before committing: mount helper (`efs-utils`/stunnel) behaviour and its per-node
  mount limits, stale mounts surviving node or pod restarts, dynamic provisioning via access
  points and the UID/GID enforcement that comes with them, and reclaim behaviour on access-point
  deletion. Read the current state of the issue rather than trusting a summary — that is why the
  link is kept rather than paraphrased.
- **[`s3fs-fuse`](https://github.com/s3fs-fuse/s3fs-fuse)** and
  **[`mountpoint-s3`](https://github.com/awslabs/mountpoint-s3)** — the two ways to make a bucket
  look like a directory. The distinction between them is in the table above, and the conclusion
  is Mountpoint.

**No manifests exist in this folder**, and that is correct. There is nothing a Kind cluster can
deploy here, and the drivers belong to the EKS cluster's add-on configuration rather than to a
Flux `HelmRelease` in this repository. This page is a reference note.

**Credentials.** Both drivers need IAM permissions, and both should get them through **IRSA or
EKS Pod Identity**, never a static access key in a Secret. The same applies to every application
in this repository that talks to S3 — which, given the list in
[object-storage/minio](../../object-storage/minio/README.md), is most of the observability and
data stack.

**Snapshots.** The EBS driver implements CSI snapshots, but the `VolumeSnapshot` CRDs and the
snapshot controller are a **separate installation** and are not present on every EKS cluster by
default. Without them the objects are created and never reconciled, silently. See
[external-snapshotter](../../../backup/external-snapshotter/README.md) and verify `readyToUse` on
a real snapshot before trusting a backup schedule. The EFS driver does not implement snapshots at
all — back EFS up at file level, with [Velero](../../../backup/velero/README.md) and Kopia or
with [VolSync](../../../backup/volsync/README.md), or with AWS Backup.

---

[← Cloud storage](../README.md)
