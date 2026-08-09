[← OCI registry](../README.md)

# skopeo

<https://github.com/containers/skopeo>

---

## The problem it solves

**Working with images in registries without pulling them into a local engine.** skopeo is a
client, not a server: it copies, inspects, deletes and signs images by talking the registry API
directly. No daemon, no local image store, and no root.

The operations that matter:

| Command | What it does |
|---|---|
| `skopeo copy` | move an image between registries — **without unpacking it** |
| `skopeo inspect` | read a manifest, its labels, layers and digest, without downloading layers |
| `skopeo list-tags` | enumerate tags in a repository |
| `skopeo delete` | remove a tag from a registry |
| `skopeo sync` | mirror whole repositories, including to and from a directory |

`copy` is the one that justifies the tool. `docker pull` followed by `docker tag` and `docker push`
downloads every layer, unpacks it into the local store, repacks it and uploads it again. `skopeo
copy` **streams the blobs from one registry to the other**, so it is faster, needs no disk, and —
critically — the destination digest is identical to the source digest. Nothing is rebuilt, so
nothing can change.

The transports it understands make the awkward cases easy:

| Transport | Use |
|---|---|
| `docker://` | a registry |
| `dir:` | a directory on disk |
| **`oci-archive:` / `docker-archive:`** | a tarball — the air-gap format |
| `containers-storage:` | the local store shared with Podman and Buildah |

## When to use it

- **promoting an image between environments** — copy the exact digest from a development registry
  to production, with no rebuild
- **mirroring** upstream images into a registry you control
- **air-gapped transfer**: `copy docker:// oci-archive:`, carry the tarball across, copy it back
- inspecting a remote image's digest, labels or architecture without pulling it
- in CI, where it is a small static binary and there is no engine to install
- scripted registry cleanup, using `list-tags` and `delete`

## When not to use it

- to **build** images — that is [Buildah](../../builder/buildah/README.md), from the same family
- to run containers — that is [Podman](../../builder/podman/README.md)
- as a replacement for a registry's own replication, when it has one:
  [Harbor](../harbor/README.md) and [zot](../zot/README.md) do scheduled sync natively, with
  retries and status
- as a substitute for retention policy; ad-hoc `skopeo delete` is not a retention strategy

## Notes

Recorded link:

- <https://github.com/containers/skopeo> — the tool, in the `containers` organisation alongside
  [Podman](../../builder/podman/README.md), [Buildah](../../builder/buildah/README.md) and CRI-O.
  They share the same image and storage libraries, which is why skopeo can read Buildah's local
  store and write a registry with no format conversion in between.

**Why a client is filed under `oci-registry/`.** It is not a registry, and it is here because it
is the tool you reach for *when working with* registries. The three workflows it owns are all
registry workflows:

| Workflow | Command shape |
|---|---|
| Promote by digest | `skopeo copy docker://dev/app@sha256:… docker://prod/app:1.2.3` |
| Mirror an upstream | `skopeo sync --src docker --dest docker docker.io/library/nginx myregistry/nginx` |
| Air-gap | `skopeo copy docker://… oci-archive:app.tar`, then the reverse on the other side |

The promotion case is worth spelling out because it interacts with
[§5 of `image/`](../../README.md#5-tags-lie-digests-do-not). Promoting by **digest** means the
artefact that reaches production is bit-for-bit the one that was tested. Rebuilding from the same
Git commit does not give that guarantee — the base image may have moved, a dependency may have
been re-published. Copying a digest is the only promotion that is actually reproducible.

Nothing is deployed here; this is a CLI, and the folder holds only the reference.

## Where it fits here

The one entry in [`oci-registry/`](../README.md) that is a client rather than a server. It
complements every registry in the folder, and it is the tool that makes an air-gapped or
multi-environment setup workable without extra infrastructure.

Read it alongside [`../../cache/`](../../cache/README.md): where those tools mirror images
automatically through a controller, skopeo is the manual, scriptable version of the same
operation — and often the right one for a handful of images.

---

[← OCI registry](../README.md)
