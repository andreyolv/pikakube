[← Base images](../README.md)

# Distroless

<https://github.com/GoogleContainerTools/distroless>

---

## The problem it solves

A normal base image ships an entire operating system userland — a shell, a package manager,
coreutils, and dozens of libraries — to run a single process that needs none of it. Every one
of those packages is inventoried by a scanner, appears in reports, needs patching, and is
available to anyone who achieves code execution inside the container.

Distroless images contain **only what the application needs to run**: the language runtime (or
nothing at all, for static binaries), CA certificates, timezone data, and `/etc/passwd`. There
is no `/bin/sh`, no `apt`, no `busybox`.

The security argument is direct: a remote code execution that lands in a distroless container
has no shell to spawn, no package manager to install a second stage, and no `curl` to exfiltrate
with. It is not a barrier to a determined attacker, but it removes the entire class of
opportunistic tooling that off-the-shelf exploits assume is present.

The variants published by the project:

| Image | Contents | For |
|---|---|---|
| `static` | CA certs, tzdata, `/etc/passwd` — no libc | Go and Rust static binaries |
| `base` | the above plus glibc | cgo binaries, anything dynamically linked |
| `cc` | `base` plus libgcc/libstdc++ | C/C++ applications |
| `java` | a JRE | JVM workloads |
| `python3`, `nodejs` | the interpreter | Python and Node (see the caveat below) |

Each also publishes `:nonroot` (runs as UID 65532) and `:debug` (adds busybox, for local
reproduction only) variants.

## When to use it

- **Go, Rust and C/C++ services** — a static binary plus `static` or `cc` is close to a
  zero-package image, and the migration is a one-line `FROM` change in a multi-stage build
- **JVM services** — `distroless/java` avoids shipping a full OS to run a JAR
- **You want the benefit without adopting new tooling** — this is distroless's real advantage
  over Chainguard's stack: it is *just an image*. Your Dockerfile, your registry, your CI all
  stay exactly as they are
- **The multi-stage pattern already exists** — build in a full image, copy the artefact into
  distroless. If your Dockerfiles are already multi-stage the change is nearly free

## When not to use it

- **The team will not give up `kubectl exec`.** This is the honest blocker. There is no shell,
  so interactive debugging in the container is gone. The answer is ephemeral debug containers
  (`kubectl debug -it <pod> --image=busybox --target=<container>`), and if that is not
  established practice the minimal base will be reverted during the first incident
- **Shell-form `ENTRYPOINT`/`CMD`, init scripts, or `exec` healthchecks.** All of them assume a
  shell. Convert to exec form and native probes first
- **Anything needing `RUN` in a derived image.** There is no shell for `RUN` to use — all
  build-time work must move to an earlier stage
- **Python and Node, sometimes.** The interpreted-language images are the weakest part of the
  project: dependency installation needs a package manager that is not there, native extensions
  need build tooling, and the images have historically lagged on runtime versions. Wolfi and
  the Chainguard Python/Node images are usually the better answer for these — see
  [`wolfi/README.md`](../wolfi/README.md)
- **You need a specific glibc or OS package.** Distroless is not customisable; you take what is
  published. `apko` exists for the case where you want to choose the package list yourself

## Notes

Original note recorded for this tool:

- <https://github.com/GoogleContainerTools/distroless> — the upstream project, maintained by
  Google under the GoogleContainerTools organisation. It is the source of the image
  definitions, the variant matrix (`static`/`base`/`cc`/`java`/`nodejs`/`python3`) and the
  documentation for the `:nonroot` and `:debug` tags. Images are published to
  `gcr.io/distroless/*`, and the repository is also where the Bazel rules that build them live.

Worth knowing beyond the note: the images are built with Bazel and signed with Cosign, so they
can themselves be verified at admission — the same mechanism described in
[`../../admission/README.md`](../../admission/README.md). Verification of the distroless base is
a reasonable first policy to enable, because it is a real supply-chain check that costs nothing
in developer friction.

---

[← Base images](../README.md)
