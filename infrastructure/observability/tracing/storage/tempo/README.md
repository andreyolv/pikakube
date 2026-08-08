[← Trace storage](../README.md)

# Grafana Tempo

<https://github.com/grafana/tempo>
<https://github.com/grafana/tempo-operator>

---

## The problem it solves

Trace backends traditionally index spans by service, operation, tags and duration so you can
search for a trace. That index is expensive, and it grows with span volume.

Tempo indexes **almost nothing** and stores traces in object storage. Cost drops by an order
of magnitude, and lookup by **trace ID** stays instant.

The design bet is that you rarely search blind — you arrive with an identifier from a log
line, an exemplar on a latency graph, or an alert. **TraceQL** then covers the cases where
you do need to search, by scanning a bounded window rather than consulting an index.

## When to use it

- **the default in a Grafana stack** — metric exemplars link straight to traces, and logs link back
- trace storage cost is a concern
- object storage is available, or [MinIO](../../../logs/storage/loki/minio/) is acceptable

## When not to use it

- you routinely need to find traces **without** an ID — "all slow requests to this endpoint last week" is what [Jaeger](../jaeger/) is better at
- logs do not carry `trace_id`. Without it the model does not work, because nothing hands you the identifier

## The prerequisite nobody mentions

Tempo's economics depend on **arriving with a trace ID**. That requires:

- `trace_id` in structured logs — see [logs](../../../logs/README.md#4-structured-logging)
- exemplars enabled in Prometheus, so metric graphs link to traces

Deploy Tempo without those and it becomes a store you cannot navigate. They are the actual
prerequisite, not the Helm chart.

---

## Notes

- Example Helm setup: <https://github.com/grafana/tempo/tree/main/example/helm>
- <https://github.com/grafana-community/helm-charts>

Try a first query at `http://localhost:3000/explore` with the simplest TraceQL there is:

```
{}
```

That returns recent traces and confirms the pipeline end to end — which is worth doing before
assuming instrumentation is at fault.

---

[← Trace storage](../README.md)
