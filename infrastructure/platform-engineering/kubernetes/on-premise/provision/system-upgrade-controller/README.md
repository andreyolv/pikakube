[← Provision](../README.md)

# system-upgrade-controller

<https://github.com/rancher/system-upgrade-controller>
<https://github.com/rancher/system-upgrade-controller/tree/master/manifests>

---

## The problem it solves

Upgrading the software **on** nodes — the OS, the kubelet, k3s or RKE2 itself — across a fleet,
without doing it by hand and without an outage.

The controller introduces a `Plan` custom resource: which nodes it applies to (by label selector),
what version to move to, how many nodes may be upgraded at once, whether to drain first, and what to
actually run. It then creates Jobs on the selected nodes to carry it out, in a controlled sequence.

It is Rancher's mechanism for upgrading k3s and RKE2, and it generalises to any node-level upgrade
you can express as a container image and a command.

## When to use it

- Self-managed clusters where node software must be upgraded on a schedule
- k3s or RKE2, where this is the intended upgrade path
- You want upgrades declared as Kubernetes objects rather than performed by a person
- Controlled concurrency and draining, rather than everything at once

## When not to use it

- Managed clusters, where node upgrades belong to the provider
- Immutable operating systems such as Talos, which upgrade by replacing the image
- Without PodDisruptionBudgets, since it drains
- For **Kubernetes control plane** upgrades on a kubeadm cluster; that sequence is
  [kubeadm's](../kubeadm/README.md) and has ordering rules of its own

## Notes

**Deployed as plain manifests, not Helm** — `namespace.yaml`, `deployment.yaml`, `configmap.yaml` and
a full `rbac/` directory with a ServiceAccount, ClusterRole and ClusterRoleBinding.

Both the project **and its upstream manifests directory** are recorded:

- <https://github.com/rancher/system-upgrade-controller/tree/master/manifests>

That second link is the good practice worth pointing at. A plain-manifest install copied into a
repository has no version and no provenance; six months later nobody can say whether it is current,
modified, or simply old. Recording where it came from turns that question into a diff.

**The RBAC is worth reading before applying it.** This controller creates privileged Jobs on nodes
that run arbitrary commands with host access — that is what upgrading a node's software requires. It
is, by construction, one of the most powerful things in a cluster: anything that can create a `Plan`
can run a container as root on the nodes it selects. Restricting who may create `Plan` resources is
not optional.

**The `Plan` fields that matter:**

- **`concurrency`** — how many nodes at once. One is the safe default and the slow one.
- **`drain`** — whether to cordon and drain before upgrading. Almost always yes, and it means
  PodDisruptionBudgets are in play.
- **`nodeSelector`** — which nodes. This is how control-plane and worker plans are separated, and
  separating them is how the correct order is enforced.
- **`version` or `channel`** — a pinned version, or a channel that resolves to the latest. In a
  GitOps repository, pinned.

**The relationship with [kured](../../nodes/kured/README.md):** they are complementary rather than
alternative. system-upgrade-controller applies the upgrade; kured handles the reboot that a kernel
update subsequently requires. Running both means being clear about which one drains a given node and
when — two controllers independently deciding to drain the same node is a scenario worth thinking
about before it happens.

---

[← Provision](../README.md)
