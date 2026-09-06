[← Platforms](../README.md)

# Plural

<https://github.com/pluralsh/plural>
<https://github.com/pluralsh/console>

---

## The category this folder does not have

[§1](../README.md#1-four-different-products-in-one-folder) sorts this folder into four
categories — full distribution, application abstraction, package UI, domain platform. Plural is a
fifth: a **fleet control plane**. One self-hosted console managing many clusters, each running an
agent that pulls its assigned state.

That is a different axis from everything else here. APL, Otomi and KubeSphere make a single
cluster complete. Plural assumes several clusters already exist and asks who operates them
together.

## Read the repository history before evaluating

This matters more than usual, because the product changed shape:

| Era | What Plural was |
|---|---|
| Originally | an **open-source marketplace and CLI** — `plural bundle install`, generating Terraform and Helm to deploy applications into your own cloud account |
| Now | the **Plural Console**: agent-based continuous deployment across a fleet, self-service catalogs with PR automation, Terraform/IaC stacks, a fleet-wide Kubernetes dashboard, and an AI assistant over it |

The linked `pluralsh/plural` repository is the CLI lineage; `pluralsh/console` is where the
current product lives. **Check the activity and licensing on both before treating either as
current** — this is exactly the "who maintains it, and would you notice if they stopped" question
from [§3](../README.md#3-how-to-evaluate-one-honestly), and the answer here is not static.

It is also open core. Which capabilities sit behind the commercial tier is a question to answer
from the current documentation rather than from the repository's README.

## What it overlaps

Plural's continuous deployment competes directly with what this repository already runs:

| Concern | Plural | What is here today |
|---|---|---|
| Deploying manifests from Git | Plural CD, agent per cluster | [Flux](../../../../gitops/flux/README.md) |
| Multi-cluster delivery | the console's fleet view | [Flux](../../../../gitops/flux/README.md) per cluster, or [Fleet](../../../../gitops/fleet/README.md) |
| Terraform runs | Stacks | [tf-controller](../../../../gitops/flux/tf-controller/README.md), or CI |
| Self-service creation | catalogs and PR automation | the gap the [IDP folder](../../../../idp/README.md) describes |
| Fleet dashboard | built in | [dashboards/](../../dashboards/README.md), per cluster |

The last row is the one Plural answers that nothing here does — a single place to see and act on
every cluster. The rows above it are the ones that make adoption expensive, because
[§2](../README.md#2-the-trade-every-platform-asks-you-to-make) applies in full: bringing its own
GitOps means one of the two has to go.

## When to use it

- there is a **real fleet** — many clusters, several teams, and the operational question is
  consistency across them rather than capability within one
- clusters are unreachable from a hub (edge, on-premise, separate accounts), which is what the
  agent-pull model is for
- you want a commercial support relationship for the fleet layer rather than owning it

## When not to use it

- **one cluster.** The entire premise is fleet scale; below it the console is overhead
- Flux or Argo CD is established and working — you would be replacing a delivery layer that is not
  the problem
- the requirement is a developer portal — that is [`../../../../idp/`](../../../../idp/README.md),
  and Backstage is the comparison
- open core is a constraint and the capabilities you need are on the far side of it

## Notes

Nothing deployed — recorded from <https://github.com/pluralsh/plural>.

**Where this lands for pikakube.** It does not, and the reason is the first bullet above: this is
a Kind-based single-cluster repository, and a fleet control plane with no fleet is pure overhead.

What is worth extracting is the category rather than the product. This folder has eleven entries
about making one cluster complete and none about operating many, and that gap is real —
[`multi-cluster/`](../../multi-cluster/README.md) covers workload **scheduling** across clusters
(Karmada, Liqo, OCM), which is a different problem from fleet **operations**. Plural, Rancher and
the fleet features of Argo CD are the answer to the second question, and if this repository ever
grows past one cluster that is the shelf to look at — not this folder's distributions.

---

[← Platforms](../README.md)
