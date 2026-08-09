[← Admission policies](../README.md)

# Kubewarden

<https://github.com/kubewarden/kubewarden-controller>
<https://github.com/kubewarden/helm-charts>

Policy engine where policies are **WebAssembly modules** distributed as OCI artifacts. Write them in
any language that compiles to Wasm, ship them like container images.

---

## The problem it solves

The other engines in this folder each impose a language: [Kyverno](../kyverno/README.md) uses YAML
with JMESPath, [Gatekeeper](../gatekeeper/README.md) uses Rego. Both are domain-specific, both have
a ceiling, and both mean a team that already writes Go or Rust has to learn something else to
express a policy.

Kubewarden's answer: a policy is a Wasm module implementing a small ABI — it receives the admission
request as JSON and returns an accept/reject/mutate response. What produced that module is your
problem, not the engine's.

| Consequence | Why it matters |
|---|---|
| Any language with a Wasm target | Rust and Go are the mainstream choices; there are SDKs for both |
| **Rego runs too** | OPA and Gatekeeper policies compile to Wasm, so existing Rego is not thrown away |
| Policies are OCI artifacts | pushed to a registry, pulled by digest, signed with cosign, scanned — the same supply chain as images |
| Versioned and immutable | a policy is a digest, not a YAML file someone edited in place |
| Sandboxed by construction | Wasm has no filesystem or network unless the host grants it; a policy cannot phone home |

That third row is the genuinely distinctive one. In Kyverno and Gatekeeper, a policy is cluster
configuration; in Kubewarden it is an **artifact with a supply chain**. You can require that a
policy be signed before it runs, which is a property the other two do not have.

The architecture is a controller plus one or more `PolicyServer` deployments. Policies are assigned
to a policy server, and each server hosts many Wasm modules. That gives isolation options the others
lack: an untrusted or expensive policy can be given its own server, so its resource use and blast
radius are bounded.

The resource types:

| CRD | Scope |
|---|---|
| `ClusterAdmissionPolicy` | cluster-wide |
| `AdmissionPolicy` | one namespace — so a tenant can own policies for their own namespace |
| `PolicyServer` | where policies run |
| `AdmissionPolicyGroup` / `ClusterAdmissionPolicyGroup` | several policies evaluated together with a boolean expression |

Namespaced policies are a real differentiator for multi-tenancy: a team can add rules for its own
namespace without cluster-admin.

## When to use it

- **Policy authors already have a language.** A team fluent in Rust or Go can write, unit-test and
  debug a policy with their normal tooling — a test framework, a debugger, a type checker. None of
  that exists for JMESPath in YAML.
- **You want policies to be signed, versioned artifacts.** If the platform already enforces signed
  images, extending that to policies is coherent, and only Kubewarden makes it natural.
- **You are migrating from Gatekeeper but keeping the Rego.** Existing policies compile to Wasm.
- **Tenants should own namespace-scoped policies.** `AdmissionPolicy` is namespaced; Kyverno's
  `Policy` is too, but Gatekeeper's constraints are not.
- **Policy isolation matters.** Separate `PolicyServer` instances bound the effect of a slow or
  buggy policy on the admission path.
- **You need a policy the other engines cannot express.** Arbitrary code with a real standard
  library beats a DSL when the logic is genuinely complicated — parsing a certificate, validating a
  domain-specific config format, arithmetic that JMESPath will not do.

## When not to use it

- **You want to require a label.** The overwhelming majority of real admission policies are simple,
  and for those the Kyverno version is three lines of YAML that anyone can read and change. Reaching
  for a compiled artifact to express "no `:latest`" is a large amount of machinery for a small
  amount of policy.
- **Nobody wants to run a build pipeline for policies.** This is the honest cost. A policy change
  means: edit the source, compile to Wasm, push to a registry, update the digest in the CRD.
  Compared to editing a YAML file and letting Flux reconcile it, that is a different workflow with
  different tooling and a different review cycle.
- **You need `generate`.** Kubewarden validates and mutates. It cannot create a NetworkPolicy per
  namespace or clone a Secret. That is Kyverno's, and it is often the more valuable capability.
- **Ecosystem size matters.** The Kyverno policy library and the gatekeeper-library are both large
  and mature. Kubewarden's `policy-hub` is smaller. For common requirements you will be writing what
  someone else has already published elsewhere.
- **Another engine is already deployed.** Two admission webhooks means twice the latency on every
  write and twice the failure surface. Pick one.
- **The team is small.** Three policy languages in one platform is a maintenance problem; the one
  that survives is the one the most people can edit.

## Notes

The original `doc.md` contained only the two repository links, which are at the top of this file.
What follows is the state of the deployment in this folder.

### How it is deployed here

`helm/helmrelease.yaml` contains **two** HelmReleases in one file, which is the correct pattern for
this chart family:

| Release | Chart | Version | Note |
|---|---|---|---|
| `kubewarden` (first document) | `kubewarden-crds` | 1.4.4 | `upgrade.crds: CreateReplace` |
| `kubewarden` (second document) | `kubewarden-controller` | 2.0.5 | `dependsOn: kubewarden-crds` |

Splitting CRDs into their own chart is deliberate on Kubewarden's part: Helm does not upgrade CRDs
from the `crds/` directory, so a separate release with `CreateReplace` is the only way to keep them
current through a GitOps flow.

Two things to be aware of in this file as written:

- Both HelmRelease objects are named `kubewarden` in the namespace `kubewarden`, while the second
  declares `dependsOn: {name: kubewarden-crds}`. A `dependsOn` refers to a HelmRelease *object*
  name, and no object with that name exists here — the first one is named `kubewarden`. Applied as
  is, the two releases also collide on name.
- Neither release sets any values, and no `PolicyServer` or policy is defined anywhere in the
  folder. The controller would install and then have nothing to do.

This is an evaluation stub rather than a deployment, and reading it that way is the point: Kubewarden
is here so the WebAssembly approach is documented and comparable, not because it is in the delivery
path. [Kyverno](../kyverno/README.md) is the engine that is actually wired up in this repo.

### If it were to be adopted

The minimum beyond what exists here: a `PolicyServer`, at least one `ClusterAdmissionPolicy`
referencing a Wasm module by OCI reference and digest, and a decision on `failurePolicy` with the
mitigations in [`../README.md`](../README.md#how-to-survive-either-choice) — Kubewarden has exactly
the same webhook availability problem as every other engine here.

---

[← Admission policies](../README.md)
