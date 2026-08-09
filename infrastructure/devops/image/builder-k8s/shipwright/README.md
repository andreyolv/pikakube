[← Building inside Kubernetes](../README.md)

# Shipwright

<https://github.com/shipwright-io/build>
<https://github.com/shipwright-io/operator>

---

## The problem it solves

**One Kubernetes API in front of every builder.** Shipwright does not build anything itself; it
defines a `Build` resource and a set of `BuildStrategy` resources, and delegates the actual work
to [Kaniko](../kaniko/README.md), [Buildah](../../builder/buildah/README.md),
[BuildKit](../../builder/buildkit/README.md), [buildpacks](../../builder/buildpacks/README.md) or
anything else that can be expressed as a strategy.

| CRD | What it declares |
|---|---|
| **`ClusterBuildStrategy` / `BuildStrategy`** | *how* to build — the steps, as a template; one per tool |
| **`Build`** | *what* to build — source, strategy, output image, parameters |
| **`BuildRun`** | one execution of a `Build` |

Underneath, the steps run as a Tekton `TaskRun`.

Why the indirection is worth anything:

- **the builder becomes a configuration value.** Migrating from Kaniko to Buildah is a change of
  `strategy`, not a rewrite of every pipeline — which matters a great deal given
  [Kaniko's maintenance status](../kaniko/README.md)
- **several strategies coexist** behind one API, so a team that needs a Dockerfile and a team that
  wants buildpacks use the same resource
- **the platform owns the strategy**, so cluster-wide constraints — resource limits, the exact
  builder version, security context — are applied once, centrally, rather than copied into every
  build pod

## When to use it

- when **more than one build tool** must coexist and should look the same to users
- when the underlying builder is expected to change and the pipelines should not have to
- where a self-service build API is being offered to teams, and per-team pod manifests are not
  acceptable
- **where Tekton is already deployed**, which removes most of the adoption cost

## When not to use it

- **where Tekton is not already there** — Shipwright requires it, and installing a pipeline engine
  to run one build is a large amount of machinery for a job a single Kaniko or Buildah pod does
- for a small number of builds with one tool: the abstraction has nothing to abstract over
- where the CI system already runs builds well and the cluster is not meant to
- if a compact, self-contained setup is the goal; this is the opposite of that

## Notes

Recorded links:

- <https://github.com/shipwright-io/build> — the build controller and the CRDs. This is the
  project proper.
- <https://github.com/shipwright-io/operator> — the operator that installs and manages it,
  including its Tekton dependency. The usual route in for an OpenShift or OLM-based cluster.
- <https://artifacthub.io/packages/olm/community-operators/shipwright-operator> — the operator
  packaged for OLM, the Operator Lifecycle Manager. Worth naming the consequence: the primary
  distribution is **OLM**, not Helm, which is a slight friction in a Flux repository where
  everything else is a `HelmRelease`. Installing the plain manifests and pinning the version is
  the alternative.

Shipwright is a CNCF Sandbox project. Development is steady but not fast, and the ecosystem around
it is small compared with Tekton's — which is the honest counterweight to the flexibility argument.

The strategic point it makes is a good one regardless of whether the tool is adopted: **the build
engine should be a replaceable detail**. Any in-cluster build setup that hard-codes one executor
into every pipeline will have to be rewritten when that executor stops being maintained, which is
precisely the situation the Kaniko examples in this repository are in.

## Where it fits here

References only — no manifests, and nothing deployed. It is the third option in
[`builder-k8s/`](../README.md) and the heaviest by a wide margin, because of the Tekton
prerequisite.

For this repository, a single [Kaniko](../kaniko/README.md) pod — or its Buildah/BuildKit
successor — is the proportionate answer. Shipwright becomes interesting only if several teams need
different build styles behind one interface, and Tekton is running anyway.

---

[← Building inside Kubernetes](../README.md)
