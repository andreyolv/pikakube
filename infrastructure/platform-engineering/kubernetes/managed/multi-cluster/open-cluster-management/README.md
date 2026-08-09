[← Multi-cluster](../README.md)

# Open Cluster Management

<https://github.com/open-cluster-management-io/ocm>

---

## The problem it solves

OCM is the **pull-based** option. A hub cluster holds the desired state; each managed cluster runs an
agent (the klusterlet) that registers itself with the hub and pulls down the work assigned to it.
Nothing connects from the hub to the cluster.

That inversion is the whole point. Clusters behind firewalls, at customer sites, on private networks
or on the edge cannot be reached from a central control plane — but they can reach out. Push-based
tools require connectivity that these environments do not have.

It is a CNCF project and the upstream of Red Hat's Advanced Cluster Management.

## When to use it

- Managed clusters that cannot accept inbound connections from a hub
- Edge, customer-site or air-gapped-adjacent fleets
- You want registration to be an explicit, mutually accepted handshake rather than credential distribution
- A foundation to build on — OCM is deliberately a framework with add-ons rather than a finished product

## When not to use it

- All clusters are reachable from one place; push-based tools are simpler then
- You want a finished management product out of the box — OCM is composable, not turnkey
- Small numbers of clusters where GitOps targeting several clusters is sufficient
- If the team is not prepared to assemble placement, policy and application add-ons themselves

## Notes

**Chart** from the project's Helm repository, with a namespace manifest and empty values. Recorded as
a link only.

**Why pull matters, concretely.** In a push model the hub holds credentials for every managed
cluster: one compromise, total fleet access, and every cluster must be routable from the hub. In
OCM's model the agent holds credentials to the hub and the hub holds none for the clusters. The
registration handshake requires acceptance on both sides, so a cluster cannot be added silently and
the hub cannot reach in uninvited.

That difference is the reason to choose OCM over [Karmada](../karmada/README.md), and it is a
security and topology argument rather than a features argument.

**What OCM is not** is equally important: it is a framework. Registration and the work-distribution
mechanism are the core; placement, policy, application lifecycle and observability are **add-ons**,
installed separately. Expecting the experience of [Rancher](../../dashboards/rancher/README.md) or of
a commercial product will disappoint. The generosity of that design is that each piece is replaceable;
the cost is that assembly is your job.

The **klusterlet** is the piece to understand operationally: an agent per managed cluster,
self-registering, pulling `ManifestWork` objects addressed to it. Its health is the fleet's health,
and it is the thing to monitor.

---

[← Multi-cluster](../README.md)
