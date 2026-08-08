[← Fluent family](../README.md)

# Fluent Operator

<https://github.com/fluent/fluent-operator>

---

## The problem it solves

Fluent Bit and Fluentd are configured through files. In Kubernetes that means a large
ConfigMap of inputs, parsers, filters and outputs — edited in place, drifting from Git, and
impossible to review meaningfully in a pull request.

Fluent Operator turns that configuration into **CRDs**:

| Resource | What it declares |
|---|---|
| `FluentBit` / `Fluentd` | the collector deployment itself |
| `ClusterInput` | what to collect |
| `ClusterFilter` | parsing, enrichment, dropping |
| `ClusterOutput` | where it goes |
| `Filter` / `Output` | the namespaced equivalents, for tenant self-service |

Configuration becomes reviewable, reconciled by Flux like everything else, and reproducible on
a rebuilt cluster.

## When to use it

- GitOps — collector configuration belongs in the repository, not in a mutable ConfigMap
- the configuration is large enough that reviewing a diff of it matters
- you run both Fluent Bit and Fluentd and want one control plane for the pair

## When not to use it

- a small static configuration that never changes — the operator is more machinery than the problem needs
- **tenant self-service is the primary goal** — the [Logging Operator](../../logging-operator/) is built around that case specifically

## Choosing between the two operators

| | Fluent Operator | Logging Operator |
|---|---|---|
| Built by | the Fluent project | kube-logging, CNCF |
| Primary intent | manage the Fluent stack declaratively | multi-tenant log routing as self-service |
| Choose it when | Fluent Bit and Fluentd are already the decision | delegation to namespace owners is the requirement |

---

[← Fluent family](../README.md)
