[← OCI registry](../README.md)

# zot

<https://github.com/project-zot/zot>
<https://github.com/project-zot/helm-charts>

---

## The problem it solves

**A registry that implements the OCI specification and nothing else.** zot is a single Go binary
with no database, no queue and no supporting services, and it is **OCI-native by design** rather
than by extension — it does not carry the Docker Registry v2 legacy that older implementations
were built around.

| Property | Detail |
|---|---|
| **Zero dependencies** | one binary, one configuration file; no PostgreSQL, no Redis |
| **OCI-conformant** | passes the distribution-spec conformance suite |
| **Referrers API** | signatures, SBOMs and attestations attach properly — the thing older registries reject |
| Storage | filesystem, or S3-compatible object storage |
| Deduplication | across repositories, with optional hard links on filesystem storage |
| Optional extensions | search, a web UI, scanning via Trivy, sync from upstream registries, metrics |
| **Sync** | mirror or pull-through cache from another registry, on a schedule or on demand |
| Authentication | htpasswd, LDAP, OIDC, mTLS; per-repository access policies |
| Footprint | small enough to run on an edge device |

The extensions are compile-time and configuration-time options, which is the part that makes zot
interesting: the minimal build really is minimal, and the features are added when wanted rather
than paid for always.

## When to use it

- **the default choice when the requirement is "a registry"** — modern, small, conformant
- as a **build cache endpoint** for [Kaniko](../../builder-k8s/kaniko/README.md) or BuildKit, where
  a full platform is pure overhead
- for **OCI Helm charts** — the target of
  [§3 of the parent](../README.md#3-helm-from-helmrepository-to-ocirepository) — where the
  referrers API and modern spec support matter
- where signatures and SBOMs must be stored alongside images and actually work
- as a pull-through cache or mirror, using its sync feature
- on small, edge or air-gapped clusters where Harbor is not proportionate

## When not to use it

- where **multi-tenancy with projects, quotas and a full RBAC model** is the requirement —
  [Harbor](../harbor/README.md)
- where a rich web UI, replication policies and scan-and-block gates are expected out of the box
- where the organisation has standardised on an enterprise product and that is not negotiable
- if the surrounding tooling assumes Docker Registry v2 quirks that zot deliberately does not
  reproduce — rare, and worth testing rather than assuming

## Notes

Recorded links:

- <https://github.com/project-zot/zot> — the registry. Apache 2.0, and a Linux Foundation project.
- <https://github.com/project-zot/helm-charts> — the official chart repository, which is the
  source used here.

Recorded command:

```bash
k port-forward svc/zot 5000
```

Port 5000 is the registry API port and the same one the reference implementation uses, so a
`port-forward` makes `localhost:5000` behave as an ordinary registry —
`docker push localhost:5000/name:tag`, `helm push chart.tgz oci://localhost:5000/charts`,
`skopeo copy` against it. That is the whole smoke test, and it is the fastest way to verify that a
registry works before wiring anything to it. (`k` is the usual `kubectl` alias.)

One thing to know when pushing to it over plain HTTP: container runtimes reject non-TLS registries
unless they are configured as insecure. Through a `port-forward` to `localhost` most runtimes make
an exception; over an Ingress they will not, and TLS becomes a prerequisite rather than a nicety.

What is configured here: a Flux `HelmRelease` at chart version **0.1.65**, in its own namespace,
with the values left as comments pointing at the chart's `values.yaml`.

**The two things to configure before it is more than an experiment**, both from
[§5 of the parent](../README.md#5-storage-garbage-collection-and-retention): S3-compatible object
storage instead of a `PersistentVolume`, so the registry is not pinned to one node and can have
replicas; and a retention policy, because zot's default is to keep everything and the build cache
repository grows fastest of all.

## Where it fits here

**The best default of the small registries in [`oci-registry/`](../README.md).** Compared with
[docker-registry](../docker-registry/README.md) it has the same footprint and materially better
spec support — the referrers API in particular, without which Cosign signatures and SBOMs do not
work properly. Compared with [Harbor](../harbor/README.md) it gives up projects, quotas,
replication policies and scan gates, and gives back six components and a database.

For this repository, with charts moving from `HelmRepository` to `OCIRepository`, zot is the
proportionate answer: it is the artefact store, and it does not become a platform of its own.

---

[← OCI registry](../README.md)
