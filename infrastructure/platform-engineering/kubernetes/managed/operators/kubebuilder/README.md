[← Operators](../README.md)

# Kubebuilder

<https://github.com/kubernetes-sigs/kubebuilder>

---

## The problem it solves

The standard way to write a Kubernetes operator in Go. Kubebuilder scaffolds a project, generates
API types, CRD manifests, RBAC rules and controller stubs from marker comments in your Go code, and
wires everything to `controller-runtime` — the same library the built-in controllers use.

The generation is the value. Change a Go struct and the CRD schema regenerates; add an RBAC marker
above a function and the Role regenerates. Keeping those three artifacts consistent by hand is where
hand-written operators go wrong.

It is a `kubernetes-sigs` project and effectively the reference toolchain.

## When to use it

- Writing an operator in Go, which is the mainstream choice
- Internal operators where you control distribution and do not need OLM
- You want the same foundations the Kubernetes project itself uses
- Envtest-based controller testing matters — it is built in

## When not to use it

- The team does not write Go; [Kopf](../kopf/README.md) exists for exactly that
- You need OLM packaging and upgrade channels — [Operator SDK](../operator-framework/README.md) adds that on top
- The requirement is templating rather than reconciliation
- For a one-off task; the scaffold implies a project you will maintain

## Notes

Recorded as a link only:

```
https://github.com/kubernetes-sigs/kubebuilder
```

Known, not used — consistent with [Kopf](../kopf/README.md) being the framework this repository
actually built with.

Worth understanding regardless, because **Kubebuilder and Operator SDK are not really competitors**.
Both generate `controller-runtime` projects with near-identical layouts. The SDK is approximately
Kubebuilder plus OLM bundle generation, plus non-Go options (Ansible, Helm). A project started with
one can largely be understood by someone who knows the other.

Three things about the toolchain that are not obvious from the README:

- **Markers drive everything.** `// +kubebuilder:validation:...` on a struct field becomes OpenAPI
  validation in the CRD; `// +kubebuilder:rbac:...` above the reconciler becomes the Role. Learning
  the marker vocabulary is most of learning Kubebuilder.
- **`envtest` runs a real API server and etcd** for tests, without a cluster. That is the single
  biggest practical advantage over rolling your own controller, and it is what makes reconcile logic
  testable at all.
- **The book is the documentation.** The Kubebuilder Book is genuinely the reference for
  `controller-runtime` as a whole, useful even when writing controllers without the scaffolding.

---

[← Operators](../README.md)
