# Kubernetes Manifest and CRD Validation in CI with flux-schema

## Problem:
- Custom Resources Validated by Nothing: In a GitOps platform, most manifests are not core Kubernetes objects — they are `HelmRelease`, `OCIRepository`, `Kustomization` and the CRDs of every operator installed in the cluster. Conventional schema validators only know the built-in API surface, and **skip every custom resource they have no schema for silently, reporting success**. The pipeline is green, the coverage claim is false, and nobody is told.

- The Cluster as the First Validator: Without a CI gate, the API server is the first thing that ever reads the manifest. A typo or a wrong `apiVersion` is discovered at apply time, which in a GitOps setup means a reconciliation error surfacing minutes after merge, in a controller log nobody is watching.

- Silent Field Drops: A misspelled field such as `resources.limits.memroy` is not an error to most tooling. Rule-based scanners deserialize manifests into typed objects and discard what they do not recognize, so the check passes, the manifest applies, and the setting simply never takes effect.

- Errors That Are Structurally Valid: A `HelmRelease` whose `chartRef` points at a source kind that is not installed, or an interval shorter than the timeout beneath it, satisfies every JSON Schema and still fails at reconcile time. Schema describes the shape of one field; it cannot describe a relationship between two.

- Validating the Wrong Artifact, at the Wrong Version: Helm charts and Kustomize overlays are not manifests. Validating the templated source either fails to parse or checks something the cluster will never see — and validation not pinned to the target Kubernetes release happily approves objects using an API that release has removed.

## Solution:
- Schema Validation That Covers CRDs: Adopted `flux-schema`, the validator maintained by the Flux project, whose built-in catalog covers Kubernetes, OpenShift, Gateway API and the Flux ecosystem CRDs. This closes the gap that defines the problem — the resources this platform is actually made of are validated, instead of being skipped by a tool that reports success either way.

- Ecosystem Schema Catalog for Operator CRDs: Extended coverage to the wider CNCF ecosystem — Crossplane, Cluster API, Cilium, Istio, Prometheus Operator, cert-manager and the rest — through the hosted catalog of roughly 118 projects, regenerated daily from upstream releases, so operator CRDs are validated without maintaining a schema list by hand.

- Deliberate Choice Between Hosted and Embedded Catalog: Treated schema resolution as a dependency decision rather than a flag copied from an example. The hosted catalog keeps schemas current and puts a CDN in the CI path; the container image ships the catalog embedded, which is the answer for an air-gapped or reproducibility-sensitive pipeline. The licence differs from the CLI's — the tool is Apache-2.0 and the catalog is AGPL-3.0 — which is checked before adoption rather than discovered later.

- Rules Beyond Schema with CEL: Used CEL expressions to catch the class of error that is structurally valid and still wrong — a `HelmRelease` referencing a source kind that is not deployed, an interval shorter than the timeout, a field required only when another field holds a particular value. These are precisely the manifests that pass every schema check and fail at reconcile time.

- Render Before Validating: Expanded Helm charts and Kustomize overlays into concrete manifests first, and pointed validation at that output rather than at the source. This is the most common design error in manifest pipelines and the reason validators appear to work while checking nothing meaningful.

- Version Pinned to the Cluster: Pinned the target Kubernetes version to the release actually running, and bumped it as part of the cluster upgrade process, so removed and deprecated APIs are reported by CI before an upgrade rather than by the API server after it.

- Fast Feedback on Changed Paths: Scoped validation to the paths a pull request touches instead of walking the entire tree on every run — a repository of roughly 1,700 manifests otherwise revalidates in full for a one-file change. The CLI accepts explicit paths, so the pipeline computes the changed set and passes it through, keeping pull request feedback in seconds.

- Layered Gates Around It: Kept schema validation as one stage in an ordered pipeline — YAML parsing first, schema conformance second, then reliability and security opinions, then organizational policy executed by the same engine that enforces it at admission. Each stage is a replaceable implementation behind a stable contract of input, exit code and report format, so a deprecated tool is swapped without redesigning the pipeline.

- Shift-Left Parity and Progressive Enforcement: Ran the cheap deterministic stages as pre-commit hooks so developers see locally the same failure CI would produce, introduced each new gate in report-only mode, quantified and remediated the existing backlog, and only then promoted it to a required status check, with findings published as inline comments on the changed lines rather than as walls of text in job logs.

## Skills:
- DevOps
- Platform Engineering
- CI/CD

## Tools:
- flux-schema
- Flux
- Kubernetes
- Helm
- Kustomize
- Github Actions
- pre-commit
