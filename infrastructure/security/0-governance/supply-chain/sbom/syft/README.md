[← SBOM](../README.md)

# Syft

<https://github.com/anchore/syft>
<https://github.com/anchore/sbom-action>

---

## The problem it solves

You have a container image and no reliable answer to "what is inside it". The Dockerfile
tells you what was asked for; the lockfile covers one language ecosystem; neither accounts for
the base image, the packages a `RUN apt-get install` pulled in, or the JAR copied out of a
builder stage.

Syft opens the built artefact and enumerates what it finds — OS packages (apk, deb, rpm),
language packages (Python, JavaScript, Go, Java, Ruby, Rust, PHP, .NET and more), and binaries
it can fingerprint — and writes the result as CycloneDX or SPDX. It works against images,
directories, archives and filesystems, so the same tool covers a container, a source tree and
a release tarball.

It is Anchore's, sits next to Grype (the scanner, in `3-container/scan/`), and the pairing is
the point: syft produces the inventory once, and any number of consumers evaluate it. Grype
will happily consume a syft SBOM instead of rescanning the image, which is the same inversion
that makes [aggregation](../../aggregation/README.md) work.

`sbom-action` is the GitHub Action wrapper. It runs syft, and can attach the result to a
release or upload it as an artefact — the CI-shaped path to the same output.

## When to use it

- generating an SBOM for a **built container image**, which is the default case
- feeding [Dependency-Track](../../aggregation/dependency-track/README.md) — emit CycloneDX
  JSON and upload it, keyed to the image digest
- you need both CycloneDX and SPDX from one scan; syft emits either from the same catalogue
- inventorying a **directory or filesystem** rather than an image — release tarballs, a
  checked-out repository, a VM image
- pairing with Grype so the scan reads an inventory instead of re-cataloguing the image every
  time
- as a build attestation: syft output attached to the image in the registry, so the inventory
  travels with the artefact

## When not to use it

- **as a vulnerability scanner** — it is not one. It produces an inventory; Grype, Trivy or
  Dependency-Track do the matching. Confusing the two is the most common misuse
- when the build system already emits an SBOM attestation natively (BuildKit `--attest
  type=sbom`) — that path stores the SBOM beside the image in the registry, which is one fewer
  moving part than generating it separately and shipping it somewhere
- as the sole basis for licence compliance — syft reports declared licence metadata, which is
  frequently missing or wrong. Deep licence work needs [ORT](../../license/ort/README.md) or
  [FOSSA](../../license/fossa/README.md), which look at file-level evidence
- expecting complete identification of **statically linked binaries** — Go and Rust binaries,
  shaded JARs and vendored C libraries are the known weak spot for every tool in this class,
  syft included. Coverage is good; it is not total
- scanning a running container to catch drift — possible, but that is a runtime-security
  question and belongs in `2-cluster/runtime-security/`

## Notes

Original references recorded for this tool:

> <https://github.com/anchore/syft>
> <https://github.com/anchore/sbom-action>

The first is the CLI, the second is the GitHub Action. Worth knowing the distinction because
they fail differently: the CLI is a single binary you can run anywhere, including locally
against an image you just built, while `sbom-action` is convenient in a workflow and pins you
to whatever syft version it bundles. For a GitOps repository the CLI in an explicit step, with
the version pinned, is usually the more predictable choice — and it makes the same command
reproducible on a laptop when someone needs to answer a question quickly.

Two practical points that are not in the notes but decide whether this is useful:

**Key the output by digest, not by tag.** An SBOM describing `myapp:latest` describes whatever
`latest` pointed at when the scan ran, which is not a durable statement. Everything downstream
— aggregation, admission, incident response — joins on the digest.

**Scan the final image, not a builder stage.** A multi-stage build exists precisely so the
build tooling does not ship; an SBOM taken from the wrong stage reports a much larger and
entirely fictional attack surface.

---

[← SBOM](../README.md)
