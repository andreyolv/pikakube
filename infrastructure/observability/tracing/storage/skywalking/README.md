[← Trace storage](../README.md)

# Apache SkyWalking

<https://github.com/apache/skywalking>
<https://github.com/apache/skywalking-helm>
<https://github.com/apache/skywalking-swck>

---

> **Not really a trace store.** SkyWalking is an APM platform: traces, metrics, service
> topology, alerting and a UI in one product. It is filed here because it stores traces, but
> it should be compared against [`platforms/`](../../../platforms/README.md), not against
> Tempo and Jaeger.

## The problem it solves

An Apache-governed observability platform with its own agents, its own analysis engine
(OAL), automatic service topology, and alerting — covering with one product what the
best-of-breed path assembles from four.

Its strength is the **JVM ecosystem**: the Java agent is mature and instruments a large set of
frameworks automatically, with more depth than generic auto-instrumentation typically reaches.

## When to use it

- a **Java-heavy** estate, where the agent's coverage is a real advantage
- you want an APM platform rather than a trace backend, and prefer Apache governance
- service topology and alerting should come from the same product as the traces

## When not to use it

- you are assembling a best-of-breed stack — this replaces several layers, and mixing produces two overlapping systems
- OpenTelemetry is the standard you are committing to. SkyWalking accepts OTLP, but its own agents and analysis are the reason to pick it, and using it purely as an OTLP sink wastes what it is for
- the estate is not JVM-centric, which removes the main differentiator

## Related

`skywalking-swck` is the Kubernetes operator, covering deployment and Java agent injection.

For the platform comparison this really belongs to, see
[`platforms/opentelemetry/`](../../../platforms/opentelemetry/README.md) — SigNoz occupies a
similar position with OTLP as the native input rather than proprietary agents.

---

[← Trace storage](../README.md)
