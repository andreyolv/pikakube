[← MinIO](../README.md)

# MinIO Operator

<https://github.com/minio/operator>
<https://min.io/docs/minio/kubernetes/upstream/reference/operator-crd.html>
<https://github.com/minio/operator/tree/master/examples/kustomization>

Chart values: <https://github.com/minio/operator/blob/master/helm/operator/values.yaml>

The second of the two [MinIO](../README.md) deployment shapes. Its counterpart is
[`../minio/`](../minio/README.md), the standalone Helm deployment.

---

## The problem it solves

The [standalone chart](../minio/README.md) deploys MinIO. That is enough for one instance, and it
stops being enough as soon as there is more than one consumer.

The operator introduces the **`Tenant`** custom resource: a complete, isolated MinIO deployment
declared as a Kubernetes object, with its own capacity, credentials, erasure-coding layout and
lifecycle. One operator manages many tenants.

| Concern | Standalone chart | Operator + `Tenant` |
|---|---|---|
| Isolation | one deployment; separate by bucket and policy | **a separate deployment per tenant** |
| Erasure coding | configured by hand through chart values | declared as pools and `volumesPerServer` |
| Scaling | edit values, upgrade the release | **add a pool** to the `Tenant` |
| Certificates | bring your own | auto-generated, or cert-manager |
| Users, buckets, policies | applied afterwards with `mc` | **declared in the `Tenant` spec** |
| Identity for clients | access keys | **STS** — Kubernetes ServiceAccount tokens |
| Upgrades | a Helm upgrade | the operator performs a rolling update |

The isolation row is the argument. As
[`../README.md`](../README.md#why-it-is-load-bearing-here) records, object storage here is the
substrate under observability, backups and the lakehouse simultaneously. One tenant for
observability, one for backups and one for the lake means those three do not share a failure
domain, a capacity budget or a credential — which is exactly what "one bucket namespace shared by
everything" fails to give you.

### Pools are the concept to understand

A `Tenant` contains **pools**, and a pool is a set of servers with a fixed number of volumes each.
That is where erasure coding lives:

| Field | Meaning |
|---|---|
| `servers` | how many MinIO pods in this pool |
| `volumesPerServer` | how many PVCs each pod gets |
| `volumeClaimTemplate` | the size and StorageClass of each of those PVCs |

`servers × volumesPerServer` is the erasure set size, and it determines how many drives can be
lost before data is. **This cannot be changed for an existing pool.** Growing a tenant means
adding a *new* pool, and MinIO then writes new objects across both — it does not rebalance the
old pool into the new shape.

That makes the initial pool geometry one of the decisions in the same class as
`storageClassName` and `accessModes` in [storage §3](../../../README.md#3-the-immutable-fields-that-trap-you):
cheap to get right at the start, expensive afterwards.

Note also that every volume is an ordinary `ReadWriteOnce` PVC from a StorageClass you choose. All
of [block-storage](../../../block-storage/README.md) applies underneath — including
`reclaimPolicy`, which on a MinIO tenant's StorageClass decides whether deleting the tenant
destroys the data.

### STS: credentials without credentials

The operator's most interesting feature, and the one worth adopting deliberately.

Instead of giving an application an access key and secret in a Secret, MinIO's **Security Token
Service** exchanges a Kubernetes **ServiceAccount token** for temporary S3 credentials. A
`PolicyBinding` says which ServiceAccount in which namespace may assume which policy.

```
ServiceAccount token  →  STS endpoint  →  temporary access key + secret + session token
        ↑                                            ↓
   projected into the pod                     scoped by PolicyBinding
```

Why this matters: a static access key is a long-lived credential that must be created,
distributed, rotated and eventually found in a Git history. An STS credential is minted per
workload, expires, and its authority is a Kubernetes object that can be reviewed. It is the same
idea as IRSA on [AWS](../../../cloud/aws/README.md) or Workload Identity on
[Azure](../../../cloud/azure/README.md), implemented against a self-hosted object store — which
is a genuinely good thing to have on-premise, where those provider mechanisms do not exist.

## When to use it

- **More than one consumer of object storage**, which in this repository is immediately the case:
  [Loki](../../../../../observability/logs/storage/loki/README.md),
  [Thanos](../../../../../observability/metrics/long-term-storage/thanos/README.md),
  [Velero](../../../../backup/velero/README.md) and the lakehouse should not share a tenant.
- **When erasure coding and durability matter.** The `Tenant` spec is where that is expressed
  properly; the standalone chart makes it awkward.
- **When storage should be self-service.** A `Tenant` is a resource a team can be given the right
  to create, with quotas, rather than a ticket.
- **When STS is wanted** instead of distributing static access keys — the strongest reason to
  choose the operator over the chart.
- **For anything that will grow.** Adding a pool is a supported operation; reshaping a standalone
  deployment is not.

## When not to use it

- **In a cloud.** S3, Blob Storage and GCS exist. Nothing in this folder beats a managed object
  store on a managed cluster — see [cloud/](../../../cloud/README.md).
- **For a single small instance.** One MinIO for local development is what
  [`../minio/`](../minio/README.md) is for; the operator adds CRDs, a controller and a concept to
  learn for no benefit at that size.
- **On a single node, expecting durability.** Erasure coding across four servers scheduled onto
  one machine is four copies on one disk. The API works and the guarantee does not — the same
  caveat as [Rook](../../../multi-storage/rook/README.md).
- **Without reading the licence position first.** Everything in
  [`../README.md`](../README.md#the-licence-situation) applies to the operator too: AGPLv3, and a
  trajectory of capabilities moving to the commercial offering. The operator is not exempt; see
  the Notes.
- **Where a Flux prune could reach the `Tenant`.** A `Tenant` is data. Deleting it with a
  `Delete` reclaim policy on its StorageClass is a data-loss event, not a rollback.

## Notes

The recorded notes for this folder, preserved and explained.

**<https://github.com/minio/operator>** — the operator itself. Two things to know before relying
on it:

- It is **AGPLv3**, like MinIO. The licence discussion in
  [`../README.md`](../README.md#the-licence-situation) applies unchanged.
- MinIO **reduced and then removed the bundled Operator Console** across the v5 and v6 operator
  lines, which is part of the same feature-reduction trajectory that made the whole category
  uncomfortable. Check what the version you deploy actually includes rather than assuming a UI
  exists — this repository pins operator chart **`6.0.4`**, on the far side of that change.

**The recorded command:**

```
k get secret console-sa-secret -o jsonpath="{.data['token']}" | base64 --decode
```

This retrieves the **JWT used to log in to the MinIO Operator Console**. Unpacked:

| Part | What it does |
|---|---|
| `console-sa-secret` | a Secret of type `kubernetes.io/service-account-token`, holding a token for the console's ServiceAccount |
| `jsonpath="{.data['token']}"` | extracts the `token` key — bracket syntax, which is the form that survives keys containing dots |
| `base64 --decode` | Secret values are base64-encoded; this yields the raw JWT |

The Operator Console does not use a username and password. It authenticates with a ServiceAccount
token, and the authority you get is the RBAC that ServiceAccount holds — which for the operator's
own service account is substantial. Two practical consequences: add `-n minio-operator` (or
whichever namespace the operator lives in) or the command silently looks in the wrong namespace,
and treat the output as a **cluster credential**, not a UI password.

Given the console removal noted above, verify that `console-sa-secret` exists at all in the
version you run. The command is preserved here because it is the answer to "how do I log in",
and because the pattern — extract a ServiceAccount token from a Secret and decode it — is worth
knowing independently of MinIO.

**<https://github.com/minio/operator/tree/master/examples/kustomization>** — the upstream example
set, referenced from the `Tenant` manifest here and the best source for current CRD shapes. As
with [Rook](../../../multi-storage/rook/README.md), read the examples for the operator version
you actually run; CRD fields change across releases.

**How it is deployed here.** A Flux `HelmRelease` named `minio-operator` in the `minio-operator`
namespace, pinned to chart version `6.0.4`, from the `minio` `HelmRepository`, with an empty
values block. The operator chart's defaults are reasonable — as with
[Rook's operator chart](../../../multi-storage/rook/rook-ceph/README.md), the decisions live in
the resources it manages rather than in the controller.

**What the `tenant/` folder contains**, and it is the more interesting half:

| Piece | What it demonstrates |
|---|---|
| `tenant.yaml` | a `Tenant` named `sandbox` in `minio-tenant`: one pool, 4 servers, 2 volumes each, 1Gi per volume, `bucketDNS`, a declared user and two buckets with `objectLock: true` |
| `secrets/` | `storage-configuration` (the `config.env` holding root credentials and `MINIO_STORAGE_CLASS_STANDARD`) and `storage-user` |
| `sts/` | a `PolicyBinding` granting the `mc-job-sa` ServiceAccount the `consoleAdmin` policy, plus a Job running `mc` that authenticates through STS |
| `sts-app/` | an application-side example — a Job in a separate namespace using `AWS_WEB_IDENTITY_TOKEN_FILE` against the STS endpoint, with a scoped policy from a ConfigMap |

Several things in there are worth extracting:

- **`servers: 4`, `volumesPerServer: 2`** is an eight-drive erasure set, which is a realistic
  minimum shape. On a single Kind node it is eight PVCs on one disk.
- **`MINIO_STORAGE_CLASS_STANDARD="EC:2"`** sets the erasure-coding parity — two parity blocks,
  so two drives may be lost. This is the durability dial, and it is set in `config.env` rather
  than in the `Tenant` spec, which is easy to miss.
- **`objectLock: true`** on both buckets enables WORM retention. That is the property that makes
  a bucket useful as a ransomware-resistant backup target, and it must be set **at bucket
  creation** — it cannot be added later.
- **The credentials in these manifests are examples** (`minio`/`minio123`,
  `console`/`console123`) and are plainly not for use. Real tenant credentials belong in an
  encrypted-secrets flow, not in `stringData` in Git.
- **The two STS examples differ usefully.** `sts/` shows the administrative path — `mc`
  authenticating as a ServiceAccount with `consoleAdmin` — while `sts-app/` shows the intended
  application path: a workload with a projected ServiceAccount token, a narrowly scoped policy,
  and the tenant's CA mounted for TLS verification. The second is the pattern to copy.

**The honest caveat that closes every file in this folder:** as
[`../README.md`](../README.md#the-uncomfortable-conclusion) and
[`../../README.md`](../../README.md#the-honest-state-of-this-category) both record, MinIO's open
position has deteriorated and the alternatives — [Garage](../../garage/README.md),
[SeaweedFS](../../seaweedfs/README.md), [RustFS](../../rustfs/README.md) — are weak. The operator
is the best available way to run MinIO properly on Kubernetes, and that assessment sits inside a
category whose direction is the actual problem.

---

[← MinIO](../README.md)
