[← Alerting](../README.md)

# Robusta

<https://github.com/robusta-dev/robusta>
<https://docs.robusta.dev/>

---

## The problem it solves

An Alertmanager notification says a pod is crash-looping. It does not say **why**, so every
page begins the same way: open the dashboard, pull the logs, check what was deployed
recently, look at the events.

Robusta attaches that context to the alert itself — recent logs, a graph of the relevant
metric, the Kubernetes events, and what changed. The notification arrives with the first ten
minutes of investigation already done.

It also runs **automations**: playbooks triggered by an alert or a cluster event, which can
gather more data or take action.

## When to use it

- alerts arrive without context and responders always start from zero
- you want automated first-response steps rather than manual triage
- Kubernetes-specific enrichment matters — events, logs and deploys correlated to the alert

## When not to use it

- alert volume is low enough that gathering context by hand is not a burden
- you want routing only, which [Alertmanager](../alertmanager/) already does

## Related

The same project maintains [kubewatch](../../events/kubewatch/), which is a much simpler
event-notification tool.

---

[← Alerting](../README.md)
