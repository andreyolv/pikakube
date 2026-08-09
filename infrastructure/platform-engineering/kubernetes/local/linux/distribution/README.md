[← Linux](../README.md)

# Distribution

<https://github.com/torvalds/linux>
<https://github.com/siderolabs/talos>
<https://github.com/microsoft/azurelinux>
<https://github.com/alpinejs/alpine>

---

## The problem it solves

Which operating system sits under the kubelet. For a workstation this is taste; for a cluster node
it is an operational decision with a long tail:

- a general-purpose distro brings a package manager, SSH, a shell and a full userland — every one
  of which is a thing that can drift, be patched by hand, or be exploited
- an **immutable** distro brings none of that, and forces every change through an API
- a minimal container base image is a different question again, and gets confused with this one
  constantly

The three real options here are a normal distro you already know, **Talos** for nodes that do
nothing but run Kubernetes, and **Azure Linux** for a vendor-maintained minimal base.

## When to use it

- Talos — cluster nodes that will never be logged into, where drift and SSH access are liabilities
- Azure Linux (formerly CBL-Mariner) — an Azure/AKS estate that wants a Microsoft-supported base
- A general-purpose distro — workstations, and nodes that also run things Kubernetes does not manage
- The kernel repository itself — reference, for when a node problem is genuinely a kernel problem

## When not to use it

- Talos, if you expect to SSH in and fix something — there is no shell, and that is the design
- Talos, if the node must also run agents that assume a normal filesystem layout
- Any immutable OS on a workstation where you install tools daily
- Azure Linux outside the Azure ecosystem; the support story is the reason to pick it

## Notes

The original note is four links and no commentary. Two of them need explaining, because the list is
not homogeneous:

- **`torvalds/linux`** is the kernel itself. It is on the list as the root of the subject, not as
  something to install. Useful when a node symptom traces to a kernel version or a specific
  cgroup/namespace behaviour.
- **`alpinejs/alpine`** is Alpine.js, a **JavaScript framework** — not Alpine Linux. Read as a
  distribution entry it is almost certainly a paste error: the intended entry for a minimal Linux
  is Alpine Linux, whose musl libc and BusyBox userland make it a common container base and an
  occasional source of DNS and glibc-compatibility surprises. Preserved here as recorded, with the
  discrepancy flagged rather than silently corrected.

**Talos is the entry that matters.** No shell, no SSH, no package manager, no systemd units to
edit; the whole node is configured by a declarative machine config and managed over a gRPC API with
`talosctl`. That removes an entire category of "someone fixed it by hand and nobody wrote it down".
The trade is total: when something goes wrong there is no box to log into, and debugging happens
through the API or not at all.

---

[← Linux](../README.md)
