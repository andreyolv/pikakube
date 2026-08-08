[← Log storage](../README.md)

# Quickwit

<https://github.com/quickwit-oss/quickwit>
<https://github.com/quickwit-oss/helm-charts>

---

## The problem it solves

Log storage has historically forced a choice: **full-text search** with Elasticsearch and its
operational cost, or **cheap storage** with Loki and label-only search.

Quickwit refuses the trade. It provides real full-text search with **object storage as the
primary backend** — indexes live in S3, and the search nodes are stateless.

That has a consequence worth stating directly: there is no cluster of stateful nodes to
rebalance, no shard allocation to tune, no heap to size. Scaling search means adding stateless
pods.

## When to use it

- you need full-text search but cannot justify operating Elasticsearch
- storage cost is a real constraint and search quality is not negotiable
- stateless search nodes fit the platform model better than a stateful cluster
- it also ingests OTLP, so it can serve as a trace backend — worth knowing when comparing against [Tempo](../../../tracing/storage/tempo/)

## When not to use it

- Kubernetes debugging only, where you always know the service and the window — [Loki](../loki/) is simpler and enough
- you depend on the Elastic ecosystem's tooling and integrations
- sub-second search over very recent data is the requirement; object storage adds latency that an index on local disk does not have

## Why it is worth evaluating

This is the most interesting option in the folder precisely because it sits in the gap
everything else leaves open. When "Loki's search is not enough, but Elasticsearch is too much
to run" describes the situation — which it often does — this is the tool that was built for it.

---

[← Log storage](../README.md)
