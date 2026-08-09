[← Redpanda](../README.md)

# Redpanda — Helm deployment

<https://github.com/redpanda-data/redpanda>
<https://github.com/redpanda-data/helm-charts>
<https://github.com/redpanda-data/connect>

---

## What this is

Deploying [Redpanda](../README.md) directly from the Helm chart, without an operator.

## When this shape fits

- a **single cluster** with a stable configuration
- GitOps, where the chart is a `HelmRelease` and values live in Git
- you would rather not run an operator for one cluster

## When it does not

- multiple clusters, or clusters created and destroyed frequently — [`redpanda-operator/`](../redpanda-operator/README.md)
- topics and users should be **Kubernetes resources** rather than managed out of band. That is the operator's main advantage

## What to set deliberately

| Setting | Why |
|---|---|
| **Storage class and volume size** | brokers are stateful; this is not easily changed later |
| Resource requests and limits | thread-per-core means CPU allocation directly determines throughput |
| Replication factor | three for anything that matters |
| TLS and authentication | on from the start, not retrofitted |
| Retention | per topic, and as a policy — see [`../../README.md`](../../README.md#2-the-properties-that-decide-everything) |

The resource setting is worth understanding: Redpanda's architecture pins work to cores, so the
CPU allocation is not a limit it occasionally reaches — it is the shape of the system.

## Redpanda Connect

[connect](https://github.com/redpanda-data/connect) is the successor to
[Benthos](../../../processing/benthos/README.md), and it covers the stateless majority of streaming work
— routing, reshaping, enrichment — without a processing engine.

Worth deploying alongside rather than reaching for [Flink](../../../processing/flink/README.md) when the
job has no state.

---

[← Redpanda](../README.md)
