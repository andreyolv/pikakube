[← Kubernetes cost visibility](../README.md)

# Kubecost

<https://github.com/kubecost/cost-analyzer-helm-chart>
<https://github.com/kubecost/kubectl-cost>
<https://github.com/kubecost/cost-prediction-action>

---

## The problem it solves

[OpenCost](../opencost/README.md) computes the allocation and exposes it as an API and as Prometheus
metrics. That is exactly right for a platform team and useless for everyone else — nobody outside it
is going to write a PromQL query to find out what their namespace costs.

Kubecost is the **commercial product built on OpenCost**: the same allocation model, with the
interface, retention, reporting, budgets, alerting, multi-cluster aggregation and support that make
it usable by people who do not operate the cluster. Its network cost breakdown — traffic between
zones, between clusters and out to the internet — is a real differentiator, because egress is
invisible in every other tool in this folder.

Licensing has tiers: a free tier that is usable for a single cluster with limited retention, and paid
tiers for the features that follow from scale. **Check current terms directly**; they have changed
more than once.

## When to use it

- **when the audience is outside the platform team** — application teams, engineering managers,
  finance — and they need a page rather than a query
- when the network cost breakdown matters: cross-zone and egress traffic is real money and nothing
  else here shows it
- multi-cluster reporting as a product feature instead of an aggregation you build
- longer retention than the metrics store keeps
- alerting and budgets that are configured rather than written

## When not to use it

- when cost data is going into Grafana beside everything else — [OpenCost](../opencost/README.md) is
  the engine underneath, and the UI is then redundant
- **alongside OpenCost, permanently.** Two systems computing the same number is a steady state
  nobody chose
- without checking which tier the features you are demonstrating belong to
- with its bundled Prometheus stack on a cluster that already has one — see the notes; but note that
  bringing your own has a cost of its own
- expecting it to optimise anything: it attributes, and the action is
  [`optimization/`](../../../optimization/README.md)

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/kubecost/cost-analyzer-helm-chart>** — the chart, and the deployment surface.
Large, with a values file to match.

**<https://github.com/kubecost/kubectl-cost>** — a `kubectl` plugin that queries the allocation API
from the terminal: `kubectl cost namespace`, `kubectl cost deployment`. The point is that it puts
cost where engineers already work rather than behind a login. For anyone who lives in `kubectl`, it
is a better interface than the UI, and it is the cheapest way to get people to look at cost at all.

**<https://github.com/kubecost/cost-prediction-action>** — a GitHub Action that predicts the cost
impact of a change to Kubernetes manifests, commented on the pull request. This is the Kubernetes
counterpart of [Infracost](../../cloud/infracost/README.md), and it closes a gap that folder cannot:
Infracost prices the node pools a Terraform plan declares, while this prices the effect of changing
a **workload's requests or replica count** — which is what actually drives the node count. Worth
knowing about; the same review-time saving as Infracost, on the half of the platform where the cost
is really decided.

**The allocation API query.**

```bash
curl http://kubecost.dev.xxxx.ai/model/allocation \
  -d window=3d \
  -d aggregate=namespace \
  -d accumulate=false \
  -d shareIdle=false \
  -d format=csv \
  -G
```

The most reusable artefact in this folder: **cost data without opening the UI.** `-G` turns the `-d`
values into query parameters on a GET. Each one is a decision from
[`visibility/`](../../README.md) section 5:

| Parameter | Meaning |
|---|---|
| `window=3d` | the period; also accepts absolute ranges |
| `aggregate=namespace` | the dimension — `controller`, `pod`, `label:team` and others are available |
| `accumulate=false` | **one row per day** rather than a single total for the window — this is what makes a trend visible instead of a snapshot |
| `shareIdle=false` | **idle capacity is not spread across namespaces.** Each namespace is charged what it reserved, and the gap between that and the node bill stays visible and unowned by the tenants |
| `format=csv` | straight into a spreadsheet or a pipeline |

`shareIdle=false` is the honest default argued for throughout this folder: spreading idle across
tenants makes every namespace look more expensive than it is and makes the actual waste — the
difference between what you bought and what you handed out — disappear into everyone's bill, where
nobody can act on it.

This command is also the basis of anything scheduled: a job that runs it weekly and publishes the CSV
is a functioning showback process, with no product involved.

**<https://github.com/kubecost/cost-analyzer-helm-chart/issues/2392>** — *"Failed Prometheus Metric
Test: Test failed for 'Kubecost's CPU usage recording rule is set up'"* (June 2023, closed).

This is **the** issue for the configuration used here, and it is the hidden cost of pointing Kubecost
at an existing Prometheus. Kubecost's queries depend on a set of **recording rules** — pre-computed
series it expects to find. Its bundled Prometheus ships them; an external Prometheus does not, so
they have to be added to the platform's own rule configuration. Until they are, Kubecost's
diagnostics report failures and some views are wrong or empty in ways that look like a licensing or
integration problem.

The lesson generalises: *"bring your own Prometheus"* is the right decision and it is not free. Check
the tool's diagnostics page after installing, and treat the required recording rules as part of the
deployment rather than as an optional extra.

### On the deployment here

Flux, chart `cost-analyzer` **1.104.1**, into a `kubecost` namespace, with the token supplied through
`valuesFrom` a `kubecost-token` Secret targeted at `kubecostToken` — the correct pattern: the
credential is referenced, never written into a values file in Git.

**The bundled stack is comprehensively disabled**, and this is the part worth copying:

```yaml
global:
  prometheus:
    enabled: false
    fqdn: http://prometheus-server.monitoring.svc:80
  grafana:
    enabled: false
    proxy: false
prometheus:
  nodeExporter:
    enabled: false
  kubeStateMetrics:
    enabled: false
  kube-state-metrics:
    disabled: true
  serviceAccounts:
    nodeExporter:
      create: false
```

Prometheus, Grafana, node-exporter and kube-state-metrics are each switched off individually,
including the service account that would otherwise be left behind. That is someone who has been
bitten by the bundled stack before — and it is exactly the configuration that makes issue 2392 above
apply, so the recording rules are the thing to verify.

**`cluster_id: ANDREYOLV_DEV`** is set as an external label on the Prometheus configuration. Cluster
identity has to be stable and unique from the first day; it cannot be reconstructed later, and
renaming it orphans the history.

**Network costs are enabled**, with `azure-cloud-services: true` — the network cost daemonset
attributes traffic, and the Azure flag classifies traffic to Azure services separately from general
egress. This is the feature that has no equivalent in OpenCost, and it costs a daemonset on every
node.

**`cloudIntegrationSecret: cloud-integration-secret`** — the same billing integration OpenCost uses
here, so both are priced from invoiced rates rather than list prices.

**`grafanaURL`** is left as a placeholder, pointing at where Kubecost's Grafana dashboards would be
deep-linked from its UI.

**The open question**, unchanged from [`kubernetes/`](../README.md) section 3: OpenCost and Kubecost
are both deployed here, and Kubecost is built on OpenCost. That is a reasonable state while
evaluating and a poor one to keep — two systems, one number, twice the operational surface.

---

[← Kubernetes cost visibility](../README.md)
