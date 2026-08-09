[← Builders](../README.md)

# Buildah

<https://github.com/containers/buildah>

---

## The problem it solves

**Building OCI images with no daemon at all.** Buildah calls the container libraries directly —
the same ones [Podman](../podman/README.md) and CRI-O use — so there is no long-running privileged
process anywhere in the picture.

It offers two ways to work, and the second is the distinctive one:

| Mode | What it is |
|---|---|
| `buildah bud` | **b**uild **u**sing **D**ockerfile — a drop-in for `docker build` |
| **The scripted API** | `buildah from`, `buildah run`, `buildah copy`, `buildah config`, `buildah commit` |

The scripted mode means an image can be built by a shell script instead of a Dockerfile. Each
command is one step, and you decide when a layer is committed — so a build can install packages,
configure, and clean up, and commit **once**, producing an image with no intermediate layer
holding the package cache. Dockerfiles fake this with `&&` chains; Buildah just does not need to.

The properties that decide adoption:

- **rootless** via user namespaces and `fuse-overlayfs` — no root, no daemon, no socket
- it can mount a container's filesystem on the host (`buildah mount`) and manipulate it with
  ordinary tools
- native OCI output, part of the `containers/` toolchain alongside Podman and
  [skopeo](../../oci-registry/skopeo/README.md)
- Red Hat is the primary sponsor, so it is well supported on RHEL-family systems

## When to use it

- **unprivileged builds in CI**, where the runner must not have a daemon or root
- **as a build pod in Kubernetes** — a one-shot pod, no controller, no daemon lifecycle
- on RHEL, Fedora or OpenShift, where it is the native path and Docker is not
- when the build genuinely needs scripting rather than a Dockerfile — conditional steps, or
  precise control over which steps become layers
- as the strategy behind [Shipwright](../../builder-k8s/shipwright/README.md), where it is one of
  the standard build strategies

## When not to use it

- on a developer machine where everyone already has Docker and nothing is gained
- where builds are frequent enough that a warm daemon with a persistent cache wins —
  [BuildKit](../buildkit/README.md)
- where BuildKit's richer cache and secret mounts are actually being used; Buildah's caching is
  more basic
- on Windows or macOS, where it needs a Linux VM and the experience is worse than
  [Podman](../podman/README.md)'s

## Notes

Recorded link:

- <https://github.com/containers/buildah> — the tool, in the `containers` organisation alongside
  Podman, skopeo and CRI-O. That grouping is the useful context: these are four tools that share
  the same image and storage libraries, so a container built by Buildah is stored where Podman
  expects it and copied by skopeo without any conversion.

Where it sits among the daemonless options:

| | **Buildah** | [Kaniko](../../builder-k8s/kaniko/README.md) | [BuildKit](../buildkit/README.md) rootless |
|---|---|---|---|
| Rootless | **yes** | no — root inside its own container | **yes** |
| Shape | a CLI, run as a one-shot pod | a one-shot pod | a daemon |
| Dockerfile | `bud`, or scripted | Dockerfile only | Dockerfile, or another frontend |
| Cache | registry-based, basic | registry repository | rich — registry, local, mounts |
| Maintenance | active | see the note in its folder | active |

Together with [BuildKit rootless](../buildkit/README.md), Buildah is one of the two credible
answers to the in-cluster build problem, and the choice between them is mostly about shape: a
one-shot pod per build, or a daemon that stays warm.

## Where it fits here

Documented as an alternative; nothing in this repository builds with it. Its relevance is as the
replacement path for [Kaniko](../../builder-k8s/kaniko/README.md) — a one-shot pod, the same
mental model, actively maintained, and rootless into the bargain.

---

[← Builders](../README.md)
