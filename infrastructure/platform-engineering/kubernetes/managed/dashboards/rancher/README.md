[← Dashboards](../README.md)

# Rancher

<https://github.com/rancher/rancher>

---

## The problem it solves

Rancher is a **multi-cluster management platform**, not a dashboard. It provisions clusters (on
bare metal, VMware, or through cloud providers), imports existing ones, and then governs them
centrally: users and groups from your identity provider, RBAC projected across clusters, a catalog
of applications, and a single console covering the whole fleet.

Its central abstraction is the **Project** — a group of namespaces across which permissions and
quotas are managed together. That fills a genuine gap: Kubernetes has namespaces and clusters, and
nothing in between, which is exactly the granularity most organisations need.

## When to use it

- Many clusters, especially heterogeneous ones, needing one place to manage access
- On-premise or edge fleets where cluster provisioning is your problem
- Centralised identity and RBAC across clusters, driven from an existing directory
- You want the Project abstraction between namespace and cluster

## When not to use it

- A single cluster — this is a platform to operate, and the dashboard is the least of it
- If a lighter cluster UI is all that is wanted; the other tools here are that
- Where you do not want a management plane holding credentials to every cluster
- Without planning its own availability; if Rancher is how access is granted, Rancher being down matters

## Notes

**Chart** `rancher` version `2.10.0` from
`https://releases.rancher.com/server-charts/stable`, with a namespace manifest. Recorded as a link
only.

Note the source: `stable`, as opposed to `latest` and `alpha`, which Rancher publishes separately.
Choosing `stable` is the right default and worth being deliberate about — Rancher's channels have
meaningfully different support expectations.

**Why it does not belong beside the other tools here**, stated plainly: everything else in
[`dashboards/`](../README.md) shows you a cluster. Rancher *runs* clusters. Its closest neighbours in
this repository are [`multi-cluster/`](../../multi-cluster/README.md) and
[`platforms/`](../../platforms/README.md), and the honest comparison is with those, not with
[Skooner](../skooner/README.md).

**Two things to know before installing it:**

- **It needs cert-manager** and a real hostname. Rancher terminates TLS for its own console and for
  the agents in every downstream cluster; that is not optional, and it is the most common reason a
  first install does not come up.
- **Downstream clusters run a Rancher agent** with substantial permissions, and the Rancher server
  holds the credentials to reach all of them. That concentration is the trade: one place to manage
  the fleet is also one place to compromise it.

SUSE maintain it, alongside RKE2, k3s, Longhorn and NeuVector — so adopting Rancher tends to pull a
broader stack behind it. Worth knowing whether that is the intent.

---

[← Dashboards](../README.md)
