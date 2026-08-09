[← Exporters](../README.md)

# Custom exporter

An example of writing your own, for the case where none of the existing ones fit.

Code: [`app/`](app/)

---

## When writing one is justified

Rarely. The [official exporter list](https://prometheus.io/docs/instrumenting/exporters/) is
long, and [sql-exporter](../sql-exporter/README.md) covers anything reachable by a query, which is more
than people expect.

The genuine cases:

- an **internal system** with an API and no exporter — a legacy service, an in-house scheduler, a vendor appliance
- a **custom resource** whose status matters. Though [kube-state-metrics](../../collector/kube-state-metrics/README.md) can expose CRDs without any code
- **business metrics** that require logic, not just a query

## What writing one involves

Less than it sounds. A client library, a metric definition, a handler:

1. pick the library for your language — `prometheus/client_python`, `client_golang`
2. define metrics with the right type — counter, gauge, histogram
3. serve `/metrics` over HTTP
4. add a `ServiceMonitor` so Prometheus discovers it

The code is straightforward. The **modelling** is where exporters go wrong.

## The three mistakes

**Wrong metric type.** A counter only goes up and is used with `rate()`. A gauge goes both
ways. Using a gauge for a count of events makes every rate calculation wrong, and it is not
obvious from the graph.

**Cardinality.** A label with unbounded values takes Prometheus down — see
[cardinality](../../README.md#3-cardinality-is-the-whole-game). This is the most common way a
custom exporter causes an incident.

**Expensive collection on scrape.** The handler runs on every scrape, from every Prometheus
replica. If it queries a slow API, the exporter becomes load on the system it observes. Cache
the result and refresh it on your own schedule.

## Before writing one

Check, in order: the official list, [sql-exporter](../sql-exporter/README.md), and whether
kube-state-metrics can expose the CRD. One of those covers most cases, and none of them
require code you then have to maintain.

---

[← Exporters](../README.md)
