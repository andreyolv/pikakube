[← Object storage](../README.md)

# SeaweedFS

<https://github.com/seaweedfs/seaweedfs>
<https://artifacthub.io/packages/helm/seaweedfs/seaweedfs>

Chart values: <https://github.com/seaweedfs/seaweedfs/blob/master/k8s/charts/seaweedfs/values.yaml>

---

> **The recorded assessment is blunt and is kept as recorded**: the documentation is complete
> garbage, the focus is enterprise, and the open-source offering is bait for the gullible. See
> the [Notes](#notes) for what that means in practice and what is and is not fair about it.

## The problem it solves

SeaweedFS is a distributed object store built around a specific insight: **most object stores
handle billions of small files badly**, because they treat every object as a first-class entity
with its own metadata record, and metadata becomes the bottleneck long before storage does.

Its answer is borrowed from Facebook's Haystack paper. Small files are packed into large
**volumes** (30 GB by default), and an object is addressed by a compact file ID — a volume number
plus an offset. Looking up an object is one lookup and one seek, and the master server only has
to track volumes, not files.

| Component | Role |
|---|---|
| **Master** | tracks volumes and their locations; Raft-replicated, so an odd number |
| **Volume server** | stores the volumes and serves reads and writes directly |
| **Filer** | optional — adds a directory tree, backed by a metadata store you choose |
| **S3 API server** | optional — the S3-compatible gateway, built on the Filer |
| Mount / WebDAV / FUSE | further access layers on top of the Filer |

The layering matters. **Plain SeaweedFS is not S3 and has no directories** — it is a blob store
addressed by file ID. Directories come from the Filer, and S3 comes from a gateway on top of the
Filer. Each layer adds a component, and the Filer adds a metadata store dependency (LevelDB,
Redis, MySQL, PostgreSQL, Cassandra) with the same single-point-of-failure logic as
[JuiceFS's metadata engine](../../file-storage/juicefs/README.md).

That is the most important structural fact about SeaweedFS and the one the documentation makes
hardest to discover.

### What it is genuinely good at

Setting aside the assessment above, the technical claims hold up:

- **Billions of small files.** This is the design target and it is met. Where MinIO or Ceph RGW
  struggle with enormous object counts, SeaweedFS was built for exactly that.
- **Fast, cheap reads.** One lookup, one seek, no metadata database in the read path for plain
  blob access.
- **Erasure coding**, tiering to cloud storage, and cross-datacentre replication.
- **Very broad feature surface** — S3, POSIX mount, WebDAV, a CSI driver, remote gateway,
  Kubernetes integration.
- **Apache-2.0.**

The breadth is genuine and it is also part of the problem: a project that does this many things
has that many things to document, and does not.

## When to use it

- **Billions of small files**, where the object-count profile is the actual constraint and other
  stores hit metadata limits. This is the case where SeaweedFS is the right answer and few
  alternatives are.
- **When someone on the team will read the source.** The code is clear; the documentation is
  not. That is a workable trade for a team willing to make it, and a bad one otherwise.
- **Existing deployments**, which work — the concern recorded here is trajectory and
  documentation, not correctness.
- Experimentation and evaluation, with the caveats below applied.

## When not to use it

- **In a cloud.** Use S3, Blob Storage or GCS. This applies to everything in this folder.
- **When the object-count profile is not the problem.** If you need ordinary S3 for Loki chunks,
  Velero backups and a lakehouse, [Garage](../garage/README.md) is simpler and
  [MinIO](../minio/README.md) is better documented. Choosing SeaweedFS without the small-files
  requirement means taking on its complexity for none of its advantage.
- **When documentation quality is a real constraint** — which for a storage system in a
  production platform it usually is. Operating a component you cannot get straight answers about
  is a risk that shows up during an incident.
- **When an unambiguous open-source boundary is required.** See the Notes.
- **Without deciding the Filer's metadata store deliberately.** The default is easy and the
  consequences are the same as every other metadata-server architecture in this repository.
- **On a single node**, expecting durability. Replication across one machine is copies on one
  disk.

## Notes

The recorded note for this tool, translated from the original and preserved in full:

> **Documentation is complete garbage, the focus is enterprise, the open source is bait for the
> gullible.**

Kept as written, because it is the recorded assessment and because softening it would misrepresent
the evaluation. Three parts, each worth separating.

**"Documentation is complete garbage."** This is the least controversial part and it is a
substantive objection, not a stylistic one. SeaweedFS's documentation lives largely in a GitHub
wiki, is organised by feature rather than by task, frequently describes capabilities without
stating which components they require, and rarely gives a complete working configuration. The
layering described above — blob store, then Filer, then S3 gateway, each with its own dependencies
— is exactly the kind of thing that needs a clear architectural page and does not have one. The
practical result is that evaluating SeaweedFS means reading the source or the Helm chart's values
file to find out what actually exists.

For a component whose failure mode is "the object store is unavailable", that is a legitimate
disqualifier. Documentation quality is not a cosmetic property of infrastructure software; it is
how fast you recover.

**"The focus is enterprise."** The project has a commercial offering, and the concern recorded
here is the familiar one: features and attention drifting toward the paid edition, with the open
version documented in a way that does not make the boundary clear. This is the same pattern
recorded for [JuiceFS](../../file-storage/juicefs/README.md), where "enterprise" appears in the
docs without context, and it is the pattern that made
[MinIO's trajectory](../minio/README.md) a problem in the first place.

**"The open source is bait for the gullible."** The strongest claim, and the one to hold most
loosely. In fairness: SeaweedFS is Apache-2.0, the code is public, and there is no evidence of
features being removed from the open edition the way MinIO removed console functionality. The
grievance being expressed is about **expectations** — an open-source project whose documentation
is poor enough that you cannot tell what you are getting, and whose commercial version is the
path of least resistance, functions as a funnel whether or not it was designed as one.

Read the whole note as: *SeaweedFS is technically real and open, and evaluating it costs far more
effort than it should, in a way that consistently benefits the commercial offering.* That is a
fair summary, and it is a legitimate reason to prefer [Garage](../garage/README.md) for a small
self-hosted deployment.

**This is the state of the category, not a preference.** As [object-storage](../README.md)
records: MinIO's open source has effectively died and the alternatives are all weak. SeaweedFS is
one of the weak alternatives, and the specific weakness is documented here rather than glossed
over. The practical conclusion is unchanged: **if a cloud provides object storage, use it.**

**How it is deployed here.** A Flux `HelmRelease` named `seaweedfs` in the `seaweedfs` namespace,
pinned to chart version `4.0.398`, from a `HelmRepository`, with an empty values block and the
upstream values file linked in a comment.

The empty values block is more consequential here than elsewhere, because the values file is
where you discover **which components exist at all**: `master`, `volume`, `filer`, `s3`, `sftp`,
`allInOne` and their dependencies are all toggles. There is no single "install SeaweedFS" — there
is a set of components to enable, and the values file is, in practice, the architecture
documentation. That is the concrete form the complaint above takes.

Also note the chart's version numbering (`4.0.398`) tracks the project's own scheme, which
advances quickly. Pinning it is correct; so is checking what changed before moving it.

**In this repository it is an evaluation entry**, not a running dependency. The tooling that needs
object storage points at [MinIO](../minio/README.md). This folder exists so the alternative is
understood — including the reasons not to choose it.

---

[← Object storage](../README.md)
