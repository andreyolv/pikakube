[← OCI registry](../README.md)

# go-containerregistry (crane)

<https://github.com/google/go-containerregistry>

---

## The problem it solves

Two problems, and it is worth separating them because the repository is one thing and the tool is
another.

**The library** is Go's implementation of the OCI distribution and image specs — `pkg/v1` with its
`Image`, `Layer` and `ImageIndex` interfaces, `remote` for talking to registries, `authn` for
credentials, `layout`, `tarball`, `daemon` and `mutate`. Its model is immutable views of an image
plus functional mutations that produce new views, which is why an edit does not require unpacking
anything. **Most of the container ecosystem is built on it** — Cosign, Kaniko and ko among others —
so its behaviour is, in practice, what "how registries work" means in Go.

**The CLI is [crane](https://github.com/google/go-containerregistry/blob/main/cmd/crane/README.md)**,
and it is a client in the same sense as [skopeo](../skopeo/README.md): no daemon, no local image
store, no root. What it adds beyond copy-and-inspect is the interesting part:

| Command | What it does |
|---|---|
| `crane copy` | stream an image between registries, digest preserved |
| `crane digest`, `crane manifest`, `crane config` | read metadata without pulling layers |
| `crane ls`, `crane catalog` | enumerate tags and repositories |
| `crane tag` | add a tag to an existing digest — **server-side, no pull** |
| **`crane append`** | add a layer of files to a base image — an image **built without a Dockerfile or a daemon** |
| **`crane mutate`** | change entrypoint, command, env, labels or annotations, producing a new image |
| **`crane rebase`** | swap the base image underneath an application layer, **without rebuilding** |
| `crane flatten` | collapse an image to a single layer |
| `crane index` | assemble or filter a multi-architecture index |
| `crane export` | write the image filesystem out as a tarball |
| `crane registry serve` | run a throwaway in-memory registry, for tests |

**`rebase` is the command that has no equivalent elsewhere.** When a base image ships a CVE fix,
the ordinary answer is to rebuild every application image that used it — which needs every build
context, every toolchain and every pipeline to still work. `crane rebase` replaces the old base
layers with the new ones in the registry and writes a new manifest; the application layer is byte
for byte the one that was tested. What it cannot do is fix anything *compiled against* the old
base, so it applies to images where the application layer is self-contained — a static binary, a
JAR, an interpreted app whose runtime lives in the base.

`gcrane` is the same tool with GCR-specific additions (recursive copy, garbage collection of
untagged images); `krane` swaps in Kubernetes workload-identity authentication.

## crane or skopeo

They overlap on the operations people actually run, and the honest answer is that either covers
the common case.

| | **crane** | **[skopeo](../skopeo/README.md)** |
|---|---|---|
| Family | Google, the Go OCI libraries | `containers/`, alongside Podman and Buildah |
| Copy and inspect | yes | yes |
| **Edit an image** — append, mutate, rebase, flatten | **yes** | no |
| Multi-arch index assembly | `crane index` | limited |
| Air-gap tarball transports | `oci-archive` via `pull`/`push` | **`oci-archive:`, `docker-archive:`, `dir:` as first-class transports** |
| Local container store | no | **`containers-storage:`** — shares Podman's and Buildah's store |
| Whole-repository mirroring | `gcrane cp -r` | **`skopeo sync`** |
| Serve a test registry | **`crane registry serve`** | no |

The split that holds up: **skopeo for moving images around**, especially across the air gap or into
a local Podman store; **crane for changing them** without a build. Installing both is normal, and
neither replaces a registry's own scheduled replication where one exists.

## When to use it

- **rebasing** application images onto a patched base after a CVE, at fleet scale
- retagging and promoting by digest in CI, where the pipeline has no engine — a single static
  binary, and it is what the [§5 promotion argument](../../README.md#5-tags-lie-digests-do-not)
  needs
- reading a remote image's digest, labels or architectures in a script
- assembling a multi-architecture index from per-architecture builds
- building trivial images — a config bundle, a set of static files — with `crane append`, with no
  Dockerfile and no builder pod
- `crane registry serve` as a test fixture, instead of standing up a registry for a test suite

## When not to use it

- to **build real images**. `append` is a layer of files, not a build; Dockerfiles belong to
  [`builder/`](../../builder/README.md) and [`builder-k8s/`](../../builder-k8s/README.md)
- as a **retention policy**. Scripted deletes are not retention — that is registry policy, and
  [Harbor](../harbor/README.md) is where it is configured
- as a replacement for native registry replication with retries and status
  ([Harbor](../harbor/README.md), [zot](../zot/README.md) both have it)
- for signing or verification — that is
  [Cosign](../../../../security/0-governance/supply-chain/signing-artifacts/cosign/README.md), which
  is itself built on this library

## Notes

Apache-2.0. Installed as a release binary (published with SLSA provenance), via `go install`,
through Homebrew, or run as a container image at `gcr.io/go-containerregistry/crane` — the `:debug`
tag is the one with a shell, which matters when it runs as a step inside a pipeline image.

**In GitHub Actions: [`imjasonh/setup-crane`](https://github.com/imjasonh/setup-crane).** It is
recorded here rather than in its own folder because it is one step that installs one binary — the
tool is the subject, the action is how it arrives.

```yaml
- uses: imjasonh/setup-crane@v0.1
  with:
    version: v0.20.2          # omit for latest; `tip` builds from source
- run: crane copy ubuntu:24.04 ghcr.io/${{ github.repository }}/ubuntu:24.04
```

It runs on Linux and macOS runners and wires up GitHub Container Registry authentication by
default, which is the whole reason to use it instead of a `curl | tar` step. Two things to note:
it is maintained by an individual — Jason Hall, a go-containerregistry maintainer — rather than by
the project or by GitHub, so it is a third-party action in the sense
[`cicd/github-actions/`](../../../cicd/github-actions/README.md) means it; and **pin the crane version
explicitly**. `version` defaults to the latest release, which makes a pipeline's behaviour depend
on when it ran.

The same argument applies to the action reference itself: `@v0.1` is a mutable tag, and the
position taken in [`cicd/github-actions/`](../../../cicd/github-actions/README.md#8-anti-patterns)
and in [`supply-chain/`](../../../../security/0-governance/supply-chain/README.md) is to pin
third-party actions by commit SHA rather than by tag.

Nothing is deployed. This is a CLI and a library; the folder holds the reference.

## Where it fits here

The second client in [`oci-registry/`](../README.md), next to
[skopeo](../skopeo/README.md) — both are here because they are what you reach for *when working
with* registries, not because they are registries.

Read it against the parent's two central points. `crane digest` and `crane tag` are
[§5 — tags lie, digests do not](../../README.md#5-tags-lie-digests-do-not) as commands: the digest
is readable without a pull, and a tag can be added to a digest without one either. And `crane
rebase` is the cheap answer to the base-image half of
[§8](../../README.md#8-size-base-images-and-reproducibility) — the reason
[kpack](../../builder-k8s/kpack/README.md) exists is rebuilding on a base-image change, and rebase
is the same outcome for images whose application layer does not need recompiling.

---

[← OCI registry](../README.md)
