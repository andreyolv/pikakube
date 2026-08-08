[← Long-term storage](../README.md)

# Grafana Mimir

<https://github.com/grafana/mimir>

---

## The problem it solves

Long-term, horizontally scalable metrics storage built for very large scale and
**multi-tenancy** — fed by Prometheus **remote write** rather than by a sidecar.

That difference in ingestion is the main architectural distinction from
[Thanos](../thanos/): Prometheus becomes a forwarder, and Mimir owns storage, querying and
rule evaluation centrally.

Multi-tenancy is native rather than bolted on — separate limits, retention and isolation per
tenant, which is what a platform team needs when several teams share one metrics system.

## When to use it

- very large scale, where the sidecar model stops being comfortable
- **multi-tenant** metrics with per-tenant limits and isolation
- Grafana is the stack, and Loki and Tempo are already deployed with similar architecture
- you want centralised rule evaluation rather than per-cluster

## When not to use it

- a modest deployment — it is a distributed system with many components, and [Thanos](../thanos/) reaches the same result with less
- Prometheus should stay authoritative locally; remote write inverts that relationship
- cardinality and resource cost are the actual problem — [VictoriaMetrics](../../storage/victoria-metrics/)

## Thanos or Mimir

| | Thanos | Mimir |
|---|---|---|
| Ingestion | sidecar uploads blocks | Prometheus remote write |
| Prometheus role | stays authoritative locally | becomes a forwarder |
| Multi-tenancy | limited | native |
| Adoption cost | low — add a sidecar | higher — a cluster to operate |
| Best at | extending what exists | large, multi-tenant, centralised |

Both work. The decision is usually **how invasive the change may be**, not which is
technically superior — Thanos extends, Mimir centralises.

## Operational note

Mimir's components share the same architectural pattern as Loki and Tempo. If any of those are
already deployed, the operational knowledge transfers — which is a real, underrated reason to
prefer it in a Grafana-centric platform.

---

[← Long-term storage](../README.md)
