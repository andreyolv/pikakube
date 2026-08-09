[← Container runtime sandbox](../README.md)

# Firecracker

<https://github.com/firecracker-microvm/firecracker>

---

## The problem it solves

Firecracker is a **virtual machine monitor** built for one purpose: starting minimal VMs extremely
quickly, with a very small footprint. It boots a microVM in around 125 milliseconds, uses a few
megabytes of memory for the VMM itself, and deliberately implements only the devices a serverless
workload needs — no BIOS, no PCI, no graphics.

That narrowness is the security argument as much as the performance one: a smaller emulated device
surface is a smaller attack surface. AWS built it for Lambda and Fargate, which is the most
demanding possible test of "isolate untrusted code, cheaply, at enormous scale".

## When to use it

- As the hypervisor backend for [Kata Containers](../kata-containers/README.md), which is how it
  reaches Kubernetes
- Building a serverless or function platform where per-invocation isolation is required
- Where boot time and memory footprint per sandbox are the binding constraints

## When not to use it

- Directly, as a Kubernetes runtime — it is a VMM, not a CRI or OCI runtime
- General-purpose virtual machines; the device model is deliberately minimal
- Without nested virtualisation available, since it needs KVM
- When [gVisor](../gvisor/README.md) already meets the threat model with less machinery

## Notes

**The recorded note is an empty file.** `doc.md` existed and contained nothing — no link, no comment.

That is worth stating plainly rather than quietly filling in, because it is itself the finding: the
folder was created, the topic was recognised as belonging in this taxonomy, and nothing was ever
written. Of every gap in this part of the repository, this is the most explicit one, and an empty
placeholder is a more honest record than a folder that was never made.

**What belongs in it**, so the gap is at least described:

Firecracker is **not a container runtime**. It cannot be set as a `RuntimeClass` handler and the
kubelet cannot talk to it. It sits one layer below: Kata Containers implements the OCI runtime
interface and can be configured to use Firecracker as its hypervisor instead of QEMU or Cloud
Hypervisor. So the path into Kubernetes is Kata, and Firecracker is a configuration choice within it.

Choosing Firecracker under Kata trades device support for speed and footprint — no PCI hotplug, a
restricted set of virtio devices, and consequently limits on what can be attached to a running
microVM. For the serverless-shaped workloads it was designed for, that is exactly the right trade.

The other place it turns up is outside Kubernetes entirely: `firecracker-containerd` and various
microVM platforms use it directly for CI runners and sandboxed execution, where an isolated,
disposable machine per job is the whole requirement.

---

[← Container runtime sandbox](../README.md)
