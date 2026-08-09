[← OpenTelemetry platforms](../README.md)

# HyperDX

<https://github.com/hyperdxio/hyperdx>
<https://github.com/hyperdxio/helm-charts>

---

## The problem it solves

An OTLP-native platform on ClickHouse, focused on the part of debugging that usually costs the
most time: **correlating a trace with the logs that belong to it**.

Its distinguishing feature is **session replay** alongside backend telemetry — the user's
browser session and the traces it produced, on one timeline. A bug report becomes "watch what
they did, then follow the trace it generated".

## When to use it

- there is a user-facing frontend and complaints need reproducing rather than guessing at
- correlating traces and logs is the recurring friction
- ClickHouse is already understood, or acceptable to run

## When not to use it

- there is no frontend, which removes the main differentiator — [SigNoz](../signoz/README.md) is more complete for backend-only
- metrics are the primary signal; the strength here is traces, logs and sessions

## Related

Session replay pairs naturally with [`frontend/`](../../../frontend/README.md) and
[Faro](../../../frontend/faro/README.md) — the same problem approached from the RUM side. Worth
deciding which one owns browser telemetry rather than running both.

---

[← OpenTelemetry platforms](../README.md)
