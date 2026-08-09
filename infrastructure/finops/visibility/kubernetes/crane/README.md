[← Kubernetes cost visibility](../README.md)

# Crane

<https://github.com/gocrane/crane>
<https://github.com/gocrane/helm-charts>

---

## The problem it solves

Cost visibility and cost optimisation are usually separate tools: one attributes, another
recommends, a third autoscales, and nothing joins them. The attribution says a namespace is
expensive; working out what to do about it starts again from scratch.

Crane (Cloud Resource Analytics and Economics) is a CNCF sandbox project that puts the whole loop in
one place. Alongside cost analysis it ships:

| Capability | What it does |
|---|---|
| **Cost visualisation** | cluster and workload cost, with Grafana dashboards |
| **Recommendation framework** | resource requests, replica counts, HPA configuration, and **idle node** identification |
| **Effective HPA** | prediction-driven horizontal autoscaling — scale *before* the load arrives, from a forecast, instead of reacting to it |
| **QoS and colocation** | run low-priority workloads on the slack of high-priority ones, with the agent protecting the latter |

Apache-2.0, and the ambition is genuinely broader than anything else in this folder. The predictive
autoscaling and the colocation work are the parts with no real open-source equivalent.

## When to use it

- when the appeal is the **combination** — analysis plus recommendations plus predictive scaling in
  one project, rather than four
- **predictable, cyclical load** where reactive HPA always scales a few minutes late; forecasting the
  curve is a real improvement
- colocating batch work on the headroom of latency-sensitive services, which is a genuine efficiency
  gain almost nobody realises
- as a source of idle-node and replica recommendations that other tools in this repository do not
  produce

## When not to use it

- **for cost allocation as the primary goal.** [OpenCost](../opencost/README.md) is the CNCF
  standard for that question, and the ecosystem — exporters, dashboards, Kubecost — is built around
  its model
- alongside VPA or another right-sizer on the same workloads: overlapping recommenders, and possibly
  overlapping mutations — see [`rightsizing/`](../../../optimization/rightsizing/README.md)
- alongside a standard HPA on the same workload; Effective HPA replaces it rather than complementing
  it
- **without checking project activity first** — see the notes
- when only one of its capabilities is wanted; each has a more focused alternative here

## Notes

Original notes recorded for this folder, translated and explained.

**<https://github.com/gocrane/crane>** — the project. CNCF sandbox, Apache-2.0, originating from
Tencent.

**<https://github.com/gocrane/helm-charts>** — the chart repository, at
`https://gocrane.github.io/helm-charts`.

**The finding that should be checked before anything else: the project appears dormant.** As of
mid-2026, the main repository's most recent activity is from **December 2024**, and the chart
repository's from **April 2024** — well over a year of no commits on both. It has stars and a real
architecture; that is not the same as being maintained.

That matters more here than for most tools, because of what Crane does. A cost dashboard that goes
stale is an inconvenience. Crane's agent participates in **QoS enforcement and colocation**, and
Effective HPA **owns the scaling decisions** for the workloads it manages — components in the
critical path of production behaviour. An unmaintained project there is a different risk category
from an unmaintained reporting tool: no security patches, no compatibility fixes as Kubernetes APIs
move, and nobody to raise a regression with.

Verify current status directly rather than trusting this note — dormant projects do come back — but
verify before deploying anything beyond the analysis components.

**On the deployment here.** Flux, chart **0.11.0** from `https://gocrane.github.io/helm-charts`, into
a `crane` namespace, with **default values**.

Default values means the analysis and recommendation components, not the agent-side colocation
features, which need explicit configuration. That is the right way round: **the recommendation
framework is the low-risk half** — it produces suggestions and changes nothing — while Effective HPA
and QoS enforcement affect running workloads.

The realistic role for Crane on this platform, given that
[OpenCost](../opencost/README.md) and [Kubecost](../kubecost/README.md) already answer the allocation
question, is as a **second opinion on recommendations**: its idle-node and replica recommenders cover
ground that [VPA](../../../optimization/rightsizing/vpa/README.md), Goldilocks and KRR do not, since
those size containers rather than fleets. Weigh that against the maintenance finding above before
depending on it.

---

[← Kubernetes cost visibility](../README.md)
