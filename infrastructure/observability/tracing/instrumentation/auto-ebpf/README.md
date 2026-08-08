[← Instrumentation](../README.md)

# eBPF auto-instrumentation

Telemetry from applications nobody instrumented — and nobody is going to.

Tools covered: [`beyla`](beyla/)

---

## The problem it solves

Instrumentation requires touching code. There is always a service where that is not going to
happen: a third-party component, a legacy binary, something owned by a team with other
priorities, or something whose source nobody has.

eBPF observes the kernel — sockets, syscalls, protocol traffic — and reconstructs spans and
metrics from what it sees. No code change, no restart, no SDK.

## What it gives you, and what it cannot

| Gives | Cannot give |
|---|---|
| service-to-service calls and their latency | anything inside the process |
| HTTP, gRPC and database call timing | **business context** — tenant, customer, order |
| error rates from status codes | custom spans and attributes |
| a real dependency graph | visibility into encrypted traffic it cannot hook above |

The boundary is the process. eBPF sees that service A called service B and it took 300ms; it
cannot see which branch ran, which query plan was chosen, or which customer it was for.

## The sensible order

1. **eBPF everywhere** — immediate coverage, including everything nobody will instrument
2. **[OpenTelemetry SDKs](../opentelemetry/)** on the critical path — where business attributes and custom spans actually matter

Treating eBPF as a reason never to instrument is the mistake it invites. It is a floor, not a
ceiling.

## Practical constraints

| Constraint | Why it matters |
|---|---|
| Kernel version | eBPF capability varies, and older kernels lose features quietly |
| Privileges | agents run privileged on every node — a real security decision |
| mTLS | encrypted service-to-service traffic can blind the agent unless it hooks above encryption |

## Related

Full platforms built on the same idea live in
[`platforms/ebpf/`](../../../platforms/ebpf/README.md) — Coroot, Pixie and others. The
difference is scope: those replace the stack, this produces telemetry for the stack you
already run.

---

[← Instrumentation](../README.md)
