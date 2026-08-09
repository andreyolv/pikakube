[← Object storage](../README.md)

# Garage

<https://github.com/deuxfleurs-org/garage>
<https://garagehq.deuxfleurs.fr/documentation/>
<https://github.com/khairul169/garage-webui>

Chart values: <https://github.com/deuxfleurs-org/garage/blob/main-v2/script/helm/garage/values.yaml>

---

## The problem it solves

[MinIO's open-source position has deteriorated](../minio/README.md), and the alternatives are
thin. Garage is the least thin of them, and the one worth reaching for first when self-hosting
S3-compatible object storage on a small cluster.

It comes from [Deuxfleurs](https://deuxfleurs.fr), a French non-profit hosting collective, and
its design goals are unusual in a useful way. It was built to run on **cheap, heterogeneous,
geographically scattered hardware over ordinary internet links** — second-hand machines in
members' homes, not a rack with a 10GbE fabric.

Everything distinctive about it follows from that:

| Property | Consequence |
|---|---|
| **Apache-2.0** | permissive, and unambiguously so — the reason it is first on the list |
| Written in Rust, single static binary | ~100 MB of RAM at rest; it runs on a Raspberry Pi |
| **No consensus protocol** | no Raft, no quorum to lose; CRDT-based metadata, eventually consistent |
| **Geo-distribution as a first assumption** | replication zones are part of the model, not a bolt-on |
| No special hardware requirements | ordinary disks, ordinary networks |
| Small conceptual surface | nodes, a layout, zones, buckets, keys |

The absence of a consensus protocol is the most interesting choice. Where
[Ceph](../../multi-storage/README.md) stops entirely when MON quorum is lost, Garage's nodes
converge through CRDTs — so a partitioned or briefly unreachable node degrades rather than halts
the cluster. The cost is that it is **eventually consistent** for some operations, which is a
real trade and one to understand before assuming S3 semantics.

### What it is not

- **Not a MinIO drop-in for every feature.** It implements the core S3 API well — buckets,
  objects, multipart uploads, presigned URLs — and does not implement everything MinIO does.
  Verify the specific API surface your tooling needs.
- **Not built for peak throughput.** It is built for durability across unreliable links on modest
  hardware. On a single fast machine, MinIO will be faster.
- **Not a large ecosystem.** The community is small, the documentation is good but not vast, and
  the number of people who have run it at scale is limited.
- **No official web console.** [garage-webui](https://github.com/khairul169/garage-webui) is a
  third-party UI; see the Notes.

## When to use it

- **Self-hosted S3 on a small cluster**, where the licence trajectory recorded in
  [object-storage](../README.md) makes MinIO an uncomfortable long-term choice. This is the
  primary case and Garage is the current best answer.
- **Genuinely geo-distributed storage** across sites with ordinary connectivity — the case it was
  designed for, and where it beats every alternative here.
- **Small, resource-constrained deployments**: homelab, edge, a single small VM, a Raspberry Pi
  cluster.
- **When Apache-2.0 matters** and AGPL does not fit the situation.
- **As a backup target** for [Velero](../../../backup/velero/README.md) or similar, on a separate
  machine from the cluster being backed up — which is the arrangement backups need anyway.

## When not to use it

- **In a cloud.** S3, Blob Storage and GCS exist, are cheaper than operating anything, and are
  more durable. See [cloud/](../../cloud/README.md). This applies to every tool in this folder.
- **For maximum throughput on one big machine.** That is not what it optimises for.
- **When strict read-after-write consistency is assumed everywhere.** The CRDT model is eventually
  consistent for some operations; check against what your consumers assume.
- **When a specific S3 feature is required** — object lock, versioning, complex lifecycle rules,
  bucket notifications — without verifying it is implemented.
- **As the substrate for everything at scale.** The list in
  [minio/](../minio/README.md#why-it-is-load-bearing-here) — Loki, Thanos, Tempo, Velero, the
  lakehouse — describes a component whose availability requirements are the union of everything
  that reads it. Garage can serve that on a small platform; at large scale, verify before
  committing.
- **When a polished admin UI is a requirement.** The official interface is a CLI.

## Notes

The recorded notes for this tool, preserved and explained.

**<https://github.com/deuxfleurs-org/garage>** — the project itself. Two things worth knowing
about the repository:

- The **organisation was renamed** to `deuxfleurs-org`, and the canonical development home is
  actually a self-hosted Forgejo instance (`git.deuxfleurs.fr`) with GitHub as a mirror. Older
  links point at `Deuxfleurs/garage`. Consistent with the project's ethos, and mildly
  inconvenient when searching for issues.
- The chart lives **inside the source tree** at `script/helm/garage`, not in a chart registry —
  which is why this folder installs from a `GitRepository`.

**<https://github.com/khairul169/garage-webui>** — a **third-party** web UI for Garage, recorded
here because Garage ships no official console and this is the usual answer to "how do I see what
is in it".

Two honest caveats. It is a community project by an individual, so it is not covered by Garage's
release process, security review or compatibility guarantees — treat it as an operational
convenience, not as infrastructure. And it necessarily holds **admin credentials** for the
Garage cluster, because that is what it is for; it should not be exposed without authentication
in front of it. The supported interface remains the `garage` CLI, and anything that must be
reproducible should go through that rather than through a UI.

This is a genuine functional gap against MinIO, whose console is a real part of its appeal — and
it is worth weighing honestly rather than dismissing, because "there is no way to browse the
buckets" is a complaint you will hear.

**How it is deployed here.** A Flux `GitRepository` pointing at the Garage repository, with a
`HelmRelease` in the `garage` namespace referencing the chart path `script/helm/garage`, and an
empty values block with the upstream values file linked in a comment. This is the repository's
standard pattern for charts inside a project's source tree — the same shape used for
[CubeFS](../../file-storage/cubefs/README.md), [RustFS](../rustfs/README.md) and
[local-path-provisioner](../../local/local-path-provisioner/README.md).

Note the chart path references the `main-v2` branch in the values comment, which is a reminder to
pin the `GitRepository` at a tag rather than tracking a branch — a moving branch reference for a
storage system is exactly the unattended upgrade you least want.

**The layout is the concept to learn.** Garage does not auto-configure. After the nodes start you
must assign a **layout**: each node is given a zone, a capacity and a role, and the layout is then
applied as an explicit versioned change. Until that happens the cluster stores nothing. This is
different from MinIO, where the topology comes from the deployment arguments, and it is the most
common first-run confusion.

The zone concept is where the geo-distribution design shows: Garage places replicas across zones,
so declaring zones honestly — one per site, or per rack — is what makes the replication
meaningful. Declaring one zone for every node gives you copies with no failure-domain separation,
the same mistake as `failureDomain: host` on a single-node
[Ceph](../../multi-storage/rook/README.md).

**Credentials and buckets** are created through the `garage` CLI (or the admin API): a key pair
per consumer, with per-bucket permissions. That is the model recommended in
[object-storage](../README.md) — a bucket per consumer with its own policy — and Garage makes it
the natural path rather than an extra step.

**In this repository it is the recorded alternative**, not a running dependency. The tooling here
that needs object storage points at [MinIO](../minio/README.md). Garage is what
[object-storage](../README.md) names as the most promising replacement for a small self-hosted
deployment, and this folder exists so that the option is understood before it is needed.

---

[← Object storage](../README.md)
