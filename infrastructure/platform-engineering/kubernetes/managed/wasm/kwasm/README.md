[← WASM](../README.md)

# KWasm

<https://github.com/KWasm/kwasm-operator>

---

## The problem it solves

Kubernetes nodes cannot run WebAssembly workloads out of the box. The node needs a Wasm shim —
`runwasi`, or `crun` built with WasmEdge — installed alongside containerd, containerd's configuration
updated to register it, and a `RuntimeClass` created so pods can select it.

KWasm automates that. Label a node, and its operator schedules a job that installs the shim, patches
the containerd configuration and restarts it. It is the prerequisite for
[SpinKube](../spinkube/README.md) and [wasmCloud](../wasmcloud/README.md), which assume a node that
can already run Wasm.

## When to use it

- Preparing nodes for Wasm workloads without building custom node images
- Trialling Wasm on an existing cluster, where rebuilding nodes is disproportionate
- Managed clusters, where you do not control the node image

## When not to use it

- Production, without understanding exactly what it changes on each node — see below
- Where node images can be built properly instead; baking the shim into the image with
  [Packer](../../virtual-machine/packer/README.md) is cleaner and reproducible
- Clusters where a privileged, node-modifying DaemonSet is not acceptable
- If the provider's node upgrades will silently undo it and nobody has planned for that

## Notes

**Chart** from the project's Helm repository, with a namespace manifest and empty values. Recorded as
a link only.

**What it actually does, stated plainly**, because this is the entry in the folder that deserves
scrutiny:

- It runs **privileged pods on your nodes**
- It writes to the **host filesystem** to install the runtime shim
- It modifies **containerd's configuration**
- It **restarts containerd**

Restarting the container runtime on a node is not a small operation. It is the mechanism by which
every container on that node is managed. The install is designed to be safe and it is still a change
to the most critical component on the machine, performed by a controller reacting to a label.

**Three consequences worth planning for:**

- **Node upgrades undo it.** On a managed cluster, replacing a node gives you a fresh node image
  without the shim. The operator reinstalls when the node is labelled again, which is the design —
  but there is a window during which pods requiring the `RuntimeClass` cannot start.
- **A failed install can leave containerd misconfigured**, and a node whose container runtime will
  not start is a node that is not coming back on its own.
- **It is a cluster-wide privilege.** Anything able to label nodes can trigger privileged
  modification of them.

**The better long-term answer**, if Wasm proves itself, is to bake the shim into the node image —
which puts the problem in [`virtual-machine/packer/`](../../virtual-machine/packer/README.md) and
[`on-premise/provision/`](../../../on-premise/provision/README.md), where node composition belongs.
KWasm is the right tool for finding out whether Wasm is worth it; it is not obviously the right tool
for having decided that it is.

---

[← WASM](../README.md)
