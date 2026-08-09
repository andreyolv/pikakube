[← Cloud cost visibility](../README.md)

# Komiser

<https://github.com/tailwarden/komiser>
<https://github.com/tailwarden/helm>

---

## The problem it solves

Cloud accounts accumulate. A volume detached during a migration, a load balancer for a service that
was deleted, snapshots from an incident two years ago, reserved addresses nobody released. None of
it is a problem individually — each is a small line on a large invoice with no owner, because the
owner left.

Komiser is a **self-hosted cloud inventory**: it reads the provider APIs, lists what exists with its
cost, region and tags, and presents it as a dashboard you can filter and group. It turns "the bill
went up" into a list of resources, which is the necessary first step to deleting anything.

It is inventory, not analysis. It tells you what exists; deciding what to remove and doing it is
still a human loop.

## When to use it

- **AWS accounts**, where its coverage is deepest — see the note below
- a self-hosted inventory when sending account inventory to a SaaS is not acceptable
- finding orphaned and untagged resources, once, before establishing a tagging policy
- as a shared read-only view for people who should not have console access

## When not to use it

- **on an Azure-first platform.** The recorded finding is that it is effectively limited to AWS, and
  an inventory tool that cannot see most of your estate is worse than none — it produces a
  confident, partial picture
- for Kubernetes cost. Cluster nodes appear as virtual machines and pods do not appear at all —
  [`kubernetes/`](../../kubernetes/README.md)
- as a FinOps platform. There is no budgeting, no recommendation engine, no chargeback —
  [OptScale](../optscale/README.md) is the tool with that scope
- where the cloud provider's own inventory and cost views already suffice; this is an extra service
  to run
- without reading the licence first — see below

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/tailwarden/komiser>** — the project. Two things to know before adopting:

- **The repository now redirects to `mlabouardy/komiser`** — it has moved out of the Tailwarden
  organisation back to its original author. That kind of move is a maintenance signal worth reading:
  check commit activity and release cadence rather than assuming a company is behind it.
- **The licence is not a standard OSI one.** GitHub does not identify a recognised open-source
  licence for it, which means the usual assumptions do not hold. Read the `LICENSE` file before
  deploying it anywhere that matters — this project has changed licence before.

**<https://github.com/tailwarden/helm>** — the chart repository, so it can be run in-cluster rather
than as a local binary. Small and lightly maintained.

**"limited to aws"** — the recorded evaluation finding, and the decisive one here. Komiser advertises
multiple providers, but coverage is far from even: the AWS integration is the mature one, and the
others cover a fraction of the resource types. On this platform — which runs on **AKS** — that makes
it close to useless, because the inventory it produces would omit most of the estate.

This is the generalisable lesson rather than a criticism of the tool: **for any multi-cloud tool,
verify coverage on the cloud you actually use before evaluating anything else.** A demo on AWS tells
you nothing about what it will show you on Azure.

**Nothing is deployed for this in the repository.** It was evaluated and set aside for the reason
above. The equivalent capability on Azure is closer to the provider's own resource graph and cost
analysis views, or to [OptScale](../optscale/README.md), which was evaluated for the broader FinOps
scope.

---

[← Cloud cost visibility](../README.md)
