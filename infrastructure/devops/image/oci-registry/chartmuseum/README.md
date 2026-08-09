[← OCI registry](../README.md)

# ChartMuseum

<https://github.com/helm/chartmuseum>

---

## The problem it solves

**A server for the classic Helm chart repository format.** A chart repository is nothing more than
an `index.yaml` listing every chart version, plus the packaged `.tgz` files. ChartMuseum serves
that, and adds an upload API so charts can be pushed rather than committed to a static site.

| Capability | Detail |
|---|---|
| Serves `index.yaml` and chart tarballs | the format `helm repo add` expects |
| **Upload API** | `POST /api/charts` — push from CI instead of regenerating a static site |
| Storage backends | local filesystem, S3, GCS, Azure, and others |
| Multi-tenancy | multiple repositories under one server, via a depth setting |
| Basic auth | username and password, or delegated to a proxy |
| In Flux | consumed as a `HelmRepository` |

The alternative it replaces is a static site: `helm package`, `helm repo index`, and commit the
result to GitHub Pages or an S3 bucket. That works and is very common; ChartMuseum's advantage is
the upload API and the fact that the index is maintained server-side.

## When to use it

- **hosting internal charts when an OCI registry is not available or not wanted**
- where existing tooling consumes chart repositories and cannot be moved to OCI
- where a chart repository should be writable by CI without a Git commit
- as a migration staging post — serve both formats while consumers move across

## When not to use it

- **for anything new** — OCI is where Helm has gone; see below
- where a registry is already deployed, because it can host charts already: one system, one
  authentication mechanism, one retention policy
- at scale with many chart versions: `index.yaml` contains **every version of every chart** and is
  downloaded whole by every client, so it grows into a real cost
- where signing and provenance matter; Cosign over OCI artefacts is far better supported than Helm
  provenance files ever were

## Notes

Recorded link:

- <https://github.com/helm/chartmuseum> — the project, under the `helm` organisation. That
  affiliation is the reason it is worth documenting rather than dismissing: it is the Helm
  project's own chart-repository server, not a third-party alternative.

**Status: this is the previous generation.** Helm 3 supports OCI registries natively — a chart is
pushed with `helm push chart.tgz oci://registry/charts` and pulled from the same registry as the
images. Flux followed with `OCIRepository` alongside `HelmRepository`. The direction of travel is
one artefact store for everything, and that is the migration described in
[§3 of the parent](../README.md#3-helm-from-helmrepository-to-ocirepository).

The comparison, plainly:

| | **ChartMuseum** | **OCI registry** |
|---|---|---|
| Format | `index.yaml` plus tarballs | charts as OCI artefacts |
| Index cost | the whole index downloaded and parsed by every client | pull the tag you want |
| Authentication | its own, or a proxy in front | the registry's, shared with images |
| Signing | Helm provenance files, rarely used in practice | Cosign, the same as for images |
| Retention | whatever you script | the registry's policy |
| Another service to run | **yes** | no — it is the registry you already have |
| In Flux | `HelmRepository` | **`OCIRepository`** |

That said, **classic chart repositories are not going away soon**. A large share of upstream charts
are still published that way, and several `HelmRelease`s in this repository consume them —
including [Harbor's own chart](../harbor/README.md), which is
[not distributed as OCI](https://github.com/goharbor/harbor-helm/issues/2265). Understanding the
format is not optional even while moving away from hosting it.

Nothing is deployed here — the folder is a reference with no manifests.

## Where it fits here

The odd one out in [`oci-registry/`](../README.md): it is not an image registry at all, and it is
in this folder because it answers the same question — *where do the artefacts live* — for the
generation of tooling that preceded OCI.

For this repository the answer is the registry, not ChartMuseum. It is documented so that the
distinction between `HelmRepository` and `OCIRepository` is an understood choice rather than a
piece of Flux syntax, because that distinction is what the migration is actually about.

---

[← OCI registry](../README.md)
