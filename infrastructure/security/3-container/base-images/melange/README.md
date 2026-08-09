[← Base images](../README.md)

# melange

<https://github.com/chainguard-dev/melange>

---

## The problem it solves

[`apko`](../apko/README.md) can only assemble packages that already exist. The moment you need
something that is not in [Wolfi](../wolfi/README.md) — a library at a specific version, an
internal application, a patched build of an upstream tool — you need a way to produce an apk
package. melange is that tool.

It builds apk packages **from source, declaratively**, in a sandboxed environment described by
YAML. The pipeline steps are named and constrained (fetch, patch, configure, build, install)
rather than arbitrary shell, which is what makes the result reproducible and the provenance
meaningful.

Why this matters beyond convenience:

| Property | Consequence |
|---|---|
| Build inputs are declared | the SBOM for the package is generated from what was actually used, not inferred |
| Builds run in a sandbox (bubblewrap, or a container) | the build cannot depend on undeclared state from the host |
| Output is signed | the package repository apko installs from is itself verifiable |
| Multi-architecture from one definition | no per-arch build scripts |

The step people miss: **melange is how your own application becomes a first-class part of the
image**, rather than a tarball copied in by a `COPY` line. Packaged application plus apko means
the whole image — base and app — is declared, reproducible and inventoried by the same
mechanism.

## When to use it

- **A package you need does not exist in Wolfi.** This is the primary trigger, and it is a real
  one: Wolfi is not Debian-sized
- **You need a patched build of an upstream package** — a backported fix, a build flag, a
  different compile-time option — and you want that patch recorded as provenance rather than
  hidden in a Dockerfile
- **You want the whole chain declarative.** melange (packages) → Wolfi (repository) → apko
  (image) is the only combination in this folder where nothing is built by executing an
  ad-hoc script
- **You are publishing packages internally.** An internal apk repository built with melange gives
  every team the same reproducibility and SBOM properties for shared components
- **Regulated environments** where "prove how this binary was produced" is an actual question

## When not to use it

- **You can consume an existing package.** Which is most of the time. Building packages is
  ongoing maintenance: upstream releases, security fixes and rebuild pipelines become yours
- **You are not using apko or Wolfi.** melange's output is an apk repository; consumed from a
  Dockerfile with `apk add` it still works, but the effort only really pays off in the full stack
- **The team has no packaging experience.** Writing correct build pipelines for C libraries,
  handling dependencies and split packages ("-dev", "-doc") is a distinct skill. Underestimating
  it is the usual way an adoption stalls
- **Short-lived application code.** A service rebuilt twenty times a day does not want a
  packaging step in front of the image build; a multi-stage Dockerfile or
  [`ko`](../ko/README.md) is the right shape

## Notes

Original note recorded for this tool:

- <https://github.com/chainguard-dev/melange> — the upstream project from Chainguard. It holds
  the CLI, the YAML pipeline reference (the named steps such as `fetch`, `patch`,
  `autoconf/configure`, `go/build`, `strip`), and the documentation for keygen and package
  signing. Reading the built-in pipelines is the fastest way to understand what melange will and
  will not let you do, because the constraint on arbitrary shell is the whole point of the tool.

The largest real-world corpus of melange definitions is
[`wolfi-dev/os`](https://github.com/wolfi-dev/os) — every package in Wolfi is a melange YAML in
that repository, which makes it the reference to copy from when writing your first one.

---

[← Base images](../README.md)
