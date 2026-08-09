[← Building inside Kubernetes](../README.md)

# Kaniko

<https://github.com/GoogleContainerTools/kaniko>

---

## The problem it solves

**Building an image from a Dockerfile inside a container, with no daemon and no privileges on the
node.** Kaniko was the first widely used answer to the problem in
[§2 of the parent](../README.md#2-what-the-socket-actually-grants), and it is still the simplest.

How it works: the executor image runs as a pod. It extracts the base image's filesystem into its
own container's root, executes each Dockerfile instruction in userspace, snapshots the filesystem
after each one to produce a layer, assembles the manifest, and pushes. No daemon, no socket, no
`privileged: true`.

| Property | Detail |
|---|---|
| Input | a standard `Dockerfile` — no changes to existing builds |
| Context | a mounted volume, a **Git URL**, a tarball, S3 or GCS |
| Cache | `--cache=true --cache-repo=<repo>` pushes layers to a registry repository |
| Credentials | a `dockerconfigjson` secret mounted at `/kaniko/.docker` |
| Shape | one pod, one build, then gone |
| Privileges on the node | **none** |

The caveat, which is often misstated: Kaniko is **not rootless**. It runs as root *inside its own
container* and modifies that container's filesystem destructively — which is why it must never be
run outside a container, and why it is a weaker position than
[BuildKit rootless](../../builder/buildkit/README.md) or
[Buildah](../../builder/buildah/README.md). It does not need privileges on the node, which was
always the point.

## When to use it

- **the simplest possible in-cluster build**: a pod, a Dockerfile, a registry secret
- an existing Dockerfile estate that must keep working unchanged
- CI that can create a pod and wants nothing else running permanently
- as a [Shipwright](../shipwright/README.md) or Tekton build strategy, where it is one of the
  standard ones
- when the build context should come straight from Git with no volume to populate

## When not to use it

- **as the foundation of a new long-lived platform** — see the maintenance note below
- where genuinely rootless building is required — BuildKit rootless or Buildah
- where builds are frequent enough that a warm daemon and a rich cache pay off — BuildKit
- for very large or unusual Dockerfiles: Kaniko's filesystem snapshotting has always been the
  slow part, and heavy `RUN` steps that touch many files are where it shows
- anywhere outside a container, which is explicitly unsupported and will damage the host

## Notes

Recorded link:

- <https://github.com/GoogleContainerTools/kaniko> — the project, under Google's
  `GoogleContainerTools` organisation alongside
  [distroless](https://github.com/GoogleContainerTools/distroless).

**Maintenance status, stated plainly.** Kaniko's development slowed substantially and Google
stepped back from actively developing it; long gaps between releases and a large backlog of open
issues are the visible symptoms. It still works, it is still widely deployed, and it is **not the
tool to build a new platform on in 2026 without checking the repository's current state first**.

The replacements, in the same shape:

| Instead of Kaniko | Why |
|---|---|
| **[BuildKit rootless](../../builder/buildkit/README.md)** | actively maintained, genuinely rootless, much better caching |
| **[Buildah](../../builder/buildah/README.md)** | actively maintained, rootless, same one-pod-per-build model |
| [Shipwright](../shipwright/README.md) | abstracts over all of them, so the choice can change later |

The manifests in this folder remain useful whichever tool wins, because the surrounding
problems — context, credentials, cache, cleanup — are identical.

**What is set up here.** The folder holds a complete working example:

| File | What it is |
|---|---|
| `kaniko.yaml` | a build `Pod` taking its context from a mounted volume at `/workspace`, pushing to `andreyolv/flask-kaniko:latest`, with `--cache=true --cache-repo=andreyolv/kaniko-cache` |
| `kaniko-git.yaml` | the same build with `--context=git://github.com/andreyolv/plumbers.git` and `--context-sub-path=docker/flask`, so no volume is needed at all |
| `namespace/` | the `kaniko` namespace |
| `pv/`, `pvc/` | a 5 Gi `hostPath` `PersistentVolume` and its claim, for the build context |
| `secrets/dockerhub.yaml` | the registry credential, mounted at `/kaniko/.docker` as `config.json` |
| `secrets/git-token.yaml` | a GitHub token, injected as `GIT_TOKEN` for private context repositories |

Both pods set modest CPU and memory requests and limits (`100m` / `256Mi`) and
`restartPolicy: Never`, which is right for a build — a failed build should stay failed and
visible, not restart in a loop.

The two comments recorded inline in the manifests are worth keeping:

- <https://github.com/settings/tokens> — where the `GIT_TOKEN` comes from.
- the `kubectl create secret docker-registry` command for the registry credential:

  ```bash
  kubectl create secret docker-registry regcred \
    --docker-server=<your-registry-server> \
    --docker-username=<your-name> \
    --docker-password=<your-pword> \
    --docker-email=<your-email>
  ```

  with the Kubernetes documentation link for pulling from a private registry.

**Two things about this setup that do not generalise**, and both are worth fixing before it is
used for anything real:

1. **The `PersistentVolume` is a `hostPath`.** That works on a single-node cluster and breaks
   silently on a multi-node one — the pod schedules onto a node where `/kaniko-context` is empty.
   The Git-context variant avoids the problem entirely and is the one to build on.
2. **The destinations end in `:latest`.** Fine for an experiment, and exactly what
   [§5 of `image/`](../../README.md#5-tags-lie-digests-do-not) argues against for anything that
   gets deployed. An immutable tag per build is the fix, and it is also what makes the update
   automation in [`../../update/`](../../update/README.md) able to order tags at all.

## Where it fits here

The most complete in-cluster build example in this repository, and the one to read for the
mechanics — context, credentials, cache repository, namespace isolation. Read it alongside the
maintenance note: the shape is correct and durable, the executor is the part to replace.

---

[← Building inside Kubernetes](../README.md)
