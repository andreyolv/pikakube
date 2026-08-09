[← Alerting](../README.md)

# Alertmanager

<https://github.com/prometheus/alertmanager>
<https://prometheus.io/docs/alerting/latest/alertmanager/>

---

## The problem it solves

Prometheus evaluates rules and decides an alert is firing. It does **not** decide who hears
about it, how often, or whether forty simultaneous alerts should arrive as forty messages.

Alertmanager is that layer: grouping, deduplication, inhibition, silencing and routing to
receivers — Slack, email, PagerDuty, webhooks.

| Mechanism | What it buys |
|---|---|
| **Grouping** | 40 pods down in one namespace becomes one notification |
| **Inhibition** | the cluster-unreachable alert suppresses every service alert beneath it |
| **Silencing** | planned maintenance without disabling the rule |
| **Routing** | severity and team decide the destination |

## When to use it

- you run Prometheus — it is the standard companion and integrates with everything
- multiple teams or severities need different destinations
- alert storms from a single root cause are a problem

## When not to use it

- there is no Prometheus and you only want pod-failure notifications — [kwatch](../kwatch/README.md) is far less to run
- correlation across many *non-Prometheus* sources is the requirement — [Keep](../keep/README.md)

## The thing that confuses people

**Alertmanager does not generate alerts.** If an alert never arrives, check the Prometheus
rule first — an unloaded or non-matching rule looks identical to a routing problem from the
Alertmanager side.

---

[← Alerting](../README.md)
