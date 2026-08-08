[← Log storage](../README.md)

# Elastic Cloud on Kubernetes (ECK)

<https://github.com/elastic/cloud-on-k8s>

---

## The problem it solves

Running Elasticsearch on Kubernetes by hand means managing StatefulSets, PVCs, rolling
restarts, certificates and version upgrades of a stateful distributed database — one of the
harder things to operate correctly.

ECK is Elastic's operator for it: `Elasticsearch`, `Kibana` and `Beats` become CRDs, with the
operator handling orchestration, safe upgrades and TLS.

## When to use it

- **full-text search is genuinely required** — security investigation, compliance search, or analytics over log content
- the Elastic ecosystem is already in place, with Kibana and its tooling
- you have the capacity to operate a search cluster

## When not to use it

- Kubernetes debugging is the actual use case. You almost always arrive knowing the service and the time window, and [Loki](../loki/) matches that at a fraction of the cost
- operational capacity is limited — shards, replicas, heap and rebalancing are real ongoing work
- full-text search matters but running a cluster does not appeal — [Quickwit](../quickwit/) covers that middle ground

## The cost reality

The index is frequently **larger than the data it indexes**. That is the price of fast
full-text search, and it is worth being explicit about before committing, because it is the
line item that surprises people.

---

## Notes

Done in this repository:

- **Central log repository for the cluster.**
- **Curator CronJob** for cleaning up old logs in Elasticsearch, with a retention policy of *N* days.

Retention is not optional here. Without an explicit cleanup job, indices accumulate until the
cluster runs out of disk — and Elasticsearch degrades badly rather than failing cleanly when
that happens.

Related folders: [`curator/`](curator/) · [`stack/`](stack/)

---

[← Log storage](../README.md)
