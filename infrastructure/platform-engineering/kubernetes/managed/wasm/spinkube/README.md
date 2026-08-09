[← WASM](../README.md)

# SpinKube

<https://github.com/spinkube/spin-operator>

---

## The problem it solves

SpinKube runs **Spin** applications — Fermyon's WebAssembly framework — as first-class Kubernetes
workloads. A `SpinApp` custom resource points at a Wasm application packaged as an OCI artifact; the
operator creates the Deployment, Service and `RuntimeClass` reference needed to run it.

Spin's model is request-driven: a component is invoked per HTTP request or per event, executes in
milliseconds, and exits. Combined with Wasm's near-instant cold start, that makes **scale to zero**
practical in a way containers cannot match — the delay between a request arriving at nothing and
being served is small enough not to matter.

## When to use it

- Event-driven or HTTP handler workloads that should cost nothing when idle
- Rust, Go, JavaScript or Python components targeting the Spin SDK
- You want Wasm workloads declared as Kubernetes objects under GitOps
- The scale-to-zero economics genuinely apply — many idle endpoints, spiky traffic

## When not to use it

- Long-running or stateful services; the execution model is short-lived by design
- Applications not written against Spin — this is framework-specific, not a general Wasm runtime
- Before the nodes can run Wasm at all; [KWasm](../kwasm/README.md) or a custom node image comes first
- Where the observability and debugging story matters more than the cold-start win

## Notes

**Installed from an `OCIRepository`**, with a namespace manifest and empty values. Recorded as a link
only.

**The `SpinApp` CRD is the interface**, and the operator's job is unglamorous and useful: translate
that resource into the ordinary Kubernetes objects that run it, including the `RuntimeClass`
reference that routes the pod to the Wasm shim rather than to the default runtime. The developer
writes a `SpinApp`; the cluster runs a pod.

**Two dependencies to be explicit about:**

- **Nodes must already run Wasm.** SpinKube does not prepare them. That is
  [KWasm](../kwasm/README.md), or a node image with the shim baked in.
- **Applications must be Spin applications.** This is not a generic Wasm workload runner — it runs
  applications built with the Spin SDK and packaged Spin's way. That coupling is the price of the
  developer experience.

**The scale-to-zero claim is the thing to evaluate**, and it is the strongest argument for the whole
category. Kubernetes can already scale a Deployment to zero; what it cannot do is bring it back
quickly enough for the first request to be served without a visible delay. Wasm's millisecond cold
start removes that objection. If a platform has many endpoints that are idle most of the time, that
is a real saving with no user-visible cost — and it is a much more concrete argument than the general
enthusiasm this area usually generates.

**Fermyon** is behind Spin, and the position paper recorded in the
[parent](../README.md) —
<https://www.fermyon.com/blog/rethinking-microservices> — is theirs. Worth reading, and worth reading
as advocacy.

---

[← WASM](../README.md)
