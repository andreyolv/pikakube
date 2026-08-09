[← Virtual machine](../README.md)

# KubeVirt

<https://github.com/kubevirt/kubevirt>

---

## The problem it solves

KubeVirt runs virtual machines as Kubernetes workloads. A `VirtualMachine` custom resource describes
the VM; KubeVirt runs QEMU/KVM inside a pod, and the VM is then scheduled, monitored, exposed through
Services and declared in Git exactly like everything else in the cluster.

The point is not that Kubernetes is a good hypervisor. It is that an organisation with both
containers and VMs can have **one** control plane, one scheduler, one GitOps repository and one
monitoring stack instead of two — and can migrate workloads from VM to container incrementally,
with both behind the same Service during the transition.

It is a CNCF project and the basis of several commercial virtualisation platforms.

## When to use it

- Legacy or vendor software that genuinely cannot be containerised
- Windows workloads alongside Linux containers
- Incremental migration, where VM and container versions coexist
- A platform offering VMs as a product — see [Cozystack](../../platforms/cozystack/README.md)

## When not to use it

- A pure VM estate; Proxmox or VMware are better at that and have the tooling for it
- Isolating untrusted containers — [gVisor or Kata](../../../on-premise/container-runtime-sandbox/README.md) are far lighter
- Before storage is designed; it is the hard part and it does not improve later
- On cloud instances that do not permit nested virtualisation

## Notes

Recorded as a link only.

**The four things that decide whether a KubeVirt deployment works**, none of which is about KubeVirt
itself:

- **Storage.** VM disks are large, long-lived and not disposable, and **live migration requires
  `ReadWriteMany` volumes**. Without shared storage, moving a VM between nodes means shutting it
  down — which turns every node upgrade into scheduled downtime for every VM on it. This is the
  decision to make first.
- **Nested virtualisation.** KubeVirt uses KVM, which needs `/dev/kvm` on the node. On bare metal
  that is fine. On cloud instances it requires the provider to support nested virtualisation on that
  instance type; otherwise QEMU falls back to emulation and the performance is not usable.
- **Node lifecycle.** Draining a node with VMs on it is not draining a node with pods on it. Plan
  upgrades around live migration, and confirm live migration works before you need it.
- **Networking.** VMs often expect bridged interfaces, multiple NICs or static addressing. That means
  Multus and a CNI arrangement beyond the default, which is a separate piece of work.

**CDI — the Containerized Data Importer** — is the companion project that gets disk images into
PersistentVolumes, from HTTP, from a registry or by upload. It is effectively required, and it is a
separate installation. Worth knowing before wondering how a VM is supposed to acquire a disk.

**Where it appears elsewhere in this repository:**
[Cozystack](../../platforms/cozystack/README.md) bundles KubeVirt as the virtualisation layer of a
bare-metal cloud platform, which is KubeVirt in its most convincing form — the mechanism by which
tenants are offered VMs, rather than a way to run one awkward legacy system.

---

[← Virtual machine](../README.md)
