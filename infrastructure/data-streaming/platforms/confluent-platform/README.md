[← Platforms](../README.md)

# Confluent Platform

<https://docs.confluent.io/platform/current/overview.html>

Examples: [`examples/`](examples/)

---

## What it is

The commercial Kafka distribution, from the company founded by Kafka's creators. Kafka plus the
components that surround it, versioned and supported together:

| Component | What it is |
|---|---|
| Kafka | the brokers |
| **Schema Registry** | the reference implementation — see [`schema-registry/`](../../schema-registry/README.md) |
| **Kafka Connect** | the connector framework, with a large catalogue |
| ksqlDB | SQL over topics — [`processing/ksqldb/`](../../processing/ksqldb/README.md) |
| Control Center | the management UI |
| REST Proxy | HTTP access to Kafka |

The value is that these are tested together at specific versions, which is real work when
assembling them yourself.

## When to use it

- **support obligations** — someone accountable when the log stops
- Connect, Schema Registry and ksqlDB are all needed, and version-compatibility management is unwelcome
- an organisation that buys platforms rather than assembling them

## When not to use it

- **Strimzi already works**, which it does for most Kubernetes deployments, and it is free
- only the broker is needed — licensing a stack to use one component
- licensing terms conflict with the platform's position

## Licensing, which is the recurring issue

Components sit under different licences. Kafka is Apache; Schema Registry, ksqlDB and Control
Center are under the Confluent Community License, which restricts offering them as a service.

That is why [Karapace](../../schema-registry/karapace/README.md) and other Apache-licensed replacements
exist, and it is worth establishing early rather than at renewal.

## The realistic position

Most Kubernetes platforms run open-source Kafka with **Strimzi**, and reach for individual
components — a registry, a connector — as needed.

Confluent makes sense when support and integration are worth paying for, or when Connect's
connector catalogue is the deciding factor. It rarely makes sense as a way to get brokers.

---

[← Platforms](../README.md)
