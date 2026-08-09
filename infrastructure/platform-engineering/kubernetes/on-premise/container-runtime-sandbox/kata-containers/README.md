[← Container runtime sandbox](../README.md)

# Kata Containers

<https://github.com/kata-containers/kata-containers>

---

## The problem it solves

Kata runs each pod inside a **lightweight virtual machine with its own kernel**, while keeping the
container interface intact. To Kubernetes it is a pod; underneath it is a microVM, and the isolation
boundary is the hypervisor rather than the host kernel's syscall surface.

Compared with [gVisor](../gvisor/README.md), the trade is inverted. gVisor reimplements the kernel
interface in userspace and therefore has compatibility gaps; Kata gives the workload a **real Linux
kernel**, so almost everything works exactly as it would in a container — at the cost of a VM's
memory footprint per pod.

## When to use it

- Untrusted workloads where compatibility cannot be compromised
- Applications making unusual syscalls, or needing kernel features gVisor does not implement
- Workloads that need a **different kernel version or kernel modules** from the host
- Where hardware-enforced isolation is a compliance requirement

## When not to use it

- Trusted workloads; the memory overhead is pure loss
- High pod density; a VM per pod changes the node sizing arithmetic entirely
- Nodes without nested virtualisation, which rules out many cloud instance types
- When gVisor's lighter footprint is sufficient for the threat model

## Notes

Recorded as a link only.

**The mechanism**, in enough detail to plan with: Kata implements the OCI runtime interface, so
containerd calls it as it would call `runc`. Instead of creating namespaces, it boots a microVM with
a minimal guest kernel and a small agent, and runs the container inside it. Pod networking and
volumes are passed through. The pod's lifecycle is the VM's lifecycle.

Supported hypervisors include QEMU, Cloud Hypervisor and
[Firecracker](../firecracker/README.md) — which is why Firecracker appears in this folder as a layer
underneath rather than as an alternative. Firecracker gives the fastest boot and the smallest memory
footprint; QEMU gives the widest device support.

**Three things that decide feasibility:**

- **Nested virtualisation.** Kata needs `/dev/kvm`. On bare metal that is normal; on cloud instances
  it depends on the instance type supporting nested virtualisation, and many do not. This is the
  first thing to check, not the last.
- **Memory per pod.** Each pod carries a guest kernel and a VM. At a density planned for containers,
  the node runs out of memory well before it runs out of CPU.
- **Startup time.** Tens to hundreds of milliseconds rather than a few. Irrelevant for long-running
  services, and material for short-lived jobs at volume.

**Compared with running [KubeVirt](../../../managed/virtual-machine/kubevirt/README.md)**, which also
puts VMs in a cluster: KubeVirt runs VMs *as* VMs, with disks and consoles, for workloads that are
virtual machines. Kata runs *containers* in VMs, invisibly, for isolation. Same underlying technology,
opposite intent.

It is an OpenStack Foundation project, formed from Intel's Clear Containers and Hyper's runV, and it
is mature — one of the few genuinely production-proven answers to hostile multi-tenancy.

---

[← Container runtime sandbox](../README.md)
