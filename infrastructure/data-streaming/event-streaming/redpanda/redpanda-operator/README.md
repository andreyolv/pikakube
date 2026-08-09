[← Redpanda](../README.md)

# Redpanda Operator

<https://github.com/redpanda-data/redpanda>
<https://github.com/redpanda-data/console>
<https://github.com/redpanda-data/connect>
<https://github.com/redpanda-data/helm-charts>

---

## What it adds over the chart

The [Helm deployment](../redpanda/README.md) gives you a cluster. The operator makes the **things inside
it** Kubernetes resources:

| CRD | What it declares |
|---|---|
| `Redpanda` | the cluster itself |
| **`Topic`** | a topic, with partitions, replication and retention |
| **`User`** | a principal and its credentials |
| `Schema` | a registered schema |

That is the difference that matters. Without it, topics and users are created by a CLI or a
console — outside Git, unreviewed, and unreproducible on a rebuilt cluster.

With it, creating a topic is a pull request, and the cluster's contents are described in the
repository like everything else.

## When to use it

- **topics and users should be in Git** — the strongest argument
- multiple clusters, or clusters recreated regularly
- self-service: teams declare their own topics with review, rather than filing a request

## When not to use it

- one static cluster where topics rarely change
- you already manage topics through another mechanism and do not want two

## Why this matters for governance

Kafka topic governance is usually a wiki page and good intentions. Declaring topics as
resources means naming conventions, retention policy and access can be enforced by
[Kyverno](../../../../security/2-cluster/policies/kyverno/) or by review — the same way every
other resource in the cluster is governed.

This repository already does topic and user governance for Kafka with Strimzi. The operator
model is what makes that possible, and it is the same argument here.

## Console

[Console](https://github.com/redpanda-data/console) works against Kafka as well as Redpanda, and
is one of the better Kafka UIs available. See
[`platforms/`](../../../platforms/README.md) — the missing management interface is a real gap in
this repository, and this is a low-cost way to close it.

---

[← Redpanda](../README.md)
