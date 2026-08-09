[← Event streaming](../README.md)

# Fluvio

<https://github.com/infinyon/fluvio>
<https://www.fluvio.io/>

---

## What it is

A streaming platform written in Rust, with a distinguishing feature none of the others here
have: **programmable processing inside the broker**, via WebAssembly.

SmartModules — filters, maps and aggregations compiled to WASM — run where the data is, so
simple transformations do not need a separate stream processor at all.

| Property | Detail |
|---|---|
| **Rust, no JVM** | very small footprint — tens of MB rather than gigabytes |
| **SmartModules** | WASM transformations executing in the cluster |
| Edge-oriented | small enough to run where a Kafka cluster cannot |
| Kafka-inspired | familiar concepts, but **not** protocol-compatible |

The last row matters: unlike [Redpanda](../redpanda/README.md) and [AutoMQ](../automq/README.md), Fluvio does not
speak the Kafka protocol. Existing clients do not connect.

## When to use it

- **edge and IoT**, where footprint is the constraint and Kafka is simply too large
- in-broker filtering removes the need for a separate processing tier
- Rust is the ecosystem, and WASM extensibility is attractive

## When not to use it

- **Kafka compatibility is required** — this is the decisive difference
- you want a large ecosystem of connectors and clients
- production dependence on a smaller, younger project

## The idea worth noting

Processing at the broker challenges an assumption this folder otherwise takes for granted: that
[event streaming](../README.md) and [processing](../../processing/README.md) are separate layers.

For genuinely simple transformations — filter, project, reshape — a separate processing tier is
a lot of machinery, and doing it in the broker removes a hop and a deployment. That is the same
instinct as [Bufstream](../bufstream/README.md) validating schemas at the broker.

Whether that is good architecture or coupling depends on how much logic ends up there — the
same question as [NiFi](../../../analytics-engineering/integration/nifi/README.md), one layer down.

---

[← Event streaming](../README.md)
