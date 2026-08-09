[← Dashboards](../README.md)

# Karpor

<https://github.com/KusionStack/karpor>

---

## The problem it solves

Most dashboards browse one cluster's objects through the API server. Karpor indexes resources —
across **multiple clusters** — and puts search in front of them: find every Deployment using a given
image, every object with a label, everything a team owns, without knowing which cluster it is in.

On top of that it adds compliance and risk views, and relationship graphs showing how a resource
connects to the things around it. The framing is "insight" rather than "console": it answers
questions about a fleet, not about a pod.

## When to use it

- Several clusters, and the question is "where is X" rather than "show me this cluster"
- Fleet-wide searches: an image version, a label, an owner
- You want compliance and risk views without assembling them yourself
- Multi-cluster inventory, complementing [`multi-cluster/`](../../multi-cluster/README.md) tooling

## When not to use it

- One cluster — `kubectl` and a simple UI cover it, and Karpor is a heavier thing to run
- As a live console for editing objects; that is not what it is optimised for
- If you cannot give it multi-cluster read access, which is a significant grant
- Where an indexing layer's staleness would matter; it is an index, not the API server

## Notes

**Chart** `karpor` version `0.7.6` from `https://kusionstack.github.io/charts`, deployed with an
`ingress.yaml` and a `namespace.yaml`. No notes were recorded beyond the project link.

**But it appears in another folder's notes**, and that is the useful cross-reference: the
[Forecastle](../../dashboard-ingress/forecastle/README.md) bug was found against **Karpor's
ingress** — Forecastle reads the host from `tls.hosts` rather than `rules.hosts`, and Karpor's
ingress does not work with a `*.127.0.0.1.nip.io` wildcard as a result. So the ingress manifest here
is the one that exposed a bug in a different tool. Worth knowing if Karpor's link on the launchpad
page appears broken: the fault is not Karpor's.

Two things to understand before adopting it, since the folder does not say:

- **It maintains its own storage and index.** That is what makes fleet-wide search possible and what
  makes it more than a UI to operate — there is state, and the state can be stale or lost.
- **KusionStack** is the parent project, an application-configuration platform. Karpor is the
  observability-and-search piece of it and runs standalone, but the wider project's direction shapes
  its roadmap.

The natural comparison is not with [Headlamp](../headlamp/README.md) but with a multi-cluster
inventory: it is closer in spirit to [`multi-cluster/`](../../multi-cluster/README.md) than to the
single-cluster consoles it sits beside in this folder.

---

[← Dashboards](../README.md)
