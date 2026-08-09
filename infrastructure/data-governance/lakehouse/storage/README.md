[← Lakehouse](../README.md)

# Storage

Where the bytes live, and what stops their cost growing without a ceiling.

Covered here: [`minio/`](minio/README.md) — client-side examples against S3-compatible storage ·
[`azure-lifecycle-policy/`](azure-lifecycle-policy/README.md) — tiering and expiry rules, worked
through on Azure Blob

## Contents

1. [What this folder is, and is not](#1-what-this-folder-is-and-is-not)
2. [Why S3-compatible is the interface](#2-why-s3-compatible-is-the-interface)
3. [Lifecycle policies: the only thing that caps cost](#3-lifecycle-policies-the-only-thing-that-caps-cost)
4. [Storage classes and tiering](#4-storage-classes-and-tiering)
5. [The small-files problem, from the storage side](#5-the-small-files-problem-from-the-storage-side)
6. [Notes](#6-notes)
7. [Anti-patterns](#7-anti-patterns)
8. [How this applies to pikakube](#8-how-this-applies-to-pikakube)

---

## 1. What this folder is, and is not

Object storage is the bottom layer of the lakehouse — [`../README.md`](../README.md) puts it first
in the four layers, and everything above it assumes it works.

**This folder is the governance and client-side view of that layer.** It holds the examples for
talking to object storage from code, and the lifecycle policy work that decides how long data
lives. It does **not** document the storage system itself.

The storage system is documented where it belongs, in infrastructure:

| Concern | Where |
|---|---|
| Running MinIO — erasure coding, tenants, capacity, the licence situation | [`site-reliability-engineering/storage/object-storage/minio/`](../../../site-reliability-engineering/storage/object-storage/minio/README.md) |
| The object storage category and its alternatives | [`site-reliability-engineering/storage/object-storage/`](../../../site-reliability-engineering/storage/object-storage/README.md) |
| **Accessing** buckets and objects from code | [`minio/`](minio/README.md) — here |
| **Deciding how long data lives** | [`azure-lifecycle-policy/`](azure-lifecycle-policy/README.md) — here |

That split is deliberate. Whether erasure coding is configured correctly is a reliability question;
whether a directory has an owner and an expiry date is a governance question, and they are answered
by different people.

## 2. Why S3-compatible is the interface

The S3 API became the interface for object storage the way SQL became the interface for relational
data — not because it is elegant, but because everything speaks it.

The practical consequence for a lakehouse is that **the storage decision stops constraining
everything above it**. The same [table format](../table-formats/README.md), the same engine, the
same client library and the same code work against AWS S3, MinIO, Garage, SeaweedFS or Azure via a
compatibility layer, with an endpoint change.

That is also why the client examples here are worth having. `boto3` is the AWS SDK, and it is what
you use to talk to MinIO — the same calls, a different `endpoint_url`. See
[`minio/boto3/`](minio/boto3/README.md).

The compatibility is not total, and the gaps are where time goes:

| Usually works | Frequently differs |
|---|---|
| bucket and object CRUD, listing, multipart upload | lifecycle rule support and semantics |
| versioning, tagging, bucket policies | storage classes and what tiering actually does |
| pre-signed URLs | object lock, legal hold and retention modes |
| server-side encryption (varies by backend) | notifications, replication, and their configuration shape |

**Path-style versus virtual-host-style addressing** is the specific thing that breaks first against
self-hosted storage. Every configuration in this repository that talks to MinIO sets
`path_style_access` or its equivalent, and forgetting it produces a DNS error that looks like
anything but a configuration problem.

## 3. Lifecycle policies: the only thing that caps cost

Object storage has no natural limit. Nothing deletes anything, ever, unless something is configured
to. A lakehouse makes that worse rather than better, because the formats deliberately keep old
data:

| Source of growth | Why it accumulates |
|---|---|
| **Table snapshots** | time travel means old file versions are retained on purpose |
| **Orphan files** | failed writes leave files nothing references and nothing cleans |
| Small files from streaming | thousands per day per partition |
| **Object versions** | versioning keeps every overwrite, including the ones nobody wanted |
| Delete markers | a "deleted" object in a versioned bucket still occupies space |
| Landing zones and scratch space | temporary by intent, permanent in practice |

A lifecycle policy is a rule the storage system evaluates by itself: after N days, move this prefix
to a cheaper tier; after M days, delete it. **It is the only mechanism that caps growth without
someone remembering to run something**, which is why it is the one control in this folder that is
not optional.

The trigger conditions are worth knowing apart, because choosing the wrong one is the common
mistake:

| Trigger | Means | Good for |
|---|---|---|
| **Creation** | days since the object was written | landing zones, immutable batch drops |
| **Modification** | days since it last changed | working areas that are updated in place |
| **Last access** | days since it was last read | **archival decisions** — the one that reflects actual value |
| Version age | days since a version became non-current | controlling the cost of versioning |

Last-access is the most useful and the least used, because it answers the question people actually
have: *is anyone still reading this?* It is also the one whose support varies most between
providers — verify it exists before designing a policy around it.

The worked example is in [`azure-lifecycle-policy/`](azure-lifecycle-policy/README.md), including
the harder-than-expected question of **how rules get attached to data in the first place** — by
path, or by tag, and who is allowed to set the tag.

## 4. Storage classes and tiering

Tiering trades retrieval latency and cost for storage cost. The shape is consistent across
providers even where the names are not: hot, cool/infrequent, cold, archive.

| | What you gain | What you pay |
|---|---|---|
| Hot → cool | lower storage cost | higher per-request cost |
| Cool → cold | lower again | higher again, plus minimum retention periods |
| Cold → archive | **much** lower | **retrieval takes hours**, and early deletion is charged |

Three things reliably go wrong:

**Minimum retention periods.** A tier frequently bills a minimum number of days regardless of when
the object is deleted. Tiering data that gets deleted a week later costs more than leaving it hot.

**Archive is not storage, it is a restore request.** Data in archive is not readable — it must be
rehydrated first, which takes hours. A query engine pointed at archived files does not run slowly;
it fails.

**Never archive table metadata.** Manifests, transaction logs and snapshot pointers are small,
constantly read, and the table is unreadable without them. Lifecycle rules over a lakehouse bucket
must be scoped to data prefixes, or they break the table while saving nothing — the metadata is a
rounding error in the bill.

## 5. The small-files problem, from the storage side

[`table-formats/`](../table-formats/README.md#5-the-part-everyone-forgets-maintenance) covers this
as a query-performance problem. From the storage side it is a **cost and operations** problem, and
the two look nothing alike:

| Consequence | Detail |
|---|---|
| **Request cost** | object storage bills per request; ten thousand small objects cost ten thousand GETs, not one |
| **Listing cost** | listing a prefix is paginated and slow; the table's metadata exists partly to avoid it |
| **Per-object overhead** | metadata per object is not free, and at scale it is a real number |
| **Lifecycle evaluation** | rules are evaluated per object; millions of tiny objects makes that expensive too |
| Erasure coding overhead | on a self-hosted system, small objects carry proportionally more overhead |

The conclusion is the same from both directions: **compaction is not an optimisation, it is
maintenance.** The difference is that from the storage side it shows up on the bill before it shows
up in a query, which means finance frequently notices before the data team does.

## 6. Notes

Recorded here as the mapping that a governed lake needs, per directory:

| Per-directory mapping | Why it matters |
|---|---|
| **Lake owners** | who is accountable for the data in this path |
| **Permissions for service principals and users** | who and what can read or write it |
| **Data lifecycle policy** | how long it lives, and where it is tiered to |
| **Size in GB** | what it costs, attributable to an owner |
| **Read/write transactions** | whether anyone actually uses it |

That list is a governance model, not a monitoring wish-list, and it is worth reading as one.

**Directory-level is the right granularity** because it is the granularity the storage system
itself can act on. Lifecycle rules filter on prefixes; permissions are granted on prefixes; cost is
attributable by prefix. A model built on anything finer cannot be enforced by the storage system,
and a model built on anything coarser cannot distinguish a landing zone from a curated table.

**The last two rows are what make the first three enforceable.** Size per directory turns storage
cost into something with an owner's name against it, and transaction counts answer the question
that lifecycle policy design actually depends on: is anyone reading this? A directory with an
owner, a size and no reads for six months is a policy decision waiting to be made, and without
those two numbers the conversation never starts.

The path-versus-tag question that follows from this — whether the policy is decided by where data
sits or by a tag someone applies — is worked through with the Azure examples in
[`azure-lifecycle-policy/`](azure-lifecycle-policy/README.md), and the conclusion there is not the
obvious one.

## 7. Anti-patterns

| Anti-pattern | Why it is bad | What to do instead |
|---|---|---|
| **No lifecycle policies** | cost grows with no ceiling, and nobody owns the growth | a rule per prefix, from day one |
| Versioning on with no version expiry | every overwrite kept forever, invisibly | a non-current version rule alongside it |
| Lifecycle rules over table metadata | archived manifests make the table unreadable | scope rules to data prefixes |
| Archive tier for anything queried | rehydration takes hours; queries fail rather than slow | cool or cold, not archive |
| Tiering data with a short life | minimum retention periods cost more than staying hot | check the minimum before tiering |
| One bucket for everything | no cost attribution, no blast radius, no separate policy | a bucket or prefix per domain, with an owner |
| **One root credential everywhere** | no granularity and no revocation | scoped keys per consumer |
| Directories with no owner | nobody can approve deleting anything, so nothing is deleted | the per-directory mapping in section 6 |
| No compaction | request costs and listing costs, before query time even suffers | schedule it — see [`table-formats/`](../table-formats/README.md) |
| Backups stored in the system being backed up | the backup does not survive the failure it exists for | a separate failure domain |

## 8. How this applies to pikakube

The storage system is **MinIO**, and it is the most depended-upon component in this repository that
is not Kubernetes itself — the full argument, along with the AGPL licence trajectory and the
alternatives, is in
[`site-reliability-engineering/storage/object-storage/minio/`](../../../site-reliability-engineering/storage/object-storage/minio/README.md).

What is recorded in this folder:

| Folder | State |
|---|---|
| [`minio/`](minio/README.md) | working `boto3` and `minio` client examples against the in-cluster endpoint, plus a Spark Parquet round-trip |
| [`minio/boto3/`](minio/boto3/README.md) | three notebook sets — the low-level client, the resource API, and the native MinIO SDK |
| [`azure-lifecycle-policy/`](azure-lifecycle-policy/README.md) | real Azure Blob policy JSON, a naming convention, and the recorded reasoning about path versus tag |

The Azure material sitting in an otherwise self-hosted repository is not an inconsistency: **the
lifecycle problem is provider-independent and the reasoning transfers directly.** The rule
structure is nearly the same shape in the S3 API — the
[`06-lifecycle`](minio/boto3/boto3-client/README.md) notebooks configure the equivalent against
MinIO — and the hard part was never the JSON. It was deciding who owns a prefix and what happens to
data nobody reads, which is the same question everywhere.

The two capabilities that depend directly on this layer:
[`table-formats/`](../table-formats/README.md), whose maintenance jobs are what keep the storage
bill flat, and [lakeFS](../version-control/lakefs/README.md), which sits in front of object storage
and versions the whole bucket.

---

[← Lakehouse](../README.md)
