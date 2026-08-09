[← eBPF auto-instrumentation](../README.md)

# Grafana Beyla

<https://github.com/grafana/beyla>

---

## The problem it solves

Auto-instrumentation via eBPF that emits **standard OpenTelemetry** — spans and RED metrics
(rate, errors, duration) in OTLP, plus Prometheus metrics, from applications with no SDK.

The output format is what distinguishes it from the eBPF platforms in
[`platforms/ebpf/`](../../../../platforms/ebpf/README.md). Those produce telemetry for their
own backend. Beyla produces telemetry for **yours** — it drops into an existing OTLP pipeline
and the traces land in Tempo, Jaeger or anywhere else alongside SDK-instrumented services.

Language-agnostic by construction: Go, Java, Python, Node.js, Rust, .NET, and anything else,
because it observes the kernel rather than the runtime.

## When to use it

- services that will not be instrumented, and you want them on the **same** traces as those that are
- immediate RED metrics per service with no code change
- a first step toward tracing, before committing to an instrumentation project

## When not to use it

- business context is the requirement — eBPF stops at the process boundary
- you want a full platform rather than a telemetry source — [Coroot](../../../../platforms/ebpf/coroot/README.md) or [Pixie](../../../../platforms/ebpf/pixie/README.md)
- kernel versions are old or inconsistent across the fleet

## Where it fits

It is now part of the OpenTelemetry project's auto-instrumentation effort, which makes it the
most standards-aligned option in this folder — and the safest one to adopt without creating a
dependency you have to unwind later.

Pairs naturally with [Alloy](../../../collector/alloy/README.md), which can run it as a component
rather than as a separate deployment.

---

[← eBPF auto-instrumentation](../README.md)
