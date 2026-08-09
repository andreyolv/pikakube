[← Builders](../README.md)

# Docker

<https://github.com/docker/buildx>
<https://github.com/docker/build-push-action>
<https://github.com/docker/compose>
<https://github.com/docker/buildkit-syft-scanner>

Linters covered here: [`hadolint`](hadolint/README.md) — the Dockerfile ·
[`dockle`](dockle/README.md) — the resulting image

---

## The problem it solves

**The default way to build a container image, and the reason everything else in this folder had to
be invented.** Docker is a CLI plus a root daemon; `docker build` hands a context to the daemon,
which runs each instruction in a container and captures the result as a layer.

Since Docker 23 the engine underneath is **BuildKit**, and **Buildx** is the CLI in front of it.
That matters because it is where the features people miss actually live:

| Feature | Why it matters |
|---|---|
| **Parallel build graph** | independent stages build simultaneously instead of top to bottom |
| **Cache export** — `--cache-to` / `--cache-from` | the layer cache lives in a registry, so ephemeral CI runners are viable |
| **Secret mounts** — `--mount=type=secret` | a credential available during a `RUN` and **not** baked into the layer |
| **SSH forwarding** — `--mount=type=ssh` | private dependencies without copying a key into the image |
| **Multi-platform** — `--platform linux/amd64,linux/arm64` | one tag, a manifest list, both architectures |
| Build checks | Docker's own linting, run during the build |

The ecosystem around it is the other half of the answer: `build-push-action` is the standard
GitHub Actions step for build, cache and push in one; Compose is how multi-container setups are
described locally; and `buildkit-syft-scanner` generates an SBOM as part of the build rather than
as a separate scanning step afterwards.

## When to use it

- **local development** — it is the tool everyone already has, and the feedback loop is shortest
- **CI runners that own their own engine** — a GitHub Actions runner, a VM-based runner
- multi-architecture builds, where Buildx's manifest-list support is the least painful route
- when the build needs secrets or SSH at build time without leaking them into layers
- anywhere the alternative would be adopting a second build tool for no gain

## When not to use it

- **as a pod inside Kubernetes** — that needs the node's socket, which is root on the node; use
  [`../../builder-k8s/`](../../builder-k8s/README.md)
- Docker-in-Docker in CI, which needs `privileged: true` and is the same escalation
- where rootless building is a requirement — [Buildah](../buildah/README.md) or
  [BuildKit rootless](../buildkit/README.md) address it directly
- where Docker Desktop's licensing is a problem — [Podman](../podman/README.md) is the drop-in
- where the build definition should not be a Dockerfile at all —
  [Buildpacks](../buildpacks/README.md)

## Notes

Everything below was recorded while working with Docker here.

**The tooling**

- <https://github.com/docker/buildx> — the Buildx CLI plugin. This is where cache export,
  multi-platform builds and secret mounts come from; plain `docker build` on an old engine has
  none of them.
- <https://github.com/docker/build-push-action> — the GitHub Actions step. It wires Buildx,
  registry login, cache import/export and push into one job step, and it is the shortest path
  from "CI builds an image" to "CI builds an image with a working cache".
- <https://github.com/docker/compose> — Compose. Not a builder, but the standard way to describe
  a local multi-container environment, and often the thing being translated when an application
  moves to Kubernetes.
- <https://github.com/kubernetes/kompose> — translates a `docker-compose.yml` into Kubernetes
  manifests. Useful as a **starting point** and not as an answer: the output is a literal
  transliteration with no probes, no resource limits and no sensible service accounts.
- <https://github.com/google/cadvisor> — Container Advisor, Google's per-container resource
  usage and performance collector. It is the component embedded in the kubelet that produces
  container metrics; recorded here because it is where container-level CPU and memory numbers
  originate.
- <https://github.com/docker/buildkit-syft-scanner> — generates an SBOM during the build using
  Syft. An SBOM produced at build time is accurate by construction, which is not true of one
  reconstructed from the image afterwards.
- <https://github.com/tonistiigi/binfmt> — QEMU emulation registered through `binfmt_misc`, so a
  single machine can build for other architectures. It is what makes
  `--platform linux/arm64` work on an x86 host, and it is **slow** for anything that compiles.

**Base images and size**

- <https://medium.com/@faruk13/alpine-slim-bullseye-bookworm-noble-differences-in-docker-images-explained-d9aa6efa23ec>
  — an explanation of what the base image tags actually mean. The short version: `bullseye`,
  `bookworm` and `noble` are distribution releases (Debian 11, Debian 12, Ubuntu 24.04); `slim`
  is the same distribution with documentation, locales and extras stripped; `alpine` is a
  different distribution altogether, built on musl rather than glibc — which is why it is small
  and why Python wheels and glibc-linked binaries sometimes misbehave on it.
- <https://wiki.debian.org/DebianReleases> — the Debian release table, which is how you find out
  what `bookworm` maps to and when it stops being supported. A base image on an
  end-of-life release stops receiving security updates, silently.
- <https://github.com/wagoodman/dive> — an interactive viewer for image layers. The fastest way
  to find out that an image is mostly a package cache somebody forgot to delete, and it reports
  wasted space explicitly.
- <https://github.com/GoogleContainerTools/distroless> — minimal base images containing the
  language runtime and nothing else: no shell, no package manager, no `ls`. Excellent for size
  and attack surface, and the absence of a shell is felt the first time something needs
  debugging — `kubectl exec` gives you nothing.
- <https://github.com/slimtoolkit/slim> — runs a container, observes which files are actually
  used, and rebuilds a minimal image from that. Dramatic size reductions and a real risk: a code
  path not exercised during observation can have its files removed.

**Practice and specifications**

- <https://docs.docker.com/build/building/best-practices/> — the canonical guidance on layer
  ordering, multi-stage builds and `.dockerignore`. Most of
  [§4 of the parent](../README.md#4-writing-a-dockerfile-that-builds-fast) is here.
- <https://docs.docker.com/reference/build-checks/> — build checks, which surface those
  best-practice violations during the build itself rather than in a separate linting step.
- <https://github.com/distribution/distribution/> — the reference registry implementation, which
  is what [`docker-registry`](../../oci-registry/docker-registry/README.md) deploys and what most
  other registries are built on or compatible with.
- <https://github.com/opencontainers/distribution-spec> — the registry HTTP API.
- <https://github.com/opencontainers/image-spec> — the image manifest, config and layer format.
- <https://github.com/opencontainers/runtime-spec> — how a container is actually run from a
  filesystem bundle. Together these three are why an image built by Buildah runs unchanged under
  containerd: the format is a standard, and the builder is swappable.

**Hardening reference**

- <https://public.cyber.mil/devsecops_enterprise_container_image_creation_and_deployment_guide_2/>
- <https://dl.dod.cyber.mil/wp-content/uploads/devsecops/pdf/DevSecOps_Enterprise_Container_Image_Creation_and_Deployment_Guide_2.6-Public-Release.pdf>

  The US Department of Defense's container image creation and deployment guide. Worth having as
  a reference for what a maximally conservative position looks like — signing, provenance,
  hardened bases, approved registries. The container-security material in this repository lives
  under `infrastructure/security/3-container/`.

**Commands recorded because they are needed regularly and never remembered**

Finding which library versions are installed in an image:

```bash
docker run --rm <image-name> bash -c "pip list"
docker run -it --rm <image> bash    # then look for requirements.txt
```

Useful when an image works and nobody can say which versions it actually contains — the answer is
inside the image, not in the repository that built it.

Clearing everything out:

```bash
docker system prune -a
```

Recorded as *"clean the whole lot"*. It removes stopped containers, unused networks, dangling and
**unused** images and the build cache. On a development machine it reclaims tens of gigabytes; it
also deletes the layer cache, so the next build is cold.

The step the installation instructions leave out:

```bash
sudo usermod -aG docker $USER
```

Recorded with some irritation as *"the command you have to use that is not in the documentation
after installing Docker"*. Without it every `docker` command needs `sudo`. Worth knowing what it
actually grants: membership of the `docker` group is **equivalent to root**, because anyone who
can talk to the daemon can start a privileged container with the host filesystem mounted. It is
fine on a personal machine and it is the exact reason the socket must never be exposed to a build
pod.

## Where it fits here

The folder also holds a small `build.sh` — the plain build, tag, push loop with `set -e` — and the
two linters, [hadolint](hadolint/README.md) for the Dockerfile and [dockle](dockle/README.md) for
the image it produces.

Docker is the right tool locally and in CI runners that own an engine. Inside the cluster it is
the wrong tool, and [`builder-k8s/`](../../builder-k8s/README.md) exists for that case.

---

[← Builders](../README.md)
