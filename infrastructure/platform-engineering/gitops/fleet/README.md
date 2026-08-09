[← GitOps](../README.md)

# Fleet

<https://github.com/rancher/fleet>

---

## The problem it solves

Fleet is Rancher's GitOps engine, and it is built around a different question from Flux and Argo CD.
Those two ask "how do I reconcile this repository into this cluster". Fleet asks **"how do I get this
bundle onto the two thousand clusters that match this label"**.

The design follows from that. A `GitRepo` object on a management cluster produces `Bundle`s, and
bundles are targeted at downstream clusters by label selector, with per-target value overrides. The
management cluster holds the intent; agents on the downstream clusters pull and apply it. Scale in
Fleet means number of clusters, not size of repository.

It is the built-in GitOps mechanism in Rancher, so on a Rancher estate it is already there and
already integrated with the cluster registry.

## When to use it

- **Rancher is the management plane** — Fleet is the native option and comes with the cluster
  inventory already populated
- the estate is many clusters, especially edge or retail sites, where the same workload is deployed
  everywhere with small per-site differences
- targeting by cluster label with per-target overrides is the primary requirement
- the number of clusters is large enough that a per-cluster `Kustomization` or `Application` would be
  unmanageable

## When not to use it

- a small number of clusters — the targeting machinery is overhead with nothing to target
- the platform is already reconciling with [Flux](../flux/README.md) or
  [Argo CD](../argocd/README.md); a second GitOps engine means two systems that can both write
- there is no Rancher; Fleet standalone works but loses the integration that is most of its value
- Helm-centric platform deployments where a chart source needs to be a first-class object with its
  own credentials and interval

## Notes

The original note was the project link alone:

- <https://github.com/rancher/fleet>

What is checked in is a working evaluation rather than a bare link, and two details in it are worth
reading:

- **Two charts, in order.** `fleet-crd` and `fleet` are separate `HelmRelease`s at version `0.9.3`,
  from `https://rancher.github.io/fleet-helm-charts/`, and the second declares `dependsOn` the first.
  Splitting CRDs into their own chart is the pattern that makes upgrades survivable — CRDs are
  cluster-scoped and outlive the release, so a chart that bundles them either fails to update them or
  deletes them on uninstall. Fleet gets this right, and the `dependsOn` is what makes the ordering
  explicit to Flux rather than accidental.
- **Fleet is installed *by* Flux here.** The chart is delivered through a Flux `HelmRelease` and
  `HelmRepository`. That is the correct way to evaluate it in this repository and also a reminder
  that if Fleet were adopted, one of the two would have to stop being the reconciler.

The example in `example/gitrepo.yaml` is Fleet's own `simple` sample from
`github.com/rancher/fleet-examples`, targeted at the `fleet-local` namespace — the built-in target
meaning "the management cluster itself". It demonstrates the `GitRepo` object without needing a
second cluster to exist.

No opinion was recorded about Fleet, which places it with the mapped-but-not-adopted tools in this
folder. The platform is not on Rancher, and that is most of the answer.

---

[← GitOps](../README.md)
