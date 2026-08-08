[← Trace storage](../README.md)

# Zipkin

<https://github.com/openzipkin/zipkin>
<https://github.com/openzipkin/zipkin-helm>

---

## What it is

The original distributed tracing system, from Twitter, and the project that made the idea
mainstream. Its data model and propagation headers (B3) shaped everything that followed,
including OpenTelemetry.

Still maintained, still simple, and still perfectly capable of storing and displaying traces.

## When to use it

- **minimal footprint** — it runs as a single service, and the in-memory mode needs no storage at all
- existing services already emit Zipkin format, or use B3 propagation
- development and testing, where you want a trace UI in one manifest

## When not to use it

- new production deployments — [Tempo](../tempo/) and [Jaeger](../jaeger/) have more capable UIs and better OpenTelemetry alignment
- large volumes, where the storage options are more limited than the alternatives

## Why it stays in the catalogue

Two reasons beyond history. It remains the easiest tracing backend to stand up for an
experiment, and **B3 propagation is still widely encountered** — plenty of services and
libraries emit it, and knowing where it comes from explains a lot of otherwise confusing
header configuration in OpenTelemetry setups.

---

[← Trace storage](../README.md)
