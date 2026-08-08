[← Exporters](../README.md)

# Azure Metrics Exporter

<https://github.com/webdevops/azure-metrics-exporter>
<https://github.com/webdevops/azure-resourcemanager-exporter>

---

## The problem it solves

The Azure equivalent of the [AWS case](../aws-exporter/): managed services — Azure Database
for PostgreSQL, Event Hubs, Storage Accounts, Synapse — publish to **Azure Monitor**, not to a
Prometheus endpoint.

Two complementary exporters here:

| Exporter | What it exposes |
|---|---|
| **azure-metrics-exporter** | Azure Monitor metrics — the runtime numbers |
| **azure-resourcemanager-exporter** | Resource Manager data — quotas, costs, resource inventory, expiring credentials |

The second is worth noticing. **Quota exhaustion and expiring service principal secrets** are
classic Azure outages, and neither appears in a runtime metric. Turning them into alertable
series prevents a category of incident that otherwise only announces itself by failing.

## When to use it

- managed Azure services are part of the platform and belong in the same alerting stack
- subscription quotas or credential expiry should be visible before they cause an outage
- Azure Monitor alerts and Alertmanager should not be two separate on-call surfaces

## When not to use it

- everything runs in-cluster with native metrics
- cost analysis is the goal — Azure Cost Management is the source for that, and
  [cloudcost-exporter](../cloudcost-exporter/) covers the Prometheus side

## Alternative

<https://github.com/RobustPerception/azure_metrics_exporter> — the older option, kept here for
reference. The webdevops exporters are the more actively maintained choice.

## Same caveats as AWS

Azure Monitor API calls are rate-limited, and the data lags by minutes. Scrape slowly, and set
alert thresholds that tolerate the delay.

---

[← Exporters](../README.md)
