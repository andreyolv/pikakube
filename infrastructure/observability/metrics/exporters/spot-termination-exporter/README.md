[← Exporters](../README.md)

# Spot Termination Exporter

<https://github.com/banzaicloud/spot-termination-exporter>
<https://github.com/banzaicloud/banzai-charts/tree/master/spot-termination-exporter>

---

## The problem it solves

Spot instances are reclaimed with roughly two minutes' notice, delivered through the
instance metadata endpoint. Nothing in Kubernetes surfaces that notice.

This exporter polls the metadata service and exposes the pending termination as a metric — so
reclamation becomes visible, countable and alertable rather than appearing as pods that
mysteriously vanished.

## When to use it

- spot instances run workloads that care about interruption
- you want to **correlate** reclamations with failures — "the pipeline failed at 03:12" and "the node was reclaimed at 03:11" is a complete explanation
- measuring how often reclamation actually happens, to decide whether the spot strategy is working

## When not to use it

- no spot instances
- a node termination handler already covers it. On EKS the AWS Node Termination Handler both
  detects and **acts** — cordon and drain — which is more useful than a metric alone

## The distinction worth making

| Need | Tool |
|---|---|
| Know it happened, and count it | this exporter |
| **Do something about it** — drain gracefully | a node termination handler |
| Understand the price landscape | [spot-price-exporter](../spot-price-exporter/README.md) |

Detection without action is only half the answer. The metric explains the incident; the
handler prevents it.

## Note on the project

Banzai Cloud is no longer active in its original form. On managed Kubernetes the provider's own
termination handler is usually the better maintained path — worth checking what the platform
already provides before deploying this.

---

[← Exporters](../README.md)
