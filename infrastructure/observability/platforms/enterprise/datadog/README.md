[← Enterprise platforms](../README.md)

# Datadog

<https://github.com/DataDog/helm-charts/blob/main/charts/datadog-operator/values.yaml>
<https://docs.datadoghq.com/>

---

> **Commercial SaaS.** The agent runs in your cluster; the data lives in Datadog.

## What it is

The most widely deployed commercial observability platform: infrastructure metrics, APM,
logs, RUM, synthetics, security and cost — correlated, with nothing to operate.

Its breadth is genuine, and so is the reason teams choose it. There is no open-source
equivalent that covers the same surface with the same integration quality out of the box.

## When it is the right call

- observability is not where the team's time should go
- breadth on day one matters more than control
- someone else being accountable for it working is worth paying for

## What you are trading

| Dimension | Consequence |
|---|---|
| **Cost** | priced per host, per ingested GB and per retention tier — it grows with success, and **logs are the usual surprise** |
| **Data location** | telemetry leaves the cluster, including logs that carry credentials and personal data |
| **Lock-in** | proprietary agent, proprietary query language; migration means re-instrumenting unless you planned otherwise |
| **Control** | cardinality limits, retention and sampling are the vendor's decisions |

## The one decision that keeps the door open

**Instrument with OpenTelemetry, not the Datadog agent.**

Datadog accepts OTLP. Emitting OTLP through the
[OpenTelemetry Collector](../../../tracing/collector/opentelemetry/) means the instrumentation
in your code is vendor-neutral, and changing platform later is a collector configuration
change rather than a fleet-wide rewrite.

It costs essentially nothing now and is close to impossible to retrofit. This is the single
highest-leverage choice when adopting any commercial platform.

## The hybrid worth considering

Keep **critical alerting** on self-hosted Prometheus and Alertmanager, and let Datadog carry
everything else. Observability that fails during an incident is the failure mode that matters
most, and a paging path you own is cheap insurance.

---

## Notes

```bash
helm repo add datadog https://helm.datadoghq.com
helm install datadog-operator datadog/datadog-operator
```

---

[← Enterprise platforms](../README.md)
