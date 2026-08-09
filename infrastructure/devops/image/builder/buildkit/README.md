[← Builders](../README.md)

# BuildKit

<https://github.com/moby/buildkit>

---

## The problem it solves

**The build engine that replaced Docker's original one**, and the one that can run without a
privileged daemon.

Two things are true at once and often confused. BuildKit is what is *inside* modern Docker — since
Docker 23 it is the default builder, driven through [Buildx](../docker/README.md). It is also a
**standalone daemon** (`buildkitd`) that runs on its own, including **rootless**, which is what
makes it a candidate for building inside Kubernetes.

What it does differently from the classic builder:

| Capability | Detail |
|---|---|
| **Build as a DAG** | independent stages run in parallel instead of strictly top to bottom |
| **Skips unused stages** | a stage nothing depends on is never executed |
| **Cache export** | `--cache-to type=registry` puts the layer cache in a registry, not on a disk that disappears |
| **Secret mounts** | `RUN --mount=type=secret` — available during the step, absent from the layer |
| SSH forwarding | `RUN --mount=type=ssh` for private dependencies, with no key in the image |
| Cache mounts | `RUN --mount=type=cache` for package manager caches that survive between builds |
| **Rootless mode** | user namespaces, no privileged operations, no host socket |
| Multi-platform | native or emulated, producing a manifest list |
| Frontends | the Dockerfile syntax is one frontend; others are possible |

The cache and secret features are the ones that change how a pipeline is written. Without cache
export, an ephemeral CI runner rebuilds everything every time. Without secret mounts, private
credentials get passed as `ARG` and end up permanently in a layer.

## When to use it

- **as a build daemon inside Kubernetes**, in rootless mode — a `Deployment` or `StatefulSet` that
  CI submits builds to, with a persistent cache volume and no host privileges
- in CI where the build must be unprivileged but a full Dockerfile is still wanted
- when the build has independent stages that can genuinely run in parallel
- when build secrets are needed and must not be baked in
- indirectly, and almost always: through `docker buildx`, where it is already the engine

## When not to use it

- for a one-shot build with no reuse, where a single Kaniko or Buildah pod is less to run —
  BuildKit is a daemon, and a daemon has a lifecycle
- where a shared build daemon is a problem: it is multi-tenant by convenience rather than by
  design, and concurrent builds from different teams share a cache
- where the team wants no build definition at all — [Buildpacks](../buildpacks/README.md)
- where the CI system already provides a maintained builder and adding another is pure operational
  cost

## Notes

Recorded link:

- <https://github.com/moby/buildkit> — the engine itself. It sits under the `moby` organisation
  rather than `docker`, which is the clue to its status: it is the upstream build component that
  Docker consumes, and it is usable entirely on its own.

The point that matters for this repository is **rootless mode**. BuildKit is the most credible
long-term answer to the problem described in
[`builder-k8s/`](../../builder-k8s/README.md#2-what-the-socket-actually-grants): it builds in user
namespaces, needs no host socket and no `privileged: true`, and it is actively maintained upstream
by the same people who maintain the Docker build path. It does need `seccomp` and `AppArmor`
annotations relaxed on the pod for user namespaces to work, which is a much smaller ask than root
on the node.

Compared with the alternatives for in-cluster builds:

| | **BuildKit rootless** | [Kaniko](../../builder-k8s/kaniko/README.md) | [Buildah](../buildah/README.md) |
|---|---|---|---|
| Shape | a daemon builds are submitted to | one pod, one build | one pod, one build |
| Rootless | yes | no — root inside its own container | yes |
| Cache | rich: registry, local, mounts | registry repository | registry |
| Maintenance | active | see the note in its folder | active |
| Setup cost | a deployment to run | a pod manifest | a pod manifest |

The practical division: Kaniko or Buildah for a simple build-on-demand job, BuildKit when builds
are frequent enough that a warm daemon with a persistent cache pays for itself.

## Where it fits here

Documented as reference material; nothing in this repository deploys `buildkitd`. It is reachable
today through `docker buildx` on a developer machine, and it is the successor to plan for in the
cluster as [Kaniko](../../builder-k8s/kaniko/README.md) ages out.

---

[← Builders](../README.md)
