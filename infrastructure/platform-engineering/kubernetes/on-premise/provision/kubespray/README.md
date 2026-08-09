[← Provision](../README.md)

# Kubespray

<https://github.com/kubernetes-sigs/kubespray>

---

## The problem it solves

Kubespray is a set of Ansible playbooks that build a production-shaped cluster on machines you
already have. It wraps [kubeadm](../kubeadm/README.md) and fills in everything kubeadm deliberately
omits: the container runtime, a choice of CNI (Calico, Cilium, Flannel, and others), etcd topology,
load balancing for the API server, and a set of optional add-ons.

The input is an Ansible inventory of hosts and a variables file. The output is a highly available
cluster with the components you selected. It also handles scaling, upgrades and removal, which is
what distinguishes it from a one-shot installer.

## When to use it

- Bare metal or VMs where the machines exist and need to become a cluster
- Ansible is already the configuration management tool and the team knows it
- High availability with stacked or external etcd, without designing it yourself
- Air-gapped installations, which it supports with a local registry and package mirror

## When not to use it

- Many clusters created and destroyed routinely — [Cluster API](../cluster-api/README.md) is the
  better model
- Teams with no Ansible experience; debugging a failed playbook run requires it
- Where a declarative Kubernetes-native lifecycle is wanted — that is
  [Kubean](../kubean/README.md), which wraps this
- Without machines already provisioned; Kubespray configures hosts, it does not create them

## Notes

Recorded as a link only.

**It configures machines; it does not create them.** Kubespray starts from an inventory of hosts that
already exist and are reachable over SSH. Creating those machines — VMs, bare metal, cloud instances
— is a separate step, and that is precisely the boundary Cluster API erases.

**Two properties that make it the pragmatic on-premise choice:**

- **Component choice is real.** Kubespray supports several CNIs, several container runtimes and
  several etcd topologies as configuration rather than as forks. Where an opinionated installer
  decides for you, this exposes the decision.
- **Air-gapped support is genuine**, which is rare and is often the deciding factor. Installing
  Kubernetes with no internet access requires a local image registry, a package mirror and a way to
  pin every artifact; Kubespray documents that path rather than leaving it as an exercise.

**Two properties that make it hard work:**

- **Ansible runs are long and fail late.** A 40-minute playbook that fails at step 200 leaves a
  partially built cluster, and understanding what state it is in requires reading the role that
  failed.
- **The variables surface is enormous.** Hundreds of settings, most of which should be left alone,
  and the difficulty is knowing which ones should not.

**It uses kubeadm underneath**, which is the practical reason to have run kubeadm by hand first: when
Kubespray fails, the failure is usually in a kubeadm step, and the debugging is kubeadm debugging.

`kubernetes-sigs`, which is a strong signal for something that builds production clusters.

---

[← Provision](../README.md)
