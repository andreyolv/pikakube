[← Cloud cost visibility](../README.md)

# OptScale

<https://github.com/hystax/optscale>
<https://github.com/hystax/helm-charts>

---

## The problem it solves

Most of the FinOps market is SaaS: your billing export leaves your account, and the analysis comes
back as a subscription. For organisations that will not do that, the alternative is usually a
spreadsheet.

OptScale (Hystax) is a **full FinOps platform, Apache-2.0 and self-hostable**. It ingests billing
data from the cloud providers and produces the things a FinOps programme actually needs: cost
breakdown by account, service and tag; optimisation recommendations such as idle and unattached
resources; budgets and constraints with alerts; anomaly detection; and a Kubernetes collector that
brings cluster cost into the same view.

It is unusual in scope. Most open-source cost tools do one job; this one attempts the whole inform
phase, across clouds, plus a Kubernetes side.

## When to use it

- **a FinOps platform is genuinely needed and SaaS is not acceptable** — this is the main reason to
  choose it
- multi-cloud, where a single view over several billing exports is the requirement
- when budgets, constraints and recommendations matter, not only a cost breakdown
- when there is capacity to operate it; see below

## When not to use it

- for Kubernetes cost allocation alone. [OpenCost](../../kubernetes/opencost/README.md) is far
  lighter and is the CNCF standard for exactly that question
- one cloud account and a small team: the provider's own cost views plus one focused tool is less
  work than running a platform
- when nobody will own the deployment. This is a multi-service application with its own datastores —
  it is a platform commitment, not a chart
- expecting it to replace in-cluster attribution. Its Kubernetes collector complements
  [`kubernetes/`](../../kubernetes/README.md); it does not supersede it
- for pull-request cost estimation — that is [Infracost](../infracost/README.md)

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/hystax/optscale>** — the platform. Apache-2.0, actively developed. Worth noting
that the project's scope has widened over time to include ML/AI experiment cost tracking alongside
cloud FinOps, which is either a bonus or scope creep depending on what you came for.

**<https://github.com/hystax/helm-charts>** — the chart repository, served at
`https://hystax.github.io/helm-charts`. **It has not been updated since mid-2023.** That is the
finding to weigh: the platform is maintained, the charts published here are not, and the chart in use
in this repository (`kube-cost-metrics-collector` 0.1.2) comes from that stale repository. Confirm
against current documentation before assuming the chart matches the platform version.

**<https://hystax.com/documentation/optscale/e2e_guides/e2e_kubernetes.html#2-install-helm-chart>** —
the vendor's end-to-end guide for connecting a Kubernetes cluster to OptScale, deep-linked to the
Helm installation step. The flow is: register the cluster as a data source in OptScale, obtain the
credentials, install the collector chart pointing at your instance. Reading it is the only way to
know what values the collector actually needs — which is relevant, because the deployment here
supplies none of them.

**On the deployment here.** Flux, from `https://hystax.github.io/helm-charts`, chart
`kube-cost-metrics-collector` version **0.1.2**, into an `optscale` namespace, with **default values
and no configuration**.

Two things follow from that, and both are decisions rather than bugs:

1. **Only the collector is deployed, not OptScale itself.** The collector's job is to ship cluster
   cost metrics to an OptScale instance. There is no instance in this repository, so as it stands it
   has nowhere to send data — the manifests capture an evaluation in progress. Self-hosting the
   platform is the much larger commitment, and it has not been made.
2. **No credentials or endpoint are configured**, which is consistent with (1). When the decision is
   made, those belong in a Secret referenced by `valuesFrom`, in the same shape the
   [Kubecost](../../kubernetes/kubecost/README.md) release in this repository already uses.

The alternative worth weighing before finishing this: for Kubernetes cost specifically, this platform
already runs [OpenCost](../../kubernetes/opencost/README.md) and
[Kubecost](../../kubernetes/kubecost/README.md). OptScale earns its keep on the **cloud account**
side — budgets, recommendations, multi-account analysis — not by being a third answer to the
allocation question.

---

[← Cloud cost visibility](../README.md)
