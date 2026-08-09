[← Base images](../README.md)

# ko

<https://github.com/ko-build/ko>

---

## The problem it solves

For a Go application, a container image is a solved problem that everyone re-solves badly. The
typical Dockerfile is a multi-stage build that copies the module cache, runs `go build` inside a
container, and copies the binary out — reimplementing, slowly and with a Docker daemon in the
loop, something the Go toolchain already does on the host in seconds.

ko removes the Dockerfile entirely. It compiles the Go binary locally, lays it into a base image
(distroless static by default), and pushes the result to a registry:

```bash
# build, push, and print the resulting image reference
ko build ./cmd/server

# render Kubernetes YAML with image references replaced by the ones just built
ko resolve -f config/ | kubectl apply -f -
```

What follows from that design:

| Property | Why |
|---|---|
| **No Docker daemon required** | ko writes OCI layers directly and pushes over the registry API |
| **Near-zero CVEs** | the image is a static binary plus CA certificates — there are no packages to have vulnerabilities |
| **Fast and cacheable** | it uses the ordinary Go build cache on the host, not a container-layer cache |
| **Reproducible** | deterministic timestamps and layering by default |
| **SBOM by default** | ko emits an SPDX SBOM alongside the image |
| **Multi-arch trivially** | `--platform=all`, using Go's own cross-compilation, with no QEMU |
| **YAML rewriting** | `ko resolve`/`ko apply` substitute `ko://` import paths with real digests, which is why so many Kubernetes controllers ship with it |

The reason it matters here rather than only in the build tooling: the resulting image has
essentially no attack surface and essentially nothing for a scanner to report. Findings against
a ko-built image are, almost by construction, findings in **your Go dependencies** — which is
[`4-code/sca/`](../../../4-code/sca/README.md)'s problem, correctly located.

## When to use it

- **Go services, CLIs, controllers and operators.** This is the entire target audience and
  within it ko is the fastest and simplest option available
- **Kubernetes controllers specifically** — the `ko://` reference rewriting removes the whole
  "build image, compute tag, template it into YAML" dance from local development and CI
- **CI runners without a Docker daemon.** ko needs no privileged container and no daemon socket,
  which sidesteps a genuine security problem in shared runners
- **You want a zero-CVE image with no new build system to learn.** For Go it is one command

## When not to use it

- **Anything not written in Go.** There is no extension mechanism for other languages; this is a
  hard boundary
- **cgo-heavy builds.** ko defaults to `CGO_ENABLED=0`. cgo works, but you must supply a base
  image with the right libc and manage cross-compilation yourself, at which point much of the
  simplicity is gone
- **The image needs more than a binary** — configuration files, templates, a whole assets
  directory. ko supports static assets through `kodata`, but if the image is really a filesystem
  with a binary in it, a Dockerfile is the honest choice
- **You need a shell in the image.** The default base is distroless static: no shell, by design.
  Debugging is `kubectl debug` with an ephemeral container
- **Monorepo images combining multiple languages** — ko builds one Go binary per image

## Notes

Original note recorded for this tool:

- <https://github.com/ko-build/ko> — the upstream project. Now a CNCF sandbox project, it began
  at Google and is the tool most of the Knative and Tekton ecosystems are built with. The
  repository documents the `ko://` reference scheme, the `kodata` mechanism for static assets,
  the `defaultBaseImage`/`baseImageOverrides` settings in `.ko.yaml` for swapping the base image,
  and the SBOM and signing behaviour.

Two points worth carrying forward:

- The default base is `cgr.dev/chainguard/static` (previously `gcr.io/distroless/static`), which
  ties ko directly to the rest of this folder — see [`distroless/README.md`](../distroless/README.md).
- Because ko signs and attests optionally but produces a digest reference always, it pairs
  cleanly with admission verification described in
  [`../../admission/README.md`](../../admission/README.md).

---

[← Base images](../README.md)
