[← WASM](../README.md)

# wasmCloud

<https://github.com/wasmCloud/wasmCloud>

---

## The problem it solves

wasmCloud is the most ambitious project in this folder and the least Kubernetes-shaped. It is a
distributed **actor platform**: business logic is written as Wasm components with no knowledge of
where they run or of what provides their capabilities. Access to HTTP, key-value storage, messaging
and so on is supplied at runtime by pluggable **capability providers**, linked to actors by
configuration rather than by imports.

The consequence is that an actor can be written once and run on a laptop, in a cluster, or at an edge
site, with a different key-value provider each time and no change to the code. Its hosts form a
lattice connected over NATS, and actors are placed across that lattice.

It is a CNCF project.

## When to use it

- Genuinely distributed applications spanning cloud and edge
- Where separating business logic from infrastructure capabilities is the actual design goal
- Fleets of small compute locations that should behave as one platform
- Polyglot components communicating through a common interface model

## When not to use it

- Kubernetes-only deployments; the lattice's value is that it spans more than one environment
- Applications not written to its actor and capability model — this is a way of building, not just running
- Where a conventional service architecture already works
- Small teams; the conceptual surface is large

## Notes

**Installed from an `OCIRepository`**, with a namespace manifest and empty values. Recorded as a link
only.

**Kubernetes is one host among several**, and that is the point of the design. wasmCloud runs its
hosts wherever there is compute — a cluster, a VM, a Raspberry Pi at a site — and joins them into a
lattice over NATS. Deploying it into Kubernetes gives you cluster-hosted members of that lattice, not
a Kubernetes-native platform.

Which means it is not really comparable to [SpinKube](../spinkube/README.md), despite both being in
this folder. SpinKube runs Wasm applications as Kubernetes workloads. wasmCloud runs a distributed
platform that happens to be able to live partly in Kubernetes.

**The capability-provider model is the interesting idea, and the coupling.** An actor declares that
it needs key-value storage; a link definition binds that to Redis, or to NATS KV, or to something
else, at deployment time. Genuinely elegant, and it means applications are written against
wasmCloud's interface model rather than against a database client. Portability across providers is
bought with portability away from wasmCloud.

**NATS is a hard dependency** — the lattice is built on it. That is a real infrastructure
requirement, and NATS is documented elsewhere in this repository as a messaging broker in its own
right.

Filed here as a bookmark for a category — distributed edge compute with a component model — that
nothing in this repository currently needs.

---

[← WASM](../README.md)
