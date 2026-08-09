[← Builders](../README.md)

# werf

<https://github.com/werf/werf>

---

## The problem it solves

**Build, publish, deploy and clean up, as one tool driven by Git.** werf is not really a builder;
it is a delivery tool whose build stage happens to be one of its parts. Its position is that
building an image and deploying it are one workflow, and splitting them across a build tool, a
templating tool and a deployment tool creates the gaps that releases fall into.

A single `werf.yaml` describes the images and the Helm chart. `werf converge` then builds whatever
changed, pushes it, renders the chart with the resulting image references already substituted, and
applies it — tracking the rollout until the resources are actually ready rather than merely
accepted.

| Capability | Detail |
|---|---|
| **Git-driven state** | image tags and cache keys are derived from Git content, so identical content is never rebuilt |
| Build | BuildKit or Docker underneath, with its own content-addressable staging |
| **Deploy** | Helm, with rollout tracking and readable failure output |
| **Registry cleanup** | a first-class feature — see below |
| CI integration | designed to be invoked from GitLab CI, GitHub Actions and others |

**The cleanup feature is the distinctive one.** Every CI-driven build pipeline creates a registry
that grows forever, and most teams discover this when storage runs out. `werf cleanup` deletes
images by policy — tied to Git history, so images built from deleted branches and superseded
commits go, while images referenced by live Git refs stay. It is the one tool in this folder that
treats registry retention as part of the delivery loop rather than as somebody else's problem.

## When to use it

- when build and deploy should be **one tool** invoked from a pipeline, rather than three stitched
  together
- when Helm is already the packaging format and its rollout feedback is unsatisfying — werf's
  tracking is materially better at saying *why* a release is stuck
- **when registry growth from CI builds is an actual problem** and nothing is pruning it
- in a GitLab-centric estate, which is the environment werf was designed around

## When not to use it

- **in a GitOps setup** — this is the important one. werf pushes: the pipeline applies to the
  cluster. Flux pulls: the cluster reconciles from Git. Running both means two things deciding
  what is deployed, and they will disagree
- where the build tool should be replaceable; werf is opinionated across the whole pipeline
- for a small setup where a Dockerfile, `helm upgrade` and a retention policy do the job
- where the team has no appetite for another delivery abstraction to learn

## Notes

Recorded links, and what each is for:

- <https://github.com/werf/werf> — the tool. Written in Go, developed by Flant, and open source.
- <https://werf.io/docs/v2/usage/cleanup/cr_cleanup.html> — **container registry cleanup**. The
  policies for deleting images from the registry based on Git history: how many images to keep per
  branch or tag, how old they may be, which Git refs protect an image from deletion. This is the
  documentation that makes the case for werf as a whole, because it addresses the problem in
  [§5 of `oci-registry/`](../../oci-registry/README.md#5-storage-garbage-collection-and-retention)
  directly.
- <https://werf.io/docs/v2/reference/cli/werf_cleanup.html> — the `werf cleanup` command
  reference, which is the CLI side of the same feature.
- <https://werf.io/docs/v2/usage/integration_with_ci_cd_systems.html> — how werf detects and
  integrates with CI systems. It reads CI environment variables to work out the branch, the tag
  and the registry, so the same command behaves correctly in a pipeline without being told.
- <https://werf.io/docs/v2/reference/werf_yaml.html> — the `werf.yaml` reference: image
  definitions, dependencies between them, the Helm chart configuration. This is the file that is
  the whole configuration surface.
- <https://github.com/marketplace/actions/werf> — the GitHub Action, for running it from Actions
  rather than GitLab CI.

The set of links recorded is itself the signal: four of the six are about **cleanup and CI
integration**, not about building. That is the right reading of what werf is for — the build is
the least interesting part of it.

## Where it fits here

Documented as an alternative delivery model, and worth understanding precisely because it is the
opposite of the one this repository uses. This platform reconciles from Git with Flux; werf pushes
from a pipeline. The two are not complementary.

**The idea worth stealing regardless of the tool** is registry cleanup driven by Git history: an
image whose branch no longer exists is an image nobody will deploy, and something should be
deleting it. Whichever registry from [`../../oci-registry/`](../../oci-registry/README.md) is
chosen, that policy needs to exist somewhere.

---

[← Builders](../README.md)
