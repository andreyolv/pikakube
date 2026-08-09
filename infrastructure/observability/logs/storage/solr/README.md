[← Log storage](../README.md)

# Apache Solr

<https://github.com/apache/solr>
<https://github.com/apache/solr-operator>

---

## What it is

A mature Apache search platform built on Lucene — the same engine underneath Elasticsearch —
with its own operator for Kubernetes.

Solr's centre of gravity has always been **application search**: product catalogues, document
search, faceted navigation. Log storage is something it can do rather than something it was
designed for.

## When to use it

- **Solr is already in the organisation** and the expertise exists
- the same cluster serves application search and logs are a secondary consumer
- Apache governance is a requirement for the search layer

## When not to use it

- choosing fresh for logs. [Loki](../loki/README.md), [Quickwit](../quickwit/README.md) and
  [OpenSearch](../opensearch/README.md) are all better matches for log-shaped workloads, and each has a
  larger community for that use case
- you want Kubernetes-native log tooling with ready dashboards and collectors

## The honest positioning

Mapped for completeness. Solr is a genuinely good search platform, and log storage is not what
it is best at — the time-series shape of logs, retention by age, and high-volume append-only
ingest are all things the purpose-built options handle better.

If it is here because it is already running, that is a legitimate reason. It is not the
choice to make from scratch.

---

[← Log storage](../README.md)
