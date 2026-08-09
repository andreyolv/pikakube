[← Object storage](../README.md)

# RustFS

<https://github.com/rustfs/rustfs>
<https://artifacthub.io/packages/helm/rustfs/rustfs>

Chart values: <https://github.com/rustfs/rustfs/blob/main/helm/rustfs/values.yaml>

---

> **The recorded assessment is blunt and is kept as recorded**: the documentation is complete
> garbage, and the tag release system is ridiculous. See the [Notes](#notes) — the second
> complaint is the more consequential of the two, and it is the reason this project cannot
> currently be pinned the way everything else in this repository is.

## The problem it solves

RustFS is a recent, Apache-2.0, S3-compatible object store written in Rust, and it exists for one
reason: **MinIO's open-source trajectory left a gap**, and RustFS is an explicit attempt to fill
it with a like-for-like replacement rather than a differently-shaped alternative.

That positioning is the whole pitch, and it is worth being precise about:

| | [MinIO](../minio/README.md) | [Garage](../garage/README.md) | RustFS |
|---|---|---|---|
| Licence | AGPLv3, with capabilities moved to commercial | Apache-2.0 | Apache-2.0 |
| Design goal | high-performance S3 in a datacentre | geo-distributed, small hardware | **a MinIO-shaped replacement** |
| Maturity | very high | moderate, and stable | **low — young project** |
| Erasure coding | yes | replication, not EC | yes |
| Console | yes, reduced in the open edition | none official | yes |
| Ecosystem | enormous | small | **very small** |

The technical claims are plausible: Rust rather than Go, so no garbage-collector pauses; erasure
coding; a web console; the S3 API surface people actually use. If they hold up, it is the closest
thing to a drop-in.

The problem is that "if they hold up" is currently expensive to determine, which is what the
recorded notes are about.

### Maturity is the whole risk

This is a young project. For most software categories that is a manageable risk. For **object
storage** it is not, because of what
[object-storage](../README.md) and [minio](../minio/README.md) record about how load-bearing this
layer is: logs, metrics, traces, backups and the lakehouse all live there. A data-loss bug in an
object store is not a bug you recover from with a rollback.

The things a young object store has not yet accumulated:

- **Time under real workloads.** Erasure coding correctness, recovery paths and behaviour under
  partial failure are proven by years of production use, not by a test suite.
- **A community of operators.** Nobody has seen the failure you are looking at.
- **A track record on security response** and on breaking changes.
- **Migration and upgrade experience** across versions.

None of that is a criticism of the code. It is the honest cost of being new in a category where
being boring is the primary virtue.

## When to use it

- **Evaluation and experimentation**, which is what this folder is for.
- **Non-critical, reproducible data** — a cache, a scratch bucket, artifacts that can be
  regenerated.
- **Tracking the category.** The MinIO gap is real, and knowing whether RustFS matures into an
  answer is worth the attention. This folder exists to keep the option visible.
- Development environments where the S3 API is all that is needed and the data is disposable.

## When not to use it

- **In a cloud.** S3, Blob Storage and GCS. Every tool in this folder loses to the managed
  service on a managed cluster.
- **For production data**, today. The maturity gap above is the reason, and no licence advantage
  compensates for it in a storage layer.
- **As the backing store for backups.** [Velero](../../../backup/velero/README.md) writing
  somewhere is a promise about recovery. That is the last place to put a young component.
- **As the substrate for observability** — [Loki](../../../../observability/logs/storage/loki/README.md),
  [Thanos](../../../../observability/metrics/long-term-storage/thanos/README.md) — whose
  availability requirements are the union of everything that queries them.
- **In any environment where reproducible deployments are required**, until the release and
  tagging problems recorded below are resolved. This is not a preference; an unpinnable
  dependency is incompatible with GitOps.
- **When [Garage](../garage/README.md) would do.** For a small self-hosted deployment Garage is
  the more mature answer with the same licence, and it is what
  [object-storage](../README.md) recommends first.

## Notes

The recorded notes for this tool, translated from the original and preserved in full:

> **The documentation is complete garbage.**
>
> **The tag release system is ridiculous.**

Both are kept as written. The second is the more actionable, and it is worth taking in reverse
order.

**"The tag release system is ridiculous."** This is a concrete, checkable objection and it has a
direct operational consequence. This repository's entire deployment model depends on **pinning**
— every `HelmRepository` pins a chart version, every `GitRepository` pins a tag, and the point is
that a reconcile today produces the same result as a reconcile next month. That discipline is
applied most strictly to storage, where an unattended upgrade is least welcome
([Longhorn](../../block-storage/longhorn/README.md) and
[Rook](../../multi-storage/rook/README.md) are both pinned for exactly this reason).

A project whose tagging is inconsistent — tags that move, releases without tags, tags without
releases, versions that do not correspond to what is built, or a stream of pre-release tags with
no clear stable line — **cannot be pinned meaningfully**. The failure is not cosmetic: it means
"the version we run" is not a well-defined statement, and a rollback target may not exist.

For a storage system this is disqualifying on its own, independently of code quality. Re-check
it before any adoption decision; it is exactly the kind of thing a maturing project fixes, and
the note should be re-verified rather than trusted indefinitely.

**"The documentation is complete garbage."** The same complaint recorded for
[SeaweedFS](../seaweedfs/README.md), and the same reasoning applies: for infrastructure whose
failure mode is "the object store is unavailable", documentation quality is how quickly you
recover, not a matter of polish. A young project with thin documentation compounds the maturity
problem, because there is also no accumulated body of community answers to fall back on.

**The pattern across this folder is the point.** [MinIO](../minio/README.md) has a licence
trajectory problem; [SeaweedFS](../seaweedfs/README.md) has a documentation and
enterprise-boundary problem; RustFS has a maturity and release-hygiene problem;
[Garage](../garage/README.md) is the most solid of the alternatives and is deliberately not
trying to be MinIO. That is precisely the assessment recorded in
[object-storage](../README.md):

> MinIO's open source has effectively died, and the alternatives so far are all weak.

RustFS is recorded here as one of the weak alternatives, with the specific weaknesses named. The
practical conclusion for the platform is unchanged: **if a cloud provides object storage, use
it**, and if self-hosting is required, Garage first.

**How it is deployed here.** A Flux `GitRepository` and a `HelmRelease` in the `rustfs`
namespace, referencing the chart path `helm/rustfs` inside the project's own source tree — the
same pattern used for [Garage](../garage/README.md),
[CubeFS](../../file-storage/cubefs/README.md) and
[local-path-provisioner](../../local/local-path-provisioner/README.md), and itself a small
confirmation that there is no published chart registry.

The values set here are deliberately minimal and deliberately modest:

| Value | Set to | Meaning |
|---|---|---|
| `replicaCount` | `1` | a single instance |
| `mode.standalone.enabled` | `true` | no erasure coding, no distribution |
| `mode.distributed.enabled` | `false` | the distributed mode is explicitly off |
| `ingress.enabled` | `false` | not exposed |

**Standalone mode with one replica has no durability mechanism at all** — the same caveat as a
single-node MinIO, recorded in [minio/](../minio/README.md#what-to-get-right). That is the correct
configuration for an evaluation entry and the wrong one for anything else. Read it as: this is
here to be looked at, not to be depended on.

---

[← Object storage](../README.md)
