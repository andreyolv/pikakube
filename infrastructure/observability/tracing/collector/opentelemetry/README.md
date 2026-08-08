[← Collectors](../README.md)

# OpenTelemetry Collector

<https://github.com/open-telemetry/opentelemetry-collector>
<https://github.com/open-telemetry/opentelemetry-collector-contrib>
<https://github.com/open-telemetry/opentelemetry-helm-charts>
<https://github.com/open-telemetry/opentelemetry-operator>

---

## The problem it solves

The vendor-neutral pipeline for all telemetry. Receive in many formats, process, export to many
destinations — with the application only ever knowing about one endpoint.

Its architecture is three stages, and understanding them is most of the tool:

| Stage | What it does |
|---|---|
| **Receivers** | accept telemetry — OTLP, Prometheus scrape, Jaeger, Zipkin, Fluent Forward, and dozens more |
| **Processors** | batch, sample, filter, redact, enrich with Kubernetes metadata, limit memory |
| **Exporters** | send onward — any backend, and several at once |

## Why it is the integration point

Point applications at the collector and the backend becomes a **configuration** decision
rather than a code one. Evaluating a new platform means adding an exporter and comparing, with
production traffic, without touching a single service.

That is the property that makes OTLP adoption worth insisting on, and this is the component
that delivers it.

## Two distributions

| | `core` | `contrib` |
|---|---|---|
| Components | the stable, minimal set | everything, including vendor-specific receivers and exporters |
| Use | you know exactly what you need | almost always, in practice |

## The operator

The [operator](https://github.com/open-telemetry/opentelemetry-operator) is worth knowing
about for a second reason beyond managing collectors: it performs **auto-instrumentation
injection**, adding the language agent to a pod through an annotation.

For Java, Python, Node.js and .NET that means tracing without touching the application image —
which is often the difference between instrumenting a fleet and not.

---

## Notes

- Example project: <https://github.com/yuriolisa/pes-2023-opentelemetry>
- <https://github.com/google/sqlcommenter> — propagates trace context **into SQL comments**, so a slow query in the database can be traced back to the request that issued it. A genuinely useful trick for a data platform, and one of the few ways to see past the database boundary.

Subfolders: [`opentelemetry-collector/`](opentelemetry-collector/) ·
[`opentelemetry-operator/`](opentelemetry-operator/) ·
[`opentelemetry-demo/`](opentelemetry-demo/)

---

[← Collectors](../README.md)
