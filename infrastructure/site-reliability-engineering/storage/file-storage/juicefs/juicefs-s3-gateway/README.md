[← JuiceFS](../README.md)

# JuiceFS S3 gateway

<https://github.com/juicedata/juicefs>
<https://juicefs.com/docs/community/s3_gateway>

Chart values: <https://github.com/juicedata/charts/blob/main/charts/juicefs-s3-gateway/values.yaml>

The HTTP-facing shape of [JuiceFS](../README.md). Its counterpart is
[`../juicefs-csi-driver/`](../juicefs-csi-driver/README.md).

---

## The problem it solves

A JuiceFS filesystem is reached by mounting it. That needs FUSE, mount privileges, the client
installed, and — in Kubernetes — [the CSI driver](../juicefs-csi-driver/README.md) with its mount
pods on every node that uses it.

Sometimes none of that is possible or wanted:

- The consumer is **outside the cluster** — a laptop, a CI runner, another cluster, a partner.
- The consumer is a **Windows or macOS machine** where the JuiceFS client is inconvenient.
- The consumer **already speaks S3** and gains nothing from a mount.
- The environment **forbids privileged pods**, so FUSE is not available.
- You want a browsable UI over the data without giving anyone a mount.

The S3 gateway answers all of these. It is an ordinary Deployment that speaks the **S3 API** and
serves the same JuiceFS filesystem behind it.

### The loop, which is worth noticing

JuiceFS turns object storage into a filesystem. The S3 gateway turns that filesystem back into an
S3 API.

That sounds circular, and it is not, because what comes out the far side is different from what
went in:

| | The underlying bucket | The gateway's S3 API |
|---|---|---|
| Contents | chunks named by hash | **real files, with real names and directories** |
| Readable without JuiceFS | yes, and meaningless | yes, and meaningful |
| Written by | the JuiceFS client | any S3 client |
| Shared with | nothing else | mounted pods, via the CSI driver, simultaneously |

The gateway exposes the *logical* filesystem — the tree that only the metadata engine knows
about. A pod with a PVC and a script using `aws s3 cp` against the gateway see the same files, by
the same names, at the same time. That is the actual point.

The consequence is one dataset with two access paths, which is a genuinely useful shape: a
training job mounts the data as a filesystem while an upload service writes to it over S3, with
no copy between them.

## What this shape adds over the simpler one

| | [CSI driver](../juicefs-csi-driver/README.md) | S3 gateway (here) |
|---|---|---|
| Interface | a mounted directory, as a PVC | an HTTP S3 endpoint |
| Kubernetes objects | controller, node DaemonSet, mount pods | **one Deployment and a Service** |
| Privileges | FUSE mounts on the node | **none** |
| Reachable from outside the cluster | no | yes, with an Ingress |
| POSIX semantics | yes, including locking | **no** — object semantics again |
| Per-node cache | yes, and it is where performance comes from | shared, at the gateway |

The gateway is the simpler deployment by a wide margin: no privileges, no DaemonSet, no
per-node state, and it scales by replica count like any stateless service.

What it gives up is POSIX. Through the gateway, this is object storage: no partial writes, no
locking, no rename semantics beyond copy-and-delete. Applications needing those must use the CSI
driver.

Running both at once is the normal configuration, not an either/or.

## When to use it

- **Consumers outside the cluster**, or on platforms where mounting is impractical.
- **Applications that already speak S3** and would gain nothing from a filesystem.
- **Environments where privileged pods are not allowed** and FUSE is therefore unavailable.
- **Alongside the CSI driver**, giving one dataset a file interface and an object interface at
  once.
- **As a migration path**: expose an existing JuiceFS filesystem over S3 so applications can be
  moved off mounts incrementally.
- To hand out **scoped credentials** for a subtree, without giving anyone a mount of the whole
  filesystem.

## When not to use it

- **As a general-purpose object store.** If applications want S3 and there is no filesystem
  requirement, use [MinIO](../../../object-storage/minio/README.md), Garage, or the cloud
  provider's service directly. Adding a filesystem in the middle purely to expose S3 at the other
  end is two systems where one would do, and it puts the metadata engine on the critical path of
  something that never needed it.
- **For high-throughput object workloads.** Every request goes through one gateway process to a
  metadata database and then to the real bucket. It is a proxy, and it scales like one.
- **Expecting POSIX guarantees.** Locking and atomic rename do not exist over this interface.
- **As the backing store for observability or backup tooling.**
  [Loki](../../../../../observability/logs/storage/loki/README.md),
  [Thanos](../../../../../observability/metrics/long-term-storage/thanos/README.md) and
  [Velero](../../../../backup/velero/README.md) should point at the real object store, not at a
  gateway in front of a filesystem in front of the same object store. Every added layer is
  another thing that must be up during an incident.
- **Without the metadata engine being highly available.** The gateway inherits the dependency in
  full — see
  [the parent README](../README.md#the-metadata-engine-is-a-hard-dependency-and-a-single-point-of-failure).
- **Exposed publicly without thought.** It is an S3 endpoint to the whole filesystem; it needs
  TLS, credentials and, realistically, an Ingress with authentication in front.

## Notes

**How it is deployed here.** A Flux `HelmRelease` named `juicefs-s3-gateway` in the `juicefs`
namespace, pinned to chart version `0.11.3`, from the same `juicefs` `HelmRepository`
([`juicedata/charts`](https://github.com/juicedata/charts)) that provides the CSI driver. The
values block is empty, with the upstream values file referenced in a comment.

**An empty values block means it is not configured yet**, and for this chart the required values
are the same two that the CSI driver leaves as placeholders: the **metadata URL** and the
**object-storage backend**. The gateway is a JuiceFS client like any other and must be told which
filesystem to serve. Deployed with defaults, it has nothing to serve.

**The gateway needs its own credentials**, separate from the underlying bucket's. It authenticates
S3 clients with an access key and secret of its own, and it separately holds the credentials for
the real object store and the metadata engine. Three sets of secrets in one Deployment is worth
noting for anyone reviewing it: none of them should be inline in `HelmRelease` values.

**It is not the same as MinIO's gateway mode.** MinIO historically had a gateway that fronted
other object stores, and it was removed. This is a different thing — a JuiceFS client that
happens to speak S3 — and it is a supported part of the Community Edition, not a deprecated
compatibility layer. Given the edition confusion recorded in
[the parent Notes](../README.md#notes), it is worth stating that the S3 gateway is in the
community build.

**Sharing with the CSI driver.** Both shapes in this folder point at the same filesystem when
given the same `metaurl` and bucket, which is the intended arrangement. What they do not share is
cache: the CSI driver caches on each node, the gateway caches at the gateway. A file written
through one appears through the other, subject to those caches, and JuiceFS's consistency model
is worth reading before designing a workflow that depends on immediate cross-path visibility.

**Scaling.** More replicas of the gateway is fine — it holds no local state beyond cache — and it
is the correct way to add throughput. What does not scale by adding gateway replicas is the
metadata engine, which every replica hits, and which remains the bottleneck and the single point
of failure for everything JuiceFS does.

---

[← JuiceFS](../README.md)
