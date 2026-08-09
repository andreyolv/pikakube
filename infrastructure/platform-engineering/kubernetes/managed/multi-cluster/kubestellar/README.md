[← Multi-cluster](../README.md)

# KubeStellar

<https://github.com/kubestellar/kubestellar>

---

## The problem it solves

KubeStellar targets multi-cluster configuration management at scale, with an emphasis on **edge**
fleets — many clusters, often small, often intermittently connected, where a conventional hub-and-
spoke control plane does not fit comfortably.

Its model separates the **workload description spaces** where you author objects from the
**inventory and transport** layer that delivers them to clusters selected by binding policies. The
separation is what lets one description apply to hundreds of clusters without the hub holding a copy
of everything per cluster.

## When to use it

- Large fleets — hundreds or thousands of clusters, edge or otherwise
- Clusters that are intermittently connected and cannot be assumed reachable
- Where the number of clusters is the scaling problem, not the size of any one of them
- You are prepared to adopt a distinctly different conceptual model

## When not to use it

- A handful of clusters — [Karmada](../karmada/README.md) is more mature and much more conventional
- You want minimal new concepts; this has several, and they are not the usual ones
- Production reliance without a careful look at project maturity
- Simple replication of manifests, which remains a GitOps problem

## Notes

**Installed from an `OCIRepository`**, with a namespace manifest. Recorded as a link only.

The reason it sits in this folder alongside four other options rather than being dismissed: the
problem it addresses is genuinely different. Karmada and OCM assume a hub that knows about each
member cluster and holds per-cluster state. That assumption is fine at tens of clusters and becomes
the bottleneck at thousands — which is the normal shape of an edge fleet, where each site has a small
cluster and there are very many sites.

Two cautions to carry into any evaluation:

- **The vocabulary is unfamiliar.** Workload description spaces, inventory spaces, binding policies —
  these do not map one-to-one onto anything in Kubernetes, and the learning cost is real. It is the
  opposite of Karmada's "submit ordinary objects, attach a policy".
- **It is a CNCF Sandbox project** and less mature than its neighbours here. For a fleet of ten
  clusters, adopting the harder model and the younger project at once is difficult to justify.

The honest reading of its presence here: it was recorded because edge-scale multi-cluster is a real
category with different constraints, and it is the entry that covers that category. Nothing in this
repository operates at that scale.

---

[← Multi-cluster](../README.md)
