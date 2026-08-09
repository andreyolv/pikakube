[← Nodes](../README.md)

# node-feature-discovery

<https://github.com/kubernetes-sigs/node-feature-discovery>

---

## The problem it solves

Scheduling constraints are expressed with node labels — `nodeSelector`, node affinity, taints. Which
means hardware capability has to be a label, and if labels are applied by hand, they are wrong within
a month: a node is replaced, a card is moved, someone types `nvida`.

NFD discovers hardware and system capability automatically and labels nodes with it: CPU features
(AVX-512, SGX, specific instruction sets), kernel version and loaded modules, PCI and USB devices
including GPUs and accelerators, memory topology and NUMA, storage characteristics, and operating
system version.

Workloads then select what they need — "a node with AVX-512", "a node with an NVIDIA device" — rather
than a node someone remembered to label.

## When to use it

- Heterogeneous clusters where nodes genuinely differ
- Workloads requiring specific CPU instructions, kernel modules or accelerators
- GPU clusters, as the foundation under device plugins and GPU-aware scheduling
- Anywhere hardware labels are currently maintained by hand

## When not to use it

- Homogeneous clusters where every node is identical; there is nothing to discover
- Managed clusters that already label instance type and capability adequately
- As a device plugin — NFD labels; it does not make devices allocatable
- If nothing in the workloads actually selects on the labels it creates

## Notes

**Chart** from the project's Helm repository, with a `HelmRelease`, `HelmRepository` and namespace
manifest. Recorded as a link only.

**NFD labels; it does not allocate.** This is the distinction that matters most and the one most
often missed. NFD tells you a node **has** an NVIDIA GPU by labelling it. Making that GPU a
schedulable, countable resource — `nvidia.com/gpu: 1` — is the **device plugin's** job, and it is a
separate installation. NFD is the discovery layer beneath it, not a replacement for it.

The full GPU stack is therefore: NFD labels the hardware, the device plugin advertises it as an
allocatable resource, and a GPU-aware scheduler such as
[KAI](../../../managed/scheduler/kai-scheduler/README.md) or
[Volcano](../../../managed/scheduler/volcano/README.md) decides who gets it.

**Two components**, worth knowing when debugging: `nfd-worker` runs on every node and detects
features; `nfd-master` receives what workers report and applies the labels. A node with no labels is
usually a worker that is not running; wrong labels are usually a stale master.

**Custom rules** are the extension point. `NodeFeatureRule` custom resources let you define labels
derived from discovered features — "if this PCI device is present and this kernel module is loaded,
label it `accelerator=foo`". That is how vendor-specific or site-specific hardware gets represented
without patching NFD.

**The label sprawl caveat:** NFD applies a great many labels by default, and `kubectl describe node`
becomes long. Feature sources can be restricted to the ones actually used, which is worth doing —
labels nothing selects on are noise, and they make the ones that matter harder to find.

---

[← Nodes](../README.md)
