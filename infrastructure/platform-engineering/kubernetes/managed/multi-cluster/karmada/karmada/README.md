[← Karmada](../README.md)

# Karmada (chart)

<https://github.com/karmada-io/karmada>

---

## The problem it solves

The direct installation of a Karmada control plane: an aggregated API server, its own etcd, the
scheduler, the controller manager and the agent components — deployed by one Helm chart into one
namespace.

Once it is running, member clusters are registered against it and ordinary Kubernetes objects
submitted to the Karmada API server are distributed according to `PropagationPolicy` resources.

## When to use it

- One Karmada control plane, which is the normal case
- You want the installation to be a `HelmRelease` like everything else in the repository
- Version and configuration managed through Helm values, in Git

## When not to use it

- Several Karmada control planes provisioned repeatedly — use the [operator](../karmada-operator/README.md)
- Before there is an actual placement requirement; see [`multi-cluster/`](../../README.md)
- If member clusters cannot be reached from the hub; Karmada pushes, and a pull-based tool such as
  [OCM](../../open-cluster-management/README.md) fits firewalled fleets better

## Notes

**Chart** `karmada` from the project's Helm repository, with a namespace manifest and empty values.
Recorded as a link only.

Three things worth knowing before the values block stops being empty:

- **It runs its own etcd.** The Karmada control plane is a real control plane, with the storage,
  backup and availability obligations that implies. The chart's default is a single etcd replica,
  which is fine for a trial and not for anything that matters. This is the single most important
  value to change.
- **Member cluster registration is a separate step** performed with `karmadactl join` (push mode) or
  by installing the agent in the member cluster (pull mode). The chart installs the hub; it does not
  make any cluster a member.
- **The kubeconfig it generates is the keys to everything.** Access to the Karmada API server is
  effectively access to every registered cluster, mediated by Karmada's own RBAC.

The choice between this and the [operator](../karmada-operator/README.md) is covered in the
[parent](../README.md); for one control plane, this is the simpler path and the right default.

---

[← Karmada](../README.md)
