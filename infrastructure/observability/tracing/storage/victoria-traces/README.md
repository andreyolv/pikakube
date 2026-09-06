[← Trace storage](../README.md)

# VictoriaTraces

<https://github.com/VictoriaMetrics/VictoriaTraces>
<https://github.com/VictoriaMetrics/helm-charts>

---

## The problem it solves

A trace backend built on the [VictoriaLogs](../../../logs/storage/victoria-logs/README.md)
storage engine, treating a span as what it already is — **a wide event with many fields**.

That framing is the whole idea. Spans are not a special data type; they are structured records
with high-cardinality attributes, which is exactly what the VictoriaLogs engine was built for.
So the backend inherits its properties: a single binary, no external dependency, no object
storage, indexed attributes, and low resource use.

It ingests **OTLP** and exposes the **Jaeger query API**, so the Jaeger UI and Grafana's Jaeger
datasource work against it without a new plugin.

## Where it sits in the folder's trade

[The distinction that organises this folder](../README.md#2-the-one-real-distinction-index-or-not)
is index-everything (Jaeger) versus index-almost-nothing (Tempo). VictoriaTraces is on the
indexed side — you can search by service, operation and attribute — but without the cost model
that usually comes with it, because the engine underneath is built for high-cardinality fields
rather than adapted to them.

The price is the same one as VictoriaLogs: storage is **local disk**, not S3. Tempo's cheap
long tail is an object-storage property, and this does not have it.

## When to use it

- you already run VictoriaMetrics, and increasingly VictoriaLogs — this is the third signal in
  the same operational model, with one vendor and one way of running things
- you want Jaeger-style search without operating Elasticsearch or Cassandra behind Jaeger
- resource footprint is a real constraint

## When not to use it

- **it is young.** Announced in 2025 and moving fast; Tempo and Jaeger are what production
  deployments have been running for years. Verify the current maturity before committing
- Grafana is the stack and Tempo is already there — TraceQL and exemplar links are a tighter
  integration than the Jaeger API gives you
- object storage economics are the requirement for retention

## The honest position

The most interesting thing here is the argument, not the maturity: if a span is a wide event,
a log engine that handles wide events well is a reasonable trace store, and the separate
purpose-built trace database is less necessary than it looks.

Worth watching, and a natural choice inside a VictoriaMetrics stack. Elsewhere the point from
[`../README.md`](../README.md#1-the-easy-layer) still holds — the backend is the least important
decision in the tracing stack, and swapping it later is a collector configuration change.

---

[← Trace storage](../README.md)
