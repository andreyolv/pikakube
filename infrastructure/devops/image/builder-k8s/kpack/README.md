[← Building inside Kubernetes](../README.md)

# kpack

<https://github.com/buildpacks-community/kpack>

---

## The problem it solves

**A Kubernetes controller that keeps images built and up to date**, using
[Cloud Native Buildpacks](../../builder/buildpacks/README.md) rather than Dockerfiles.

The distinctive part is not building. It is **rebuilding**. An `Image` resource declares "this
source, built with this builder, pushed to this tag", and the controller keeps that true. It
rebuilds when:

| Trigger | Consequence |
|---|---|
| The source changes | a new commit produces a new image, without a pipeline |
| **The buildpacks change** | a language runtime fix reaches every image using it |
| **The stack — the base image — changes** | **a base-image CVE is patched across the whole fleet** |

That third row is the reason kpack exists. With a Dockerfile per repository, a base-image CVE is a
pull request in every repository and weeks of chasing. With kpack, updating the stack causes the
controller to rebuild — or rebase, which does not even re-run the build — every affected image
automatically.

The resource model:

| CRD | What it declares |
|---|---|
| `ClusterStore` | the available buildpacks |
| `ClusterStack` | the build and run base images |
| `Builder` / `ClusterBuilder` | a combination of store and stack, ordered |
| **`Image`** | source + builder + destination tag; the thing you actually create |
| `Build` | one execution, created by the controller, not by you |

## When to use it

- **many services in a few languages**, where per-repository Dockerfiles have become a burden
- when base-image patching must be a platform action rather than a campaign across teams
- as the build half of an internal developer platform: teams push source, images appear
- where reproducible and consistently structured images matter more than fine control
- in a GitOps setup — an `Image` resource is desired state, reconciled by a controller, which is
  the same model as everything else in the cluster

## When not to use it

- **a handful of services** — the fleet-maintenance benefit is the whole benefit, and it does not
  exist yet
- where builds need Dockerfile-level control: system packages, custom compilation, unusual layouts
- where an existing Dockerfile estate works and nothing is hurting
- for anything that is not an application — sidecars, tools, base images
- if the team is unwilling to own a builder, a stack and a store as platform artefacts; kpack is a
  platform commitment, not a build command

## Notes

Recorded link:

- <https://github.com/buildpacks-community/kpack> — the project. The organisation name matters:
  kpack began at Pivotal/VMware and now sits under `buildpacks-community`, which is community
  stewardship rather than a vendor roadmap. Activity is steady rather than fast; check the release
  cadence before committing a platform to it.

What is in this folder:

| File | What it is |
|---|---|
| `release-0.11.5.yaml` | the pinned kpack release manifest — CRDs, controller and webhook |
| `serviceaccount.yaml` | `tutorial-service-account` in the `kpack` namespace, referencing `registry-credentials` both as `secrets` and as `imagePullSecrets` |
| `registry-credentials.yaml` | a `kubernetes.io/dockerconfigjson` secret with the value redacted as `xxxxxxxxxx` |

The service account is the piece worth understanding, because it is where builds usually fail
first. kpack builds **as** that service account, and it needs the registry credential in two
roles: as `secrets`, so the build can **push** the result, and as `imagePullSecrets`, so the pods
can **pull** the builder and stack images. Getting one and not the other produces an error that
does not obviously point at the cause.

The release manifest being pinned to a version rather than tracking `latest` is the right
instinct, and it is also the awkward part of adopting kpack in a Flux repository: the upstream
distribution is a plain manifest bundle rather than a Helm chart, so upgrades mean replacing the
file rather than bumping a chart version.

The redacted secret is correct — a real `dockerconfigjson` in Git is a published credential. The
proper handling for this repository is a sealed or externally sourced secret rather than a
placeholder that has to be filled in by hand at apply time.

## Where it fits here

Mapped as the buildpack-based alternative to [Kaniko](../kaniko/README.md), and the two are not
really competing: Kaniko builds a Dockerfile when asked; kpack owns a set of images continuously.

For this repository, at its current size, Kaniko or a Dockerfile build is proportionate. The
threshold for kpack is the one in
[§3 of `builder/`](../../builder/README.md#3-dockerfile-or-no-dockerfile): the point at which a
base-image CVE means opening more pull requests than anyone wants to count.

---

[← Building inside Kubernetes](../README.md)
