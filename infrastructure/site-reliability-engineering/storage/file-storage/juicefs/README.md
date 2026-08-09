[← File storage](../README.md)

# JuiceFS

<https://github.com/juicedata/juicefs>
<https://github.com/juicedata/juicefs-csi-driver>
<https://github.com/juicedata/juicefs-operator>
<https://github.com/juicedata/charts>

Deployment shapes: [`juicefs-csi-driver/`](juicefs-csi-driver/README.md) — PVCs for pods ·
[`juicefs-s3-gateway/`](juicefs-s3-gateway/README.md) — an S3 API over the same filesystem

---

## The problem it solves

Object storage is cheap, durable and effectively unlimited. It is also
[not a filesystem](../../object-storage/README.md) — no directories, no locking, no partial
writes, no POSIX semantics — and a large amount of software only knows how to read files.

JuiceFS closes that gap properly, and it is the most architecturally interesting tool in this
folder because of **how** it closes it.

It stores nothing itself. It **composes two systems** into a POSIX filesystem:

| Half | Holds | Backed by |
|---|---|---|
| **Data** | file contents, split into chunks and written as objects | S3, MinIO, Azure Blob, GCS, Ceph RGW — any object store |
| **Metadata** | the directory tree, inodes, file attributes, timestamps, locks | **a separate database**: Redis, PostgreSQL, MySQL or TiKV |

Every file operation splits across the two. `read()` and `write()` go to object storage. `stat`,
`readdir`, `rename`, `chmod`, `flock` — every metadata operation — goes to the database.

The result is a real filesystem: mountable, POSIX-compliant, with working file locking and atomic
rename, over a bucket. Unlike a FUSE driver such as `s3fs` or BlobFuse, which
[fakes a filesystem over object storage](../../cloud/aws/README.md#s3-is-not-a-pvc) and cannot
provide those guarantees, JuiceFS provides them because the guarantees live in the database, not
in the bucket.

### The metadata engine is a hard dependency and a single point of failure

This is the sentence to take away from this file, and it deserves to be uncomfortable.

The objects in the bucket are **chunks named by hash**. They are not files. There is no directory
structure in the bucket, no filenames, no way to reconstruct the tree by looking at it. The
mapping from "the file `/data/reports/2026-q1.parquet`" to "these seventeen objects, in this
order" exists in exactly one place: the metadata engine.

| Failure | Consequence |
|---|---|
| Object storage unavailable | file contents unreadable; the filesystem still lists correctly |
| Object storage loses data | those files are corrupt or truncated |
| **Metadata engine unavailable** | **the entire filesystem is unavailable** — every mount hangs |
| **Metadata engine loses data** | **the entire filesystem is unrecoverable** — every byte is still in the bucket, and none of it is addressable |

The last row is the one that catches people. A perfectly healthy S3 bucket containing every chunk
of every file is worthless without the metadata. Recovery is not "difficult" — there is no
supported path.

And the default deployment makes this easy to get wrong. Redis is the most commonly used metadata
engine because it is fast and easy to start. A single-replica Redis with `appendonly no` — the
default in many charts — holds the entire filesystem's index in memory, writes it to disk
occasionally, and loses everything on an ungraceful restart.

So the honest framing is: **JuiceFS does not remove operational burden, it moves it.** You stop
operating a filesystem and start operating a database that must never lose a write. Whether that
is a good trade depends entirely on whether you are better at running
[Redis](../../../../databases/nosql/key-value/redis/README.md) or
[PostgreSQL](../../../../databases/sql/postgresql/README.md) than at running a filesystem. For
many teams the answer is genuinely yes — which is the case for JuiceFS, made properly.

### Choosing the metadata engine

| Engine | Speed | Durability story | Notes |
|---|---|---|---|
| **Redis** | fastest | needs AOF `appendfsync always` plus replication, and is still RAM-bound | the default choice, and the most common way to lose a filesystem |
| **PostgreSQL** | good | transactional and well understood; back it up like any database | the sensible default for most teams |
| **MySQL / MariaDB** | good | same | if that is what you already run |
| **TiKV** | good | distributed and horizontally scalable | for very large filesystems; see [TiKV](../../../../databases/distributed/key-value/tikv/README.md) |
| SQLite | — | single node, no concurrency | testing only |

Metadata capacity is RAM-bound on Redis and roughly linear in file count everywhere. This is the
same architectural pattern as [HDFS's NameNode](../../block-storage/hdfs/namenode/README.md) and
[MooseFS's master](../../on-premisse/README.md#21-moosefs-and-glusterfs) — one component that
knows where everything is. Recognising the pattern is more valuable than any of the three tools.

**Back up the metadata engine on a schedule, and test restoring it.** JuiceFS has a `dump`
command that exports metadata to a portable file; a scheduled dump stored somewhere other than
the metadata engine is the difference between an outage and a total loss.

### What it is good at

Setting aside the warning, the properties are real:

- **Effectively unlimited capacity**, at object-storage prices rather than provisioned block
  volume prices.
- **Genuine RWX** across any number of nodes, with working POSIX locking — which is more than NFS
  reliably provides.
- **Aggressive local caching.** Chunks are cached on the node's disk, so repeated reads do not
  return to the bucket. For read-heavy workloads over a warm cache, performance is much better
  than the architecture suggests.
- **Data survives the cluster.** The bucket is independent of Kubernetes.
- **Compression and encryption at rest**, applied before objects are written.

## When to use it

- **Very large shared datasets** where the volume makes provisioned block storage or a filer
  expensive: training data, model artifacts, media, scientific data.
- **Read-heavy, write-once workloads** — the caching model is built for this, and it is where
  JuiceFS beats NFS rather than merely matching it.
- **When object storage already exists** and is already operated well, and a POSIX view of it is
  the missing piece.
- **When the team is genuinely good at running a database.** This is the real precondition, and
  it is worth stating as one.
- **Cross-cluster or hybrid access** — the same filesystem mounted from several clusters, since
  neither half lives in Kubernetes.
- With the [S3 gateway](juicefs-s3-gateway/README.md), when applications should see an S3 API
  over the same data.

## When not to use it

- **Without a highly available, durable metadata engine.** A single-replica Redis without AOF is
  a filesystem waiting to be deleted by a restart. If you cannot commit to running that database
  properly, use something else.
- **For latency-sensitive small-file workloads.** Every metadata operation is a database round
  trip and every cache miss is an object GET. It is not a local disk.
- **For a database.** Yes, it is POSIX and yes, locking works — and it is still object storage
  with a network in the write path. The rule in
  [file-storage §4](../README.md#4-what-breaks-on-a-network-filesystem) stands.
- **When NFS would do.** A shared config directory does not need a distributed filesystem with a
  database dependency.
- **When simplicity is the priority.** The full deployment is: an object store, a database, a CSI
  driver, mount pods, and a cache tier. That is four things that can be down.
- **Assuming the operator is a supported open-source path** — see the Notes, which is the
  recorded caveat for this tool.

## Notes

The recorded note for this tool, translated from the original:

> **The JuiceFS operator has no licence — I think it is enterprise. The documentation is not very
> clear; it talks about "enterprise" in the docs with no context at all.**

This is a real and useful observation, and it is worth unpacking because it describes the whole
project's documentation problem, not just one repository.

**On the licence.** A repository published without a `LICENSE` file is, legally, **all rights
reserved** — the absence of a licence is not permissiveness, it is the default of copyright.
Public visibility on GitHub grants the right to view and fork within GitHub's terms, and nothing
else: no right to use, modify or deploy. So the instinct recorded here is correct in its
practical conclusion — treat an unlicensed repository as unusable in a production platform until
its terms are explicit. Check the current state of
<https://github.com/juicedata/juicefs-operator> before relying on it; this kind of thing does get
corrected, and the note should be re-verified rather than trusted forever.

**On "enterprise" appearing without context.** JuiceFS ships in two editions — a Community
Edition (Apache-2.0, the [`juicefs`](https://github.com/juicedata/juicefs) repository) and a
closed-source Enterprise Edition whose main difference is a proprietary distributed metadata
engine that replaces Redis/PostgreSQL. The documentation covers both, and frequently describes a
feature without stating which edition it belongs to. The practical effect is exactly what the
note says: you read a page, plan around a capability, and discover later that it was an
Enterprise feature.

The rule that follows: **when reading JuiceFS documentation, establish which edition every page
is describing before treating anything as available.** This is the same class of problem recorded
for [SeaweedFS](../../object-storage/seaweedfs/README.md) and
[RustFS](../../object-storage/rustfs/README.md), and it is the single most common reason a
self-hosted storage evaluation goes wrong.

**The consequence for this repository** is that the operator is not used here. The two deployment
shapes present — [`juicefs-csi-driver/`](juicefs-csi-driver/README.md) and
[`juicefs-s3-gateway/`](juicefs-s3-gateway/README.md) — are both installed from
[`juicedata/charts`](https://github.com/juicedata/charts), the Helm chart repository, which is the
supported community path.

**The remaining links, and what each is:**

| Repository | What it is |
|---|---|
| [`juicefs`](https://github.com/juicedata/juicefs) | the filesystem itself — the client, the `juicefs` CLI, `format`, `mount`, `dump` |
| [`juicefs-csi-driver`](https://github.com/juicedata/juicefs-csi-driver) | the Kubernetes driver — see [`juicefs-csi-driver/`](juicefs-csi-driver/README.md) |
| [`juicefs-operator`](https://github.com/juicedata/juicefs-operator) | the operator, with the licence caveat above |
| [`charts`](https://github.com/juicedata/charts) | the Helm charts, and the source used here |

**How it is deployed here.** Both shapes are Flux `HelmRelease` objects in the `juicefs`
namespace, sourced from a shared `HelmRepository` named `juicefs` and pinned — `0.28.4` for the
CSI driver, `0.11.3` for the S3 gateway. The CSI driver's values define a `juicefs-sc`
StorageClass with the backend fields left as placeholders (`<meta-url>`, `<bucket>`,
`<access-key>`, `<secret-key>`), which is correct: the metadata engine and bucket are the
deployment-specific decisions, and putting real ones in Git would be the wrong kind of concrete.
Note that those credentials belong in a Secret rather than inline in the `HelmRelease` values
once they are real.

---

[← File storage](../README.md)
