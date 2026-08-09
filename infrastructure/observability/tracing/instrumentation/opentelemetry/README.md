[← Instrumentation](../README.md)

# OpenTelemetry SDKs

<https://github.com/open-telemetry/opentelemetry-specification>
<https://github.com/open-telemetry/opentelemetry-python>
<https://opentelemetry.io/docs/languages/>

---

## What this is

The standard itself: a specification, plus SDKs for every mainstream language, defining how
telemetry is produced and what its fields mean.

Three parts matter:

| Part | What it gives you |
|---|---|
| **API and SDK** | create spans, metrics and logs in code |
| **OTLP** | one wire protocol, accepted by every backend in this repository |
| **Semantic conventions** | agreed names — `http.request.method`, `db.system`, `service.name` — so telemetry from different services is comparable |

The semantic conventions are underrated. They are what makes a dashboard written for one
service work for another, and what lets a backend understand your data without configuration.

## Automatic instrumentation first

Most languages have a zero-code path: a Java agent, `opentelemetry-instrument` for Python, a
Node.js require hook. It instruments known frameworks and libraries — HTTP servers and
clients, database drivers, message queues — with no source change.

```bash
# Python, as an example: no code modification
opentelemetry-instrument python app.py
```

In Kubernetes the [operator](../../collector/opentelemetry/README.md) can inject this through a pod
annotation, which means instrumenting a fleet without rebuilding images.

Start there. Add manual spans afterwards, only where the automatic picture is insufficient.

## What to add manually, when you do

Not more spans — **attributes**. An automatic span says the service took 300ms. A useful span
says which tenant, which endpoint, which query, which batch size.

That is the difference between "the service is slow" and "the service is slow for this
customer's largest dataset", and it is the part no agent can infer.

## The decision this represents

Instrumenting with OpenTelemetry rather than a vendor SDK is the one choice in
[`tracing/`](../../README.md) worth being firm about. It costs nothing extra at the start, and
it is what keeps every backend decision reversible afterwards.

---

[← Instrumentation](../README.md)
