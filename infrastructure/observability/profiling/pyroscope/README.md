[← Profiling](../README.md)

# Grafana Pyroscope

<https://github.com/grafana/pyroscope>

---

## The problem it solves

Continuous profiling stored and queried like any other signal, and — the reason to pick it —
**inside Grafana**, alongside metrics, logs and traces.

That integration is the product. A latency spike on a dashboard leads to the trace, and the
trace leads to the flame graph of the function responsible, without leaving the tool or
correlating timestamps by hand.

Profiles arrive either from language SDKs or from eBPF via
[Grafana Alloy](../../tracing/collector/alloy/), so instrumentation is optional.

## When to use it

- Grafana is already the visualisation layer — this is the profiling option that lands where people look
- you want profiles linked from traces rather than stored separately
- comparing profiles over time to catch regressions

## When not to use it

- you are not in the Grafana ecosystem — [Parca](../parca/) is a cleaner standalone choice
- only one process needs investigating right now, where [`py-spy`](https://github.com/benfred/py-spy) is more direct

---

## Notes

Verify the Grafana plugin actually installed, from inside the container:

```bash
grafana cli plugins ls
```

Worth checking explicitly — a missing plugin looks like "no profiling data" rather than like a
plugin problem, and the [Grafana Operator cannot install app plugins](../../dashboards/grafana/grafana-operator/README.md).

---

[← Profiling](../README.md)
