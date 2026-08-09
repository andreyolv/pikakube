[← Provision](../README.md)

# Cluster API

<https://github.com/kubernetes-sigs/cluster-api>
<https://github.com/kubernetes-sigs/cluster-api-operator>
<https://github.com/kubernetes-sigs/image-builder>
<https://github.com/kubernetes-sigs/cluster-api-provider-azure>
<https://github.com/kubernetes-sigs/cluster-api-provider-aws>
<https://github.com/kubernetes-sigs/cluster-api-addon-provider-helm>

---

## The problem it solves

Cluster API makes **Kubernetes manage Kubernetes**. A management cluster holds `Cluster`,
`MachineDeployment`, `Machine` and related custom resources; controllers reconcile real clusters to
match them, using an **infrastructure provider** for the platform underneath — AWS, Azure, vSphere,
OpenStack, bare metal.

Creating a cluster becomes applying YAML. Upgrading becomes editing a version field, after which the
controller rolls machines. A failed machine is replaced, because desired state says it should exist.
Cluster lifecycle becomes the same declarative problem as every other resource in this repository.

## When to use it

- More than a handful of clusters, or clusters created and destroyed regularly
- On-premise and bare metal, where there is no managed control plane to fall back on
- You want cluster lifecycle in Git, reviewed and versioned like everything else
- Heterogeneous infrastructure behind one API

## When not to use it

- One cluster that will exist for years — [kubeadm](../kubeadm/README.md) and a runbook are simpler
- Without treating the management cluster as production; it is now the thing that must not break
- If nobody will learn the provider for your infrastructure; each has its own quirks and failure modes
- Where a managed control plane is available and acceptable

## Notes

**The recorded verdict**, translated: *"very cool for on-prem"*.

That is the only opinion in the whole [`on-premise/`](../../README.md) tree, and it is a defensible
one. On-premise cluster lifecycle is otherwise a collection of runbooks, and Cluster API is the only
option here that makes it declarative.

**The six recorded links, and why each is there:**

- **`cluster-api`** — the core: the CRDs and controllers.
- **`cluster-api-operator`** — installs and manages the Cluster API components themselves, including
  providers, so bootstrapping the management cluster is also declarative. The same
  chart-versus-operator choice that appears with
  [Karmada](../../../managed/multi-cluster/karmada/README.md).
- **`image-builder`** — builds node images with the kubelet, the container runtime and dependencies
  baked in. This is Packer with Kubernetes recipes, and it is the piece that makes machines boot
  ready instead of being configured afterwards. See
  [`virtual-machine/packer/`](../../../managed/virtual-machine/packer/README.md).
- **`cluster-api-provider-azure`** and **`-aws`** — the infrastructure providers. Note that both
  recorded providers are clouds, which is a slight tension with the "very cool for on-prem" verdict —
  the on-prem providers are vSphere, Metal3 and OpenStack, and they are not in the list.
- **`cluster-api-addon-provider-helm`** — installs Helm charts into clusters as they are created. The
  answer to "the cluster exists, now it needs a CNI", and an alternative to
  [`add-ons/`](../../add-ons/README.md).

That set is a complete picture of the problem rather than a single link: build the images, create the
clusters, install the add-ons, manage the whole thing declaratively.

**The three things to plan before adopting it:**

- **The management cluster is now critical.** It holds the state of every cluster it manages. It needs
  its own backups, its own monitoring, and a plan for what happens when it is unavailable —
  which, notably, is *not* an outage for the managed clusters, but is an outage for changing them.
- **The bootstrap problem.** Something must create the first cluster. `kind` is the usual answer, then
  the management cluster is pivoted onto itself or onto a permanent home.
- **Providers vary in maturity.** The AWS and Azure providers are well exercised; others less so, and
  the bare-metal story in particular deserves investigation before commitment.

---

[← Provision](../README.md)
