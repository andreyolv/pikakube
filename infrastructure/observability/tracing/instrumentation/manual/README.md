[← Instrumentation](../README.md)

# Manual instrumentation

Examples of emitting each signal from application code with the OpenTelemetry SDKs.

Subfolders: [`tracing/`](tracing/) · [`metrics/`](metrics/) · [`logs/`](logs/)

---

## Why all three signals are here

OpenTelemetry is not a tracing library that grew. The SDKs emit **traces, metrics and logs**
over the same protocol, with the same resource attributes and the same context.

That is the practical reason to adopt OTLP rather than a tracing-specific SDK: a log written
through the SDK carries the **`trace_id` automatically**, and a metric recorded inside a span
can carry an exemplar pointing back to it.

The correlation between signals stops being something you engineer and becomes something you
get.

## When manual instrumentation is worth it

[Automatic instrumentation](../opentelemetry/README.md) covers the mechanical part — HTTP handlers,
database drivers, queue clients. It cannot know anything about your domain.

Add manual instrumentation for:

| What | Example |
|---|---|
| **Business attributes** | tenant, customer, plan, dataset, batch size |
| **Meaningful units of work** | a pipeline stage, a transformation, a batch — spans that match how you think, not how the framework calls out |
| **Domain metrics** | rows processed, records rejected, queue depth |
| **Errors with context** | which record failed and why, not only that something threw |

The test for whether a span is worth adding: does it let you answer a question you currently
cannot? "Which tenant is slow" is a question. "This function was called" is not.

## The mistake to avoid

Instrumenting **more** rather than **better**. A trace with two hundred spans per request is
harder to read than one with twelve, costs more to store, and adds overhead to every call.

Automatic instrumentation for coverage, a small number of deliberate manual spans with good
attributes on top. Attributes are where the value is — not span count.

---

[← Instrumentation](../README.md)
