[← On premise](../README.md)

# Container runtime interface

<https://github.com/containerd/containerd>
<https://github.com/cri-o/cri-o>
<https://github.com/opencontainers/runc>
<https://github.com/containers/crun/>
<https://github.com/youki-dev/youki>
<https://github.com/nestybox/sysbox>
<https://github.com/kuasar-io/kuasar>
<https://github.com/WasmEdge/WasmEdge>
<https://github.com/lima-vm/lima>

---

## The problem it solves

The kubelet does not start containers. It speaks the **Container Runtime Interface** to a high-level
runtime, which manages images, pod sandboxes and container lifecycle, and which in turn calls a
**low-level runtime** that does the actual `clone`, `unshare` and cgroup work.

Two layers, routinely confused:

| Layer | Speaks | Examples |
|---|---|---|
| **High-level (CRI)** | CRI to the kubelet, OCI to the layer below | containerd, CRI-O |
| **Low-level (OCI)** | creates the process, namespaces and cgroups | runc, crun, youki, sysbox |

Knowing which layer a problem is in is most of debugging it. "The image will not pull" is the
high-level runtime; "the container will not start" is frequently the low-level one.

## When to use it

- containerd — the default nearly everywhere, and the right choice absent a reason
- CRI-O — Kubernetes-only by design, minimal surface; the OpenShift default
- crun — a C rewrite of runc: faster startup, lower memory, useful at density
- youki — a Rust implementation of the same interface
- sysbox — when containers must run Docker or systemd inside them, without privileged mode
- Kuasar — a runtime designed to host multiple sandbox types, including VMs and Wasm

## When not to use it

- Changing the runtime on a managed cluster; you do not own the nodes
- Swapping runtimes for performance without measuring — the difference is real and usually small
- sysbox or Kuasar without understanding their constraints; these are specialist choices
- Confusing this with [sandboxing](../container-runtime-sandbox/README.md), which is the next question, not this one

## Notes

The recorded note is a list of nine links with no commentary. Sorting them into layers is most of
what makes the list useful:

**High-level (CRI) runtimes**

- **containerd** — the default for every managed provider and for `kubeadm`. Graduated CNCF project.
- **CRI-O** — built solely to run Kubernetes containers, with no Docker-compatibility surface.
  Red Hat's, and OpenShift's default.

**Low-level (OCI) runtimes**

- **runc** — the reference implementation, in Go; what containerd and CRI-O call by default.
- **crun** — the same interface in C. Materially faster to start and lighter on memory, which shows
  up at high pod density and in short-lived workloads. Also the route to WasmEdge, since crun can be
  built with Wasm support.
- **youki** — a Rust implementation. Younger; the interesting property is memory safety in the
  component that manipulates namespaces and capabilities.
- **sysbox** — the unusual one. It makes containers able to run **Docker, systemd and Kubernetes
  inside them** without `--privileged`, by virtualising parts of `/proc` and `/sys`. That solves the
  Docker-in-Docker problem properly rather than by handing out host access, which makes it genuinely
  interesting for CI.

**Other**

- **Kuasar** — a multi-sandbox runtime: containers, VMs and Wasm behind one runtime, aimed at the
  case where a node must host several isolation models.
- **WasmEdge** — a WebAssembly runtime, reachable through crun. This is where this folder touches
  [`managed/wasm/`](../../managed/wasm/README.md): running a Wasm module as a Kubernetes workload
  means a node whose low-level runtime can execute one.
- **Lima** — Linux VMs on macOS. Not a Kubernetes runtime at all; it is how a Mac gets a Linux VM to
  run containers in, and it belongs to the workstation story rather than to node configuration.

**The practical advice** is short: use containerd unless something specific pushes you elsewhere. The
runtime is not where cluster problems usually are, and changing it introduces a variable in the most
critical component on every node. The reasons that do justify a change — Wasm support, sysbox's
nested-container capability, crun's density gains — are all specific and identifiable in advance.

---

[← On premise](../README.md)
