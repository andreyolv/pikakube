[← OpenTelemetry platforms](../README.md)

# SigNoz

<https://github.com/SigNoz/signoz>
<https://github.com/SigNoz/charts>

---

## The problem it solves

Metrics, logs and traces in **one backend**, ingested over OTLP and stored in ClickHouse, with
dashboards and alerting included.

It is the most complete open-source answer to "I do not want to run Prometheus, Loki, Tempo
and Grafana separately". One deployment replaces four, and correlation between signals works
because they share a store and identifiers rather than being joined after the fact.

## When to use it

- a small team where operating four systems is not realistic
- starting fresh with OpenTelemetry, and no Prometheus investment to preserve
- correlation between traces and logs is the recurring pain
- log volume is the cost driver — columnar storage is usually cheaper per GB

## What is not open source

Same catch as [OpenObserve](../openobserve/README.md), one step milder. The community edition
does ship user management — invite-based accounts and three fixed roles (admin, editor, viewer) —
so it is not the "one shared root password" situation. **But SSO is the paid line: SAML and
Google OAuth live in the `ee/` directory under the SigNoz Enterprise License, not in the
Apache-licensed core.**

So self-hosting means:

- **no identity provider integration** — accounts are created by invite and live only in SigNoz,
  which means offboarding someone is a manual step in yet another system
- **roles are coarse and fixed** — no custom permissions, no per-team scoping of what a viewer can see
- the authentication story is exactly the piece you cannot fix yourself, because it is the piece
  that is not open

The engine is genuinely open and genuinely good. Access control is where the funnel is, and it is
worth pricing that in before treating this as "the open-source replacement for four systems".

## When not to use it

- **SSO or an identity provider is mandatory** — that requires the enterprise license
- **Prometheus is entrenched.** PromQL, recording rules, alerting rules and community dashboards represent a large sunk investment that does not transfer
- you need long-term metric retention at scale — [Thanos](../../../metrics/long-term-storage/thanos/README.md) and [Mimir](../../../metrics/long-term-storage/mimir/README.md) are purpose-built
- Grafana's dashboard ecosystem is load-bearing

## Migration note

Because ingestion is OTLP, adopting it is a **collector configuration change**, not a
re-instrumentation. Running the [OpenTelemetry Collector](../../../tracing/collector/opentelemetry/README.md)
in front means you can send the same telemetry to SigNoz and to an existing stack in parallel
while evaluating — which is the cheap way to make this decision with evidence.

---

[← OpenTelemetry platforms](../README.md)
