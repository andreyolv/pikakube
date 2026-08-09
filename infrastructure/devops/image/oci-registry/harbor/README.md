[← OCI registry](../README.md)

# Harbor

<https://github.com/goharbor/harbor>
<https://github.com/goharbor/harbor-helm>

---

## The problem it solves

**A registry with the things a registry alone does not have**: projects, users, policy and
replication. Harbor is a CNCF graduated project and the default answer when the requirement is a
registry *platform* rather than a place to put blobs.

| Capability | Why it matters |
|---|---|
| **Projects** | a namespace with its own members, roles, quota and policies — the unit of multi-tenancy |
| **RBAC** | project admin, developer, guest; plus robot accounts for CI |
| **Replication** | pull or push between Harbor instances and external registries, on a schedule or on push |
| **Tag retention** | keep the last N, keep by pattern, keep what is deployed — see [§5 of the parent](../README.md#5-storage-garbage-collection-and-retention) |
| **Immutability rules** | forbid repushing a tag; the enforcement behind [§5 of `image/`](../../README.md#5-tags-lie-digests-do-not) |
| **Vulnerability scanning** | Trivy built in, scan on push, block pulls above a severity |
| **Signing** | Cosign and Notation integration, with a policy to require it |
| Proxy cache | a project can be a pull-through cache for an upstream registry |
| Quotas | per-project storage limits, so one team cannot fill the disk |
| Webhooks | notify on push, scan completion, or policy violation |

Two of these deserve emphasis because nothing else in this folder provides them. **Replication**
is how images are promoted between environments — build once in a development registry, replicate
the exact digest to production — without rebuilding and without trusting a tag. And the
**proxy cache project** removes the Docker Hub dependency described in
[`../../cache/`](../../cache/README.md) with no extra component at all.

The cost is the architecture: core, jobservice, portal, registry, registryctl, Redis and
PostgreSQL. That is a real deployment, not a pod.

## When to use it

- **several teams share one registry** and need separate access control and quotas
- promotion between environments should be replication of a digest, not a rebuild
- **retention and immutability policies are needed** — the two things that keep storage bounded and
  tags meaningful
- scanning at push and a policy that blocks vulnerable images from being pulled
- a web UI is genuinely wanted, for browsing, permissions and audit

## When not to use it

- when the requirement is "a registry" — [zot](../zot/README.md) is a fraction of the footprint
  and speaks the same protocol
- on a small or single-node cluster: seven components and a database is a lot of moving parts to
  own
- as a build cache endpoint only — [docker-registry](../docker-registry/README.md) is enough
- where a managed registry already exists — ECR, GAR, ACR do most of this and you operate none of it
- if PostgreSQL and Redis are not things this platform wants to run and back up

## Notes

Recorded links:

- <https://github.com/goharbor/harbor> — the project.
- <https://github.com/goharbor/harbor-helm> — the official Helm chart, which is what is used here.

**Recorded finding — the chart is not distributed as OCI:**

> not support oci helm —
> [goharbor/harbor-helm#2265](https://github.com/goharbor/harbor-helm/issues/2265)

The note is terse, so here is the precise reading. It is filed against **harbor-helm**, the chart
repository, not against Harbor itself. Harbor the registry stores OCI Helm charts perfectly well —
it dropped its old ChartMuseum-backed chart repository in favour of OCI artefacts. What is missing
is the other direction: **Harbor's own chart is published as a classic HTTP chart repository**, so
it must be consumed as a Flux `HelmRepository` and cannot be consumed as an `OCIRepository`.

The irony is worth stating: in a repository migrating from `HelmRepository` to `OCIRepository`
([§3 of the parent](../README.md#3-helm-from-helmrepository-to-ocirepository)), the registry that
would host those OCI charts is itself one of the releases that has to keep using the old
mechanism. It is a small operational wart rather than a blocker — but it is the kind of detail
that turns "we have converted everything" into "everything except one".

**Recorded credentials and frustration:**

> User: `admin`
> Password: `Harbor12345`
>
> sometimes this damn login just does not work

`admin` / `Harbor12345` is the chart's default administrator credential — public knowledge, and to
be changed before anything is exposed beyond a `port-forward`.

The login failing intermittently is a real and well-known symptom, and it usually is not the
password. Harbor's **portal answers before its core is ready**: the Ingress routes to the portal
as soon as its pod is up, but authentication is handled by `harbor-core`, which waits for
PostgreSQL and runs database migrations first. Log in during that window and you get an
authentication error rather than a "still starting" message. The other common cause is a mismatch
between `externalURL` and the address actually used in the browser, which breaks the OIDC/session
redirect — and the configuration here has `externalURL: http://harbor.127.0.0.1.nip.io` while the
Ingress carries a TLS secret, so `http` versus `https` is exactly the kind of mismatch that
produces it. The fix in both cases is to wait for `harbor-core` to be `Ready` and to make sure the
URL matches, not to keep retrying the password.

**What is configured here:** a Flux `HelmRelease` at chart version **1.19.1**, exposed through
Ingress at `harbor.127.0.0.1.nip.io` with an mkcert TLS secret (`mkcert-tls-secret`), plus
Forecastle annotations so it appears on the dashboard under the "DevOps" group with the CNCF
Harbor icon. The `nip.io` hostname is the standard local-cluster trick — it resolves any
`*.127.0.0.1.nip.io` name to `127.0.0.1`, so Ingress works locally without editing `/etc/hosts`.

## Where it fits here

The heavyweight option in [`oci-registry/`](../README.md), and the only one that answers the
multi-tenancy, retention, replication and scanning questions properly. The lighter alternatives are
[zot](../zot/README.md) — modern, OCI-native, one binary — and
[docker-registry](../docker-registry/README.md).

The honest position for this cluster: Harbor is more than is needed to store images, and its
retention and immutability policies are exactly what
[§5 of the parent](../README.md#5-storage-garbage-collection-and-retention) says every registry
needs. If it is deployed, use object storage rather than a `PersistentVolume`, because with charts
moving to OCI the registry stops being something you can afford to run on one node.

---

[← OCI registry](../README.md)
