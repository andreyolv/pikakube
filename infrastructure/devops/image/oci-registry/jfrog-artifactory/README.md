[← OCI registry](../README.md)

# JFrog Artifactory

<https://github.com/jfrog/charts>

---

## The problem it solves

**One artefact manager for every package format an organisation uses** — Maven, npm, PyPI, NuGet,
Debian, RPM, Go modules, Helm and container images — behind one set of credentials, one permission
model and one retention configuration.

That is a genuinely different proposition from the rest of this folder. [zot](../zot/README.md)
and [Harbor](../harbor/README.md) are registries that happen to store OCI artefacts; Artifactory
is a **universal repository manager** whose OCI support is one adapter among many.

| Capability | Detail |
|---|---|
| Many package types | one server for Maven, npm, PyPI, Docker, Helm and the rest |
| **Remote repositories** | a caching proxy for any upstream — Maven Central, npm, Docker Hub |
| **Virtual repositories** | local and remote presented as one endpoint, resolved in a defined order |
| Permissions | fine-grained, per repository and per path |
| Replication | between instances, push or pull |
| Build integration | build info, and traceability from an artefact back to the build that produced it |
| Xray (separate product) | vulnerability and licence scanning across every format |

The **remote plus virtual repository** pattern is the reason organisations standardise on it: a
developer configures one npm registry URL, and it serves internal packages and proxies the public
one, with caching and policy applied in between. Nothing else in this folder does that for
non-container formats.

## When to use it

- **the organisation already runs it** — then using it as the OCI registry too is obviously right
- many package ecosystems need proxying and hosting, not only container images
- a single permission model and audit trail across every artefact type is a requirement
- build traceability from artefact back to build is needed for compliance

## When not to use it

- **as a new choice for a Kubernetes-only estate** — it is a large product for a job
  [zot](../zot/README.md) or [Harbor](../harbor/README.md) do more directly
- where OSS-edition limitations bite; see the note below
- where the operational weight is not wanted: it is a JVM application with a database and
  substantial memory requirements
- where the licence cost of the paid editions has not been budgeted, and the OSS edition does not
  cover the need

## Notes

Recorded link:

- <https://github.com/jfrog/charts> — JFrog's Helm chart repository. Only the charts repository was
  recorded, not a product repository, which is the correct pointer: Artifactory itself is not open
  source, and the charts are the open artefact.

**Edition matters, and it is the first thing to check.** What is deployed here is
`artifactory-oss` — the free, open-source edition — and the OSS edition's repository-type support
is **much narrower than the product's**. It covers generic, Maven and a limited set of formats;
**Docker/OCI registry support has historically been a Pro feature**, not an OSS one. Verify
against JFrog's current edition comparison before assuming this folder gives you a working
container registry, because if it does not, the whole reason it sits in
[`oci-registry/`](../README.md) does not apply.

That caveat is the single most important thing on this page: an Artifactory OSS deployment can be
running perfectly and still refuse to be a container registry.

What is configured here: a Flux `HelmRelease` deploying `artifactory-oss` at chart version
**107.98.10** from the `jfrog` chart repository, in its own namespace, with the values left as
comments pointing at the chart's `values.yaml`. The chart version scheme is JFrog's own —
`107.x.y` tracks the Artifactory `7.x` line — which is worth knowing because it looks like a
mistake and is not.

The other thing to size before deploying: Artifactory is a JVM application with a PostgreSQL
database (or a bundled Derby, which is only for evaluation) and meaningful memory requirements.
It is the heaviest option in this folder by some distance, [Harbor](../harbor/README.md) included.

## Where it fits here

Mapped as the enterprise universal-artefact option. For this repository it is the wrong shape:
the requirement is images and OCI Helm charts, which [zot](../zot/README.md) covers with one
binary and [Harbor](../harbor/README.md) covers with policy on top.

The case for Artifactory is organisational rather than technical — it wins where it is already
the standard and the OCI registry should not be a separate thing to operate.

---

[← OCI registry](../README.md)
