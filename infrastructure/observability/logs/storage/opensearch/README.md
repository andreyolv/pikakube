[← Log storage](../README.md)

# OpenSearch

<https://github.com/opensearch-project/OpenSearch>
<https://github.com/opensearch-project/OpenSearch-Dashboards>
<https://github.com/opensearch-project/helm-charts>
<https://github.com/opensearch-project/opensearch-k8s-operator>

---

## What it is

The Apache-2.0 fork of Elasticsearch, created by AWS after Elastic changed its licence in
2021. Same lineage, same query capability, same operational model — with OpenSearch Dashboards
in place of Kibana.

It is now a mature project in its own right rather than a fork tracking upstream, with
features Elastic does not have and vice versa.

## When to use it

- full-text search is required **and** the licence matters — Apache 2.0 removes the question entirely
- you are on AWS, where it is the managed offering
- an existing Elasticsearch deployment needs to move off the Elastic licence

## When not to use it

- Kubernetes debugging is the real use case — [Loki](../loki/README.md) is cheaper and fits how logs are actually consulted
- the operational cost of a search cluster is not available
- you want search without running a cluster — [Quickwit](../quickwit/README.md)

## Choosing between OpenSearch and Elastic

| | OpenSearch | [Elastic (ECK)](../elastic-operator/README.md) |
|---|---|---|
| Licence | Apache 2.0 | Elastic licence |
| Managed on AWS | yes, natively | via Elastic Cloud |
| Ecosystem | large, and growing independently | larger, longer established |
| Operator | `opensearch-k8s-operator` | ECK, generally more polished |

For most log use cases they are interchangeable. The decision is usually licensing and cloud
alignment rather than capability — which is worth saying plainly, because comparisons of the
two often imply a bigger technical gap than exists.

---

[← Log storage](../README.md)
