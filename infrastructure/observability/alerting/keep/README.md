[← Alerting](../README.md)

# Keep

<https://github.com/keephq/keep>
<https://github.com/keephq/helm-charts>

---

## The problem it solves

Alertmanager groups and deduplicates alerts **from Prometheus**. It has nothing to say about
the alerts arriving from Datadog, from a cloud provider, from a database monitor and from CI
— all describing the same outage from four angles.

Keep is an alert management layer above the sources: it ingests from many systems,
correlates related alerts into a single incident, deduplicates, and applies workflows.

## When to use it

- alerts come from **several independent systems** and nobody can tell which belong together
- a single incident produces notifications in four different tools
- you want workflows across sources rather than per-tool automation

## When not to use it

- Prometheus is the only source — Alertmanager's grouping and inhibition already solve this, with far less to run
- the problem is missing *context* rather than missing *correlation* — that is [Robusta](../robusta/README.md)

## The honest framing

This is a tool for a specific kind of organisational mess: multiple monitoring systems that
nobody is going to consolidate. If consolidating is still possible, that is the cheaper fix.

---

[← Alerting](../README.md)
