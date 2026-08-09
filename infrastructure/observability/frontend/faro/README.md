[← Frontend observability](../README.md)

# Grafana Faro

<https://github.com/grafana/faro-web-sdk>
<https://github.com/grafana/faro>

---

## The problem it solves

Browser telemetry usually means adopting a separate product, with its own agent, storage and
UI, disconnected from the server-side stack.

Faro is a web SDK that emits **Real User Monitoring** data — page load timings, Core Web
Vitals, JavaScript errors, user sessions, and frontend traces — into the same OpenTelemetry
and Grafana pipeline everything else already uses.

The payoff is correlation: a slow page in the browser links to the trace of the backend call
behind it, in one timeline.

## When to use it

- there is a user-facing UI, and server metrics do not explain complaints about speed
- Grafana is already the visualisation layer, so the data lands where people look
- you want frontend spans continuous with backend traces

## When not to use it

- there is no frontend
- you are not prepared to handle sampling and data scrubbing — browser telemetry is high volume and can carry personal data

## Note on collection

Faro data reaches the stack through a collector endpoint, so the
[OpenTelemetry Collector](../../tracing/collector/opentelemetry/README.md) or
[Alloy](../../tracing/collector/alloy/README.md) is part of the setup rather than an optional extra.

---

[← Frontend observability](../README.md)
