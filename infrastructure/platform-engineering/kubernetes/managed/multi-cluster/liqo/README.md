[← Multi-cluster](../README.md)

# Liqo

<https://github.com/liqotech/liqo>

---

## The problem it solves

Liqo establishes a **peering** between two clusters and then makes the remote one appear as a virtual
node locally. Pods scheduled onto that node run in the peer cluster. So far, the same idea as
[Admiralty](../admiralty/README.md).

What makes Liqo different is what comes with the peering: it also extends **networking** — pods and
services across the peered clusters can reach each other, with the overlay set up as part of the
peering rather than as a prerequisite — and it offers **storage** reflection for the remote side.

That matters because cross-cluster networking is the problem every other tool in this folder leaves
to you, and it is usually the hardest part.

## When to use it

- Bursting workloads to another cluster where they must still reach local services
- Peering between organisations or sites, where a full federation control plane is disproportionate
- You want cross-cluster networking as part of the tool rather than as a mesh project of its own
- Symmetric, bidirectional resource sharing between clusters

## When not to use it

- Many clusters with central policy-driven placement — that is [Karmada](../karmada/README.md)
- Where the network overlay Liqo creates would conflict with an existing mesh or CNI arrangement
- Strict network segmentation between clusters; peering is the opposite of that by design
- Stateful workloads expecting their original volumes; reflection is not migration

## Notes

**Chart** `liqo` from the project's Helm repository, with a namespace manifest and empty values.
Recorded as a link only.

Three things that decide whether it fits, none of which is in the project's headline:

- **Peering is a relationship, not a hierarchy.** Liqo's model is cluster-to-cluster, negotiated,
  and can be bidirectional. That is a good fit for two teams or two sites sharing capacity, and a
  poor fit for governing a fleet from one place. If you want a hub, this is the wrong shape.
- **It creates a network overlay.** That is the headline feature and the main integration risk. On a
  cluster that already runs a service mesh, or has a CNI with strong opinions, the interaction needs
  checking before installation rather than after.
- **CIDR conflicts are the classic failure.** Two clusters built independently frequently use
  overlapping pod and service CIDRs. Liqo handles remapping, but the setup is where peering most
  often fails, and it is worth knowing the CIDRs of both clusters before starting.

Academic origin — it came out of Politecnico di Torino — which shows in the quality of the model and
in a documentation style that is stronger on concepts than on operations.

---

[← Multi-cluster](../README.md)
