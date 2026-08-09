[← OCI registry](../README.md)

# docker-registry

<https://github.com/distribution/distribution>
<https://github.com/twuni/docker-registry.helm>

---

## The problem it solves

**The reference implementation of the registry API, and the minimum that works.** `distribution`
is the CNCF project that the original Docker Registry v2 became, and it is what most other
registries are built on or measured against.

What it is:

| Property | Detail |
|---|---|
| One binary | no database, no cache service, no UI |
| Implements the [distribution spec](https://github.com/opencontainers/distribution-spec) | push, pull, tags, manifests |
| Storage drivers | filesystem, S3, Azure, GCS, and others |
| **Pull-through cache mode** | proxy an upstream registry — a Docker Hub mirror in one setting |
| Authentication | htpasswd, token-based, or delegated to a proxy in front |
| Garbage collection | a command, run separately |

What it is not: there is no UI, no user management, no projects, no quotas, no retention policy,
no scanning, no replication. That is not a criticism — for a build cache endpoint or an internal
mirror it is exactly the right amount of software.

The **proxy mode** is the underrated feature. Configured as a pull-through cache in front of
Docker Hub and set as a mirror in the container runtime, it removes rate limits and most of the
egress problem described in [`../../cache/`](../../cache/README.md) with one deployment and no
manifest changes.

## When to use it

- as a **pull-through cache** in front of a public registry
- as a **build cache endpoint** for [Kaniko](../../builder-k8s/kaniko/README.md) or BuildKit, where
  the content is disposable and the features are irrelevant
- for local development and testing, where the whole registry is `docker run registry`
- inside a CI environment as a short-lived artefact store between pipeline stages
- when the requirement is genuinely "somewhere to put layers" and nothing more

## When not to use it

- as **the** platform registry: no RBAC, no retention, no immutability, no quotas — which means
  storage grows forever and tags can be silently repushed
- where OCI artefacts beyond images matter; its support for the referrers API and modern artefact
  types lags [zot](../zot/README.md)
- where a UI is expected — separate UI projects exist and are another thing to run
- where more than one team shares it and needs to be isolated from each other

## Notes

There is no `doc.md` for this folder; what follows is recorded from the manifests and from the
chart it uses.

- <https://github.com/distribution/distribution> — the upstream project, recorded in
  [`../../builder/docker/`](../../builder/docker/README.md) alongside the OCI specifications. It
  is a CNCF project, and it is the implementation the specification was written from.
- <https://github.com/twuni/docker-registry.helm> — the chart used here. Worth naming plainly:
  **there is no official Helm chart** for `distribution`. The `twuni` chart is the de facto
  community one, and it is a community-maintained chart rather than an upstream artefact — a small
  supply-chain consideration, and the reason to pin the version.

What is configured here: a Flux `HelmRelease` at chart version **2.2.3** from the `twuni` chart
repository, in its own namespace, with the values left as comments pointing at
[artifacthub](https://artifacthub.io/packages/helm/twuni/docker-registry) and the chart's
`values.yaml`.

Three things to decide before it is anything other than a test:

| Decision | Why |
|---|---|
| **Storage backend** | the default is a `PersistentVolume`, which pins the registry to one node and forbids replicas. S3-compatible object storage is what makes it scalable |
| **Garbage collection** | deleting a tag frees nothing; blobs are content-addressed and shared. GC must be run, and historically it wanted the registry read-only while it ran |
| **Authentication** | the default deployment is open. htpasswd is the minimum, and a proxy in front is the usual answer |

The garbage-collection point is the one that turns into an incident: without it, and without any
retention policy at all, a registry used as a build cache grows monotonically until the volume
fills — and the first symptom is builds failing to push, not a disk alert.

## Where it fits here

The smallest option in [`oci-registry/`](../README.md), and mapped as the baseline the others are
compared against.

For anything new, **[zot](../zot/README.md) is the better choice at the same footprint**: same
single binary, same lack of ceremony, and materially better OCI support — the referrers API in
particular, which is what signatures and SBOMs need. The case for `distribution` is when the
requirement really is a pull-through cache or a disposable build cache, where the ecosystem's most
boring, most deployed implementation is a feature in itself.

---

[← OCI registry](../README.md)
