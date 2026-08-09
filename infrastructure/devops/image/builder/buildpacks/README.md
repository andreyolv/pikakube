[← Builders](../README.md)

# Buildpacks

<https://github.com/GoogleCloudPlatform/buildpacks>

---

## The problem it solves

**Producing an image with no Dockerfile.** Cloud Native Buildpacks inspect a source tree, detect
what it is, and build an image from it — the platform owns how images are constructed, not each
application team.

The build is two phases:

| Phase | What happens |
|---|---|
| **Detect** | each buildpack is asked "can I handle this source?" — a `requirements.txt` means Python, a `pom.xml` means Java |
| **Build** | the matching buildpacks contribute layers: runtime, dependencies, the application |

The output is an OCI image built on a **stack** — a build base and a run base defined centrally.

The property that justifies all of it is **rebase**. Because the runtime layers and the
application layers are separate and recorded in metadata, a new base image can be swapped
underneath an existing image **without rebuilding the application**. When a base-image CVE is
announced:

| | **Dockerfile per repository** | **Buildpacks** |
|---|---|---|
| The fix | edit `FROM` in every repository | update the stack once |
| Effort at 50 services | 50 pull requests, and a month of chasing | one change, and a rebase |
| Consistency | whatever each team wrote | identical by construction |
| Who needs to act | every application team | the platform team |

This is fleet maintenance, not developer convenience, and it is the only argument for buildpacks
that survives contact with a team that likes writing Dockerfiles.

## When to use it

- **many similar services** — a dozen or more, in a handful of languages, where per-repository
  Dockerfiles have become a maintenance burden
- when base-image patching must be a **platform** action rather than a campaign
- as an internal platform offering: developers push source, the platform produces an image
- with [kpack](../../builder-k8s/kpack/README.md), which turns rebase into something a controller
  does automatically when the stack changes
- where reproducible, consistently structured images matter more than control over the details

## When not to use it

- **a handful of services** — the maintenance benefit does not exist yet and the abstraction costs
  more than it saves
- builds with unusual requirements: system libraries, custom compilation steps, odd runtime
  layouts. There are escape hatches, and they are more work than a Dockerfile would have been
- where teams need to see and control exactly what is in the image
- where an existing Dockerfile estate works and nothing is actually hurting
- for anything that is not an application: sidecars, tools, base images

## Notes

Recorded link:

- <https://github.com/GoogleCloudPlatform/buildpacks> — **Google's** buildpacks, the ones used by
  Cloud Run, App Engine flexible and Cloud Functions. Worth being precise about what this is,
  because "buildpacks" names three different things:

| Thing | What it is |
|---|---|
| **Cloud Native Buildpacks** | the CNCF specification — lifecycle, buildpack, builder, stack |
| `pack` | the reference CLI that runs a build locally |
| **GoogleCloudPlatform/buildpacks** | Google's *implementation* — a specific set of buildpacks and builders |

Google's set is the one recorded here. It covers Go, Java, Node.js, Python, Ruby, PHP and .NET,
and it is the same one that runs behind Cloud Run — which is a useful property in itself: an image
built locally with these buildpacks is built the same way Google's platform would build it. The
alternatives in the same space are Paketo Buildpacks (the CNCF-community set, and the one
[kpack](../../builder-k8s/kpack/README.md) is most often used with) and Heroku's original
buildpacks, which predate the specification.

The relationship with kpack is the one that matters here: buildpacks define **how** an image is
built, and kpack is a Kubernetes controller that decides **when** — including rebuilding
automatically when the stack or the buildpacks change. Buildpacks without kpack means running
`pack build` in CI, which works and gives up the automatic-rebase property that was the reason to
adopt them.

## Where it fits here

Documented as an alternative to the Dockerfile model. The deployed-side counterpart is
[kpack](../../builder-k8s/kpack/README.md) in [`builder-k8s/`](../../builder-k8s/README.md), which
is where buildpacks become interesting for a platform rather than for one build.

For this repository, at its current size, a Dockerfile plus [hadolint](../docker/hadolint/README.md)
is the proportionate answer. The threshold to watch for is the one in
[§3 of the parent](../README.md#3-dockerfile-or-no-dockerfile): when a base-image CVE means
opening pull requests in more repositories than anyone wants to count.

---

[← Builders](../README.md)
