[← Operators](../README.md)

# Operator Framework

<https://github.com/operator-framework/operator-sdk>
<https://github.com/operator-framework/operator-lifecycle-manager>
<https://github.com/operator-framework/operator-controller>

---

## The problem it solves

Three separate projects are recorded here under one name, and keeping them distinct is the point of
this page — they are routinely discussed as a single thing and they solve different problems.

| Project | Problem it solves |
|---|---|
| **Operator SDK** | *writing* an operator — scaffolding, in Go, Ansible or Helm |
| **Operator Lifecycle Manager (OLM)** | *installing and upgrading* operators — catalogs, channels, dependency resolution |
| **operator-controller** | OLM v1 — a rebuilt, simpler successor to OLM |

The SDK overlaps heavily with [Kubebuilder](../kubebuilder/README.md); the distinctive part of this
family is **OLM**. It treats operators as installable packages with versions, upgrade channels and
dependencies — a package manager for cluster extensions — which is what makes an operator
distributable to people who did not write it. OperatorHub is built on it, and OpenShift ships it.

## When to use it

- Publishing an operator for others to install, with upgrade channels and a catalog
- OpenShift environments, where OLM is the native installation path
- Operators whose logic is genuinely Ansible or Helm, which the SDK supports as first-class options
- Managing many third-party operators and wanting declarative version and dependency control

## When not to use it

- A single internal operator you install yourself — OLM is a whole subsystem to run for no benefit
- Where GitOps already installs everything; OLM's dependency resolution overlaps and can conflict
- If your team writes Python — [Kopf](../kopf/README.md), and neither of these
- Adopting OLM v0 today without checking where operator-controller (v1) has got to

## Notes

The recorded note is three links with no commentary, which understates how different the three are.
Their relationship:

- **Operator SDK** is the developer tool. Its Go path is Kubebuilder with extra commands for
  generating OLM bundles. Its **Helm** and **Ansible** paths are genuinely distinctive: an operator
  whose reconcile logic is a Helm chart or an Ansible role, with no Go at all. For wrapping an
  existing chart in a CRD, that is a real shortcut.
- **OLM** is the cluster-side runtime. It introduces `Subscription`, `ClusterServiceVersion` and
  `CatalogSource`, resolves dependencies between operators, and performs upgrades along channels.
  Powerful, and a substantial system in its own right.
- **operator-controller** is the OLM v1 rewrite. OLM v0's dependency resolution and upgrade semantics
  proved hard to reason about; v1 deliberately narrows the scope. Anyone evaluating OLM today should
  look at which version is current before building on v0.

**The tension with GitOps is worth stating**, because it is the usual reason not to adopt OLM in a
repository like this one: OLM decides *when* an operator upgrades, based on channels and its own
resolution. Flux decides when things change, based on Git. Two systems owning the same lifecycle is a
recipe for surprises, and in a Flux-driven repository the plain `HelmRelease` path is simpler and
more predictable.

Recorded as links only — none of the three is deployed here.

---

[← Operators](../README.md)
