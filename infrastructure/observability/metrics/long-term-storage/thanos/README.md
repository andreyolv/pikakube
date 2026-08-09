[← Long-term storage](../README.md)

# Thanos

<https://github.com/thanos-io/thanos>

---

## The problem it solves

Extends existing Prometheus instances with unlimited retention and a global query view,
**without changing how they run**.

A sidecar next to each Prometheus uploads completed blocks to object storage. A querier then
presents recent local data and historical object-storage data as a single PromQL endpoint —
across every cluster at once.

The sidecar model is the reason it is usually the first choice: nothing about the existing
Prometheus deployment has to change.

## Components worth knowing

| Component | Job |
|---|---|
| **Sidecar** | uploads blocks; serves recent data from the local Prometheus |
| **Store Gateway** | serves historical blocks from object storage |
| **Querier** | fans out to sidecars and store gateways, deduplicates, presents one endpoint |
| **Compactor** | merges blocks and downsamples — the component that makes long queries affordable |
| **Ruler** | evaluates rules against the global view rather than one cluster |

## When to use it

- Prometheus is already deployed and retention or a global view is now needed
- multiple clusters that must be queried together
- you want the least invasive path from where you are

## When not to use it

- very large scale with multi-tenancy — [Mimir](../mimir/README.md) is designed for that shape
- cardinality and cost are the underlying problem — [VictoriaMetrics](../../storage/victoria-metrics/README.md) addresses both layers at once
- retention is not actually a requirement yet; this is several components to operate

## Operational note

**The compactor is not optional.** Without it, blocks accumulate un-merged and un-downsampled,
queries over long ranges become slow, and storage grows far faster than expected.

It also must run as a **single instance per bucket** — two compactors on the same bucket
corrupt data. This is the mistake worth knowing about in advance.

Known issue: <https://github.com/thanos-io/thanos/issues/8285>

Object storage backend on a local cluster: [MinIO](minio/README.md)

---

[← Long-term storage](../README.md)
