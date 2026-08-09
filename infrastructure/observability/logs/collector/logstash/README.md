[← Log collectors](../README.md)

# Logstash

<https://github.com/elastic/logstash>

---

## The problem it solves

The processing stage of the Elastic stack — the "L" in ELK. It ingests from many sources,
transforms through a filter pipeline (grok, mutate, enrichment, geoip), and writes to
Elasticsearch or elsewhere.

Its grok library is genuinely extensive, which matters when the input is **unstructured logs
from software you do not control** and a regex has to extract fields from a sentence.

## When to use it

- Elasticsearch or [OpenSearch](../../storage/opensearch/README.md) is the destination, and the rest of the Elastic tooling is already in place
- heavy parsing of unstructured legacy formats, where the grok pattern library saves real work
- an existing Logstash pipeline that works

## When not to use it

- **Kubernetes log shipping.** It runs on the JVM and is by far the heaviest option here — on a DaemonSet that cost is multiplied by every node
- greenfield anything — [Fluent Bit](../fluent/fluent-bit/README.md) for shipping, [Vector](../vector/README.md) for transformation
- resources are constrained

## If it has to be in the picture

Do not run it as the node agent. Use [Fluent Bit](../fluent/fluent-bit/README.md) as the DaemonSet and
Logstash as an **aggregator** behind it, so the JVM footprint is paid a few times instead of
once per node. Elastic's own guidance points the same way.

---

[← Log collectors](../README.md)
