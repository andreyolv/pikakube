[← Trace storage](../README.md)

# Jaeger

<https://github.com/jaegertracing/jaeger>
<https://github.com/jaegertracing/helm-charts>

---

## The problem it solves

The CNCF-graduated tracing backend, and for many teams the reference implementation of what a
tracing UI should do.

Its differentiator against [Tempo](../tempo/README.md) is **search**. Jaeger indexes spans, so you can
find traces without knowing an ID:

- all traces for a service and operation
- traces slower than a duration
- traces carrying a specific tag — a tenant, a customer, an error code
- comparison between two traces, to see what differs

That is the exploratory mode: you suspect something is wrong and go looking, rather than
following an identifier you already have.

## When to use it

- **searching traces without an ID** is a real workflow
- you want a mature, well-understood UI that people already know
- Grafana is not the centre of the stack, so Tempo's integration advantage does not apply

## When not to use it

- Grafana is the UI and logs carry `trace_id` — [Tempo](../tempo/README.md) is cheaper and links better
- storage cost matters and the index is hard to justify
- you want an APM platform rather than a trace store — [SkyWalking](../skywalking/README.md) or [`platforms/`](../../../platforms/README.md)

## Storage note

Jaeger stores in Cassandra, Elasticsearch or OpenSearch — which means **another stateful
system to operate**, and that is frequently the deciding factor against it. Tempo needs a
bucket; Jaeger needs a database.

Recent versions also support OTLP natively, so it fits the OpenTelemetry pipeline without a
translation layer.

---

[← Trace storage](../README.md)
