[← Base images](../README.md)

# Wolfi

<https://github.com/wolfi-dev/os>

---

## The problem it solves

Traditional Linux distributions were designed for machines, and containers inherited all of
their assumptions: a kernel, an init system, a service manager, a package set sized for a
general-purpose server, and — decisively — a **release cadence**. When a CVE is fixed upstream,
a distribution's patched package appears days or weeks later, because that is how stable
release engineering works.

Wolfi is a Linux **undistro** built for containers only. The design choices that matter:

| Choice | Consequence |
|---|---|
| **No kernel** | it is not a bootable OS; it only ever runs as a container base |
| **glibc, not musl** | manylinux Python wheels, the JVM and cgo all behave normally — the thing Alpine gets wrong |
| **apk package format** | Alpine's tooling and small package granularity, without Alpine's libc |
| **Rolling, continuously rebuilt** | a fixed package is usually available within hours, not weeks |
| **Every package built with melange, with SBOM and signatures** | provenance for the whole base, not just for your layer |
| **Aggressively minimal package granularity** | you install a runtime without pulling in a compiler and a shell |

The result is the property Chainguard markets and which is broadly accurate for the images
themselves: **zero known CVEs** in the base most of the time. Not because vulnerabilities are
hidden, but because the package set is small and the rebuild loop is fast enough that fixes land
before scanners flag them.

The practical framing: Wolfi is what you use when you want a base as small as Alpine, as
compatible as Debian, and patched faster than either.

## When to use it

- **Python, Node and JVM workloads that need a small base.** This is Wolfi's strongest case,
  because glibc means wheels install and the JVM behaves — the two things that make Alpine
  painful and distroless awkward for interpreted languages
- **You want to keep writing normal Dockerfiles.** `FROM cgr.dev/chainguard/wolfi-base` with
  `RUN apk add ...` works exactly as expected. Unlike apko, nothing about your build changes
- **CVE turnaround is the actual complaint.** If the recurring problem is "the fix exists
  upstream but our base has not picked it up", Wolfi's continuous rebuild is precisely the fix
- **You need a shell in the final image** and still want it minimal — `wolfi-base` gives you
  that; distroless cannot
- **As the foundation for [`apko`](../apko/README.md)** — apko needs a package repository to
  assemble from, and Wolfi is it

## When not to use it

- **A package you need does not exist in Wolfi.** The repository is large but not
  Debian-sized. The answer is to build it with [`melange`](../melange/README.md), which is real
  work — evaluate this before committing
- **Your organisation requires a vendor-supported enterprise distribution** for compliance
  reasons (RHEL/UBI). Wolfi is community-built; Chainguard sells supported images on top of it,
  which is a commercial relationship, not the same thing as RHEL support
- **You depend on distribution-specific behaviour** — systemd units, RPM/dpkg tooling in the
  image, or anything expecting a full FHS userland
- **Long-term reproducibility from tags.** Wolfi is rolling: there are no stable point releases
  to pin to. Pin by **digest** if you need the same bytes twice
- **A static Go or Rust binary.** You do not need a distribution at all — distroless `static`
  or [`ko`](../ko/README.md) is smaller still

## Notes

Original note recorded for this tool:

- <https://github.com/wolfi-dev/os> — the Wolfi OS repository. This is where the package
  definitions live: each package is a melange YAML file, so the repository doubles as the
  evidence of how every package in the distribution was built. Useful in practice for two
  things: checking whether a package you need already exists before deciding to build it, and
  reading a real melange definition when you have to write one yourself.

Related repositories in the same stack, documented separately in this folder:
[`apko`](../apko/README.md) assembles Wolfi packages into images, and
[`melange`](../melange/README.md) builds the packages. The three are designed together and are
best understood as one pipeline — see [`../README.md`](../README.md) section 3.

---

[← Base images](../README.md)
