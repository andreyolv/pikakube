[← Builders](../README.md)

# Podman

<https://github.com/containers/podman>

---

## The problem it solves

**A container engine with no daemon.** Podman runs containers as ordinary child processes of the
user's shell, using the same libraries as [Buildah](../buildah/README.md), skopeo and CRI-O. There
is no root service listening on a socket, so there is nothing to escalate through.

The reason it is easy to adopt is the CLI: it is deliberately compatible, so `alias docker=podman`
gets most people through the day. `podman build` is Buildah underneath; `podman run`, `ps`,
`images`, `push` all behave as expected.

What it adds beyond compatibility:

| Feature | Detail |
|---|---|
| **Rootless by default** | containers run as your user, in a user namespace |
| No daemon | nothing to start, nothing running when you are not using it |
| **Pods** | it groups containers into pods, the Kubernetes concept, natively |
| `podman generate kube` | emits Kubernetes YAML from running containers |
| `podman play kube` | runs a Kubernetes manifest locally |
| systemd integration | containers as user services, via Quadlet |
| No licence question | Apache 2.0, and no equivalent of Docker Desktop's commercial terms |

## When to use it

- **as a local alternative to Docker Desktop**, particularly where its licensing is a problem
- on Fedora, RHEL and derivatives, where it is the default and Docker is the awkward one
- when rootless containers on a shared development machine are a requirement
- for `podman play kube` / `generate kube`, which shorten the loop between local containers and
  Kubernetes manifests
- as a systemd-managed container runtime on a single server, where a daemon adds nothing

## When not to use it

- **in CI/CD** — see the note below; there is no advantage over the alternatives there
- where Compose is deeply relied upon: `podman-compose` exists and is not as smooth as the real
  thing
- where the surrounding tooling assumes a Docker socket — Testcontainers, some IDE integrations,
  and anything that talks to `/var/run/docker.sock` directly
- as an in-cluster builder; that is [Buildah](../buildah/README.md) or
  [BuildKit](../buildkit/README.md) directly

## Notes

Recorded, in full:

> No advantage for CI/CD.
>
> Good for running locally on the machine, as an alternative to Docker Desktop.

That is a sharper verdict than it first looks, and it is right.

**Why there is no CI/CD advantage.** The property that matters in CI is building without root and
without a daemon. Podman gets that from Buildah, which is already usable directly — so in a
pipeline, `buildah bud` does the same job with one less layer of tooling. And in Kubernetes,
running Podman inside a pod hits the same nested-container problems as anything else; the tools
designed for that case ([Kaniko](../../builder-k8s/kaniko/README.md), BuildKit rootless, Buildah)
solve it more directly. Podman's strengths — an interactive CLI, pod grouping, systemd units — are
all about a human at a terminal, and CI has no human at a terminal.

**Why it is good locally.** Docker Desktop requires a paid subscription for larger organisations,
and its VM is heavy. Podman gives the same commands with no daemon, no licence question, rootless
by default, and `podman play kube` as a genuinely useful extra when the target is Kubernetes
anyway.

The one thing to check before switching a team over is the socket dependency: tools like
Testcontainers expect `/var/run/docker.sock`. Podman can expose a compatible socket, which usually
works, and "usually" is the operative word.

## Where it fits here

Documented as a local-machine choice. In this repository the cluster-side builders are
[`builder-k8s/`](../../builder-k8s/README.md), and Podman is not among them by design — the
recorded verdict is exactly why.

---

[← Builders](../README.md)
