[← Integration](../README.md)

# Apache InLong

<https://github.com/apache/inlong>
<https://inlong.apache.org/>

---

## What it is

An Apache **integration platform** rather than a connector tool — originating at Tencent for
very large-scale ingestion, and covering the whole path: collection, aggregation, transport,
sorting and delivery.

Its scope is broader than the other tools in this folder:

| Layer | What InLong provides |
|---|---|
| Collection | agents on hosts, file and log collection, database CDC |
| Transport | its own message queue layer, or Kafka/Pulsar |
| Sorting | routing and light transformation before delivery |
| Management | a UI and API for defining data streams as governed objects |

That last row is the distinguishing idea: a data stream is a **registered, governed object**
with an owner and a lifecycle, not a pipeline someone configured.

## When to use it

- very large-scale ingestion, at the volume the project was built for
- ingestion should be a **governed capability** — teams register streams, the platform operates them
- you want collection agents and transport managed by the same system

## When not to use it

- a modest number of pipelines — this is a platform, and the overhead is real
- connector breadth is the requirement — [Airbyte](../airbyte/README.md) has far more sources
- the estate is not already Apache-ecosystem-oriented

## The honest positioning

Mapped for completeness and for the model it represents rather than as a likely choice.
Documentation and community outside China are thinner than for the alternatives, which matters
when something goes wrong.

The idea worth taking from it, independent of the tool: **treating a data stream as a
registered object with an owner** is a governance pattern, and it applies whichever ingestion
tool is used. That thinking belongs with
[`data-governance/`](../../../data-governance/README.md).

---

[← Integration](../README.md)
