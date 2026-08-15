[← Object storage](../README.md)

# COSI — Container Object Storage Interface

<https://github.com/kubernetes-sigs/container-object-storage-interface>

<https://container-object-storage-interface.github.io>

What CSI is for volumes, COSI intends to be for buckets: a vendor-neutral API for **provisioning a
bucket and getting credentials to it** from inside Kubernetes.

---

## The problem it solves

Every consumer listed at the top of [`../README.md`](../README.md#why-this-matters-more-than-it-looks)
— [Loki](../../../../observability/logs/storage/loki/README.md),
[Thanos](../../../../observability/metrics/long-term-storage/thanos/README.md),
[Tempo](../../../../observability/tracing/storage/tempo/README.md),
[Velero](../../../backup/velero/README.md), the lake — needs the same two things before it can
start: **a bucket that exists, and a credential that can write to it.** Neither is a Kubernetes
object. So each one is created somewhere else:

| Where the bucket comes from today | What it costs |
|---|---|
| The cloud console, by hand | undocumented, unreproducible, and discovered missing during a rebuild |
| Terraform or [Crossplane](../../../../platform-engineering/iac/README.md) | correct, but a **second system** and a second lifecycle from the workload that uses it |
| A vendor CRD — Rook's `CephObjectStoreUser`, the MinIO operator's tenant resources | Kubernetes-native and completely **non-portable** |
| A `Secret` someone pasted in | the credential outlives the person, the bucket and the reason |

COSI's proposition is that requesting a bucket should look like requesting a volume: an application
team writes a claim, a class chosen by the platform team decides where and how it is satisfied, a
driver does the provider-specific work, and the credential arrives as a `Secret` the workload can
consume. Portable across MinIO, Ceph, S3 and the rest, in the way `PersistentVolumeClaim` is
portable across storage backends.

## The model

Five resources, deliberately mirroring CSI's split between what the user asks for and what the
administrator configures:

| Resource | Analogue in CSI | What it is |
|---|---|---|
| **`BucketClass`** | `StorageClass` | admin-defined: which driver, which parameters, delete or retain |
| **`BucketClaim`** | `PersistentVolumeClaim` | namespaced: *"I want a bucket"* — new, or bound to an existing one |
| **`Bucket`** | `PersistentVolume` | cluster-scoped: the actual bucket the driver provisioned |
| **`BucketAccessClass`** | — | admin-defined: the authentication type and policy for access grants |
| **`BucketAccess`** | — | namespaced: *"grant this service account access"* → produces a `Secret` |

Three components run it: a **central controller** reconciling the objects, a **sidecar** next to each
driver translating them into gRPC calls, and a **driver** per storage provider implementing that
gRPC interface. Exactly CSI's structure, which is the point — the design is a known-good one.

**The access half is the part with no CSI equivalent, and it is the more interesting half.**
Splitting `BucketAccess` from `BucketClaim` means the bucket and the credential have separate
lifecycles: several workloads can be granted distinct credentials to one bucket, and revoking one
does not touch the bucket or the others. That is the piece that is genuinely painful to build by
hand, and the reason a bucket-provisioning `Job` in Terraform is not the same thing.

## The thing to understand before adopting it

**COSI does not mount anything.** A `BucketAccess` produces a `Secret` containing bucket details and
credentials — endpoint, bucket name, region, keys — which the workload mounts or reads and then uses
**with an S3 client**. There is no filesystem, no device, no `volumeMounts` path that behaves like a
directory.

That is correct design and it is the sentence everyone skips. It is the same boundary
[`../README.md`](../README.md#it-is-not-a-filesystem) draws: object storage is an HTTP API, and
anything that presents a bucket as a POSIX mount is a convenience layer that will eventually
corrupt something. COSI standardises the **paperwork** — provisioning and credentials — and leaves
the data path exactly where it was.

The practical consequence: COSI only helps applications that already speak S3. Every consumer in the
table above does, which is why the fit is good in principle.

## When to use it

- you run **multiple object storage backends** — MinIO in the lab, Ceph on-premise, S3 in the cloud —
  and want one way for application teams to ask for a bucket
- you are building a **self-service platform** where "request a bucket" should be a manifest in the
  team's repository rather than a ticket
- **credential rotation and revocation per consumer** is a requirement rather than an aspiration
- you are already committed to the CSI mental model and want the same shape for buckets
- you want to **follow** the standard: watching the API and keeping bucket creation abstracted is
  cheap even if adoption comes later

## When not to use it

- **on anything you cannot afford to break.** The project describes itself as pre-alpha, the API is
  `v1alpha2`, and it has already been through more than one incompatible revision. This is the
  headline caveat and it dominates every other consideration
- when a **cloud provides the storage**. Provisioning an S3 bucket with
  [ACK](../../../../platform-engineering/iac/cloud/aws-controllers-for-kubernetes/README.md),
  [ASO](../../../../platform-engineering/iac/cloud/azure-service-operator/README.md) or Terraform is
  a solved problem with mature tooling. COSI's payoff is **portability across backends**, and if
  there is only one backend there is no payoff
- when your storage vendor's own CRDs already do this and you are not going to change vendor. Rook
  and MinIO both provision buckets and users declaratively today, and are production-grade in a way
  COSI is not
- **for the data path.** It is a provisioning API, not a mount, not a gateway, not a cache
- when the driver you need does not exist. The ecosystem is thin, and a standard with no driver for
  your backend is a design document

## Notes

**The honest status.** COSI has been "coming" since 2021 and is still alpha. That longevity is
itself informative: the reason is not that the design is wrong — it is close to a straight port of
CSI — but that the problem it solves is **less painful than the one CSI solved**. A volume must be
attached to a node by the kubelet, so it *had* to be a Kubernetes concern; a bucket is created by an
API call that Terraform, Crossplane or a vendor operator can already make. That difference is why
CSI became universal in three years and COSI has not in five, and it is the thing to weigh before
adopting it.

**Check the drivers before the API.** The list of implementations is short and its maturity is
uneven. Whether COSI is usable for you is decided entirely by whether a driver exists for the
backend you actually run — and that question is answered in the driver's repository, not in the
specification.

**Compare it against the alternative you already have.** For most platforms the realistic choice is
COSI versus *a bucket in Terraform plus an ExternalSecret*, and the second one works today, is
reviewable, and has no alpha CRDs in the cluster. COSI's advantage arrives when there are many
teams, several backends, and credential lifecycles that must be managed rather than issued once.

**Where this fits in pikakube.** Nothing here uses it, and the category assessment in
[`../README.md`](../README.md#the-honest-state-of-this-category) — *MinIO's open source has
effectively died and the alternatives are all weak* — is the reason COSI is worth recording anyway.
An abstraction over bucket provisioning is worth exactly as much as the ease of swapping the thing
underneath it, and this is a category where swapping is a live possibility rather than a
hypothetical. The cheap version of the idea is available now without any of the alpha risk: keep
bucket names, endpoints and credentials in configuration that consumers read, so the day
[MinIO](../minio/README.md) is replaced by [Garage](../garage/README.md), the change is one Secret
and one endpoint rather than an edit to Loki, Thanos, Tempo and Velero.

---

[← Object storage](../README.md)
