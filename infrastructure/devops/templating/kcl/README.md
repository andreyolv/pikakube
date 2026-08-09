[← Manifest templating](../README.md)

# KCL

<https://github.com/kcl-lang/kcl>

<https://github.com/kcl-lang/flux-kcl-controller>

---

## The problem it solves

Every tool in this folder generates YAML. Almost none of them can tell you the YAML is **wrong**
before the API server does.

KCL is a configuration language whose central construct is the **schema**: types, defaults,
constraints and validation rules, checked at compile time. A field that must be one of three
values, a replica count that must be positive, a required annotation — these are declared once
and enforced everywhere the schema is used, and the failure is a compile error with a line number
rather than a rejected apply.

It is a proper language — imports, functions, inheritance, a package manager — but the schema
system is the reason to pick it over the others.

## When to use it

- **Platform teams defining what an application manifest may contain.** A schema is an enforced
  contract; a `values.yaml` is a suggestion.
- **When invalid configuration is expensive.** Anything that fails at apply time in a production
  cluster is worth catching in CI, and that is what constraints buy.
- **Heavy CRD use.** Custom resources have no client-side validation until they hit the API
  server; a KCL schema gives them one.
- **GitOps without a build step**, via the Flux controller below — the one thing on this list that
  no other alternative here offers.

## When not to use it

- **Small configuration.** Defining schemas to generate three manifests is more work than the
  three manifests.
- **When adoption matters.** KCL is young. The community, the examples and the pool of people who
  can review a change are all small compared to Helm or Kustomize, and that is a real operational
  risk for something the cluster depends on.
- **Consuming third-party software.** Vendors ship charts.

## Notes

The recorded links:

| Link | What it is |
|---|---|
| [kcl-lang/kcl](https://github.com/kcl-lang/kcl) | the language and compiler |
| [kcl-lang/flux-kcl-controller](https://github.com/kcl-lang/flux-kcl-controller) | a Flux controller that reconciles KCL sources directly from a Git repository |

**The second link is the interesting one for this repository.** Every other alternative in this
folder requires rendering to YAML in CI and committing or publishing the result, which inserts a
build step into a workflow that currently has none. The KCL controller makes KCL a first-class
Flux source alongside `HelmRelease` and `Kustomization` — the controller compiles it in-cluster
and applies the output.

That makes KCL the only tool documented here that could be **added** to this stack rather than
having to **replace** part of it. Which is a statement about feasibility, not a recommendation:
adding a third source type means a third thing to debug when reconciliation stops, and the
maturity gap against Flux's built-in controllers is significant.

KCL is a CNCF sandbox project. The pitch it shares with [Timoni](../timoni/README.md) —
**validation before apply, and typed configuration** — is the strongest argument any of these
tools make against Helm, and it is the argument to revisit if hand-written YAML ever becomes the
bottleneck here.

---

[← Manifest templating](../README.md)
