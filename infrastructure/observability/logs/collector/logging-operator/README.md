[← Log collectors](../README.md)

# Logging Operator

<https://github.com/kube-logging/logging-operator>

---

## The problem it solves

A central log pipeline has a central configuration file, and every team that wants their logs
routed somewhere specific has to ask the platform team to edit it. That file grows, drifts,
and becomes something nobody wants to touch.

The Logging Operator (CNCF) makes routing **namespace-scoped and declarative**: a team creates
a `Flow` and an `Output` in their own namespace, describing how their logs are filtered and
where they go, without access to anyone else's configuration.

| Resource | Scope | Owner |
|---|---|---|
| `Logging` | cluster | platform team — the collector deployment itself |
| `ClusterFlow` / `ClusterOutput` | cluster | platform team — defaults for everyone |
| `Flow` / `Output` | namespace | **application team** — their own routing |

## When to use it

- **multi-tenant clusters** where teams need different destinations, filters or retention
- log routing should be self-service rather than a ticket
- you want the collector configuration reviewed as code, per namespace

## When not to use it

- a single pipeline to a single destination — [Fluent Bit](../fluent/fluent-bit/) alone is far less to run
- one team owns everything, which removes the delegation benefit that justifies the operator

## The comparison worth making

[Fluent Operator](../fluent/fluent-operator/) also turns Fluent configuration into CRDs. The
difference is intent: Fluent Operator manages the Fluent stack, while the Logging Operator is
built around **tenant self-service** as the primary use case. If delegation is the reason you
are looking, this is the one designed for it.

---

[← Log collectors](../README.md)
