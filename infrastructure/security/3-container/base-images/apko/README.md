[← Base images](../README.md)

# apko

<https://github.com/chainguard-dev/apko>

---

## The problem it solves

A Dockerfile is a **script**. `RUN` executes arbitrary commands against the network at build
time, which produces three problems that no amount of care fully removes:

- **Builds are not reproducible.** The same Dockerfile built twice gives different bytes,
  because `apt-get update` resolved different versions, a mirror changed, or a timestamp got
  baked in.
- **The SBOM is a reconstruction.** Because nobody recorded what went in, tools have to inspect
  the finished image and *guess* the package inventory afterwards.
- **The image accumulates build-time state** — caches, compilers, temporary files — unless
  someone remembers to clean up in the same layer.

apko takes the opposite approach: an image is **declared**, not built. You write YAML listing
the apk packages, the entrypoint, the user and the architectures; apko resolves the packages
and writes the OCI image directly. There is no `RUN`, no shell, and no build container.

What that buys:

| Property | Why it follows |
|---|---|
| **Reproducible, bit-for-bit** | no arbitrary commands, and timestamps are set deterministically |
| **Accurate SBOM, generated at build time** | apko knows exactly which packages it installed — nothing is inferred |
| **Multi-architecture natively** | it assembles per-architecture images from packages, without QEMU emulation |
| **Minimal by construction** | there is no build-time cruft to clean up, because none was created |
| **Fast** | assembling packages is quicker than executing a build script |

apko is one third of Chainguard's stack: [`melange`](../melange/README.md) builds the packages,
[`wolfi`](../wolfi/README.md) is the repository of them, apko assembles them into an image.

## When to use it

- **You want a genuinely accurate SBOM.** This is the strongest reason. An SBOM produced by
  scanning a finished image is a best-effort inventory; an SBOM produced by the thing that
  installed the packages is a record. That difference matters for anything downstream in
  `0-governance/supply-chain/`
- **Reproducible builds are a requirement** — regulatory, or because you want to be able to
  prove a published image corresponds to a commit
- **Publishing base images for other teams.** apko's sweet spot is producing the small,
  standardised bases that application Dockerfiles then build on
- **Multi-arch without emulation.** If cross-building under QEMU is currently slow and flaky,
  apko sidesteps it entirely
- **Combined with [`melange`](../melange/README.md)** when your own application is packaged as
  an apk — then the whole chain from source to image is declarative

## When not to use it

- **Your build genuinely needs imperative steps.** apko has no `RUN` and that is deliberate. If
  the application needs `npm install`, `pip install` or a compiler at image-build time, apko is
  the wrong tool *unless* you first turn that work into a package with melange — which is a
  real cost
- **Application images with fast-changing code.** apko is at its best for bases and for
  packaged software. For "rebuild on every commit of my service", ordinary multi-stage
  Dockerfiles (or [`ko`](../ko/README.md) for Go) are less friction
- **The packages you need are not in Wolfi or Alpine.** apko can only install what a package
  repository already offers
- **You are not prepared to introduce new tooling.** Everyone knows Dockerfiles; nobody arrives
  knowing apko. If the goal is only "fewer CVEs", [`distroless`](../distroless/README.md) gets
  most of the benefit with zero new concepts

## Notes

Original note recorded for this tool:

- <https://github.com/chainguard-dev/apko> — the upstream project from Chainguard. The
  repository holds the CLI, the YAML schema reference for image configuration, and the examples
  worth reading first. It is also where the SBOM generation behaviour is documented — apko emits
  SPDX (and CycloneDX) alongside the image as part of the build, which is the feature that
  distinguishes it from scanning an image afterwards.

Two practical points not in the note but worth recording:

- apko and melange are usually driven together through the same YAML conventions used across
  [`wolfi-dev/os`](https://github.com/wolfi-dev/os), so that repository is the largest working
  corpus of real apko/melange configuration available.
- apko can publish and sign in one step, which connects directly to
  [`../../admission/README.md`](../../admission/README.md): an image built by apko already has
  the signature and attestations an admission verifier will ask for.

---

[← Base images](../README.md)
