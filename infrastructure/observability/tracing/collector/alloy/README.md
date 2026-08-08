[← Collectors](../README.md)

# Grafana Alloy

<https://github.com/grafana/alloy>

---

## What it is

Grafana's distribution of the OpenTelemetry Collector — a superset rather than an alternative.
It includes the upstream components and adds the rest of the Grafana collection story in one
agent:

| Capability | Replaces |
|---|---|
| OTLP receive, process, export | the OTel Collector |
| Prometheus scraping and remote write | a Prometheus agent |
| Log collection to Loki | Promtail |
| eBPF profiling to Pyroscope | a separate profiling agent |

It is the successor to Grafana Agent, and its configuration language is declarative with
components wired into a pipeline.

## When to use it

- the stack is **Grafana** — one agent for metrics, logs, traces and profiles instead of four
- you want Promtail's replacement and an OTel collector without running both
- eBPF profiling into [Pyroscope](../../../profiling/pyroscope/) is part of the plan

## When not to use it

- vendor neutrality is the goal — the upstream [OpenTelemetry Collector](../opentelemetry/) is the neutral choice, and Alloy's extra value is Grafana-shaped
- you only need OTLP forwarding, where upstream is smaller and more portable

## The trade

Fewer agents to deploy and one configuration language, against a configuration format that is
Grafana's rather than the standard. The telemetry itself stays OTLP, so the lock-in is
operational rather than in the data — which is the milder kind.

---

## Notes

```bash
kubectl port-forward svc/alloy 12345
```

The UI on that port shows the component graph and each component's health — which is the
fastest way to find where a pipeline is silently dropping data.

---

[← Collectors](../README.md)
