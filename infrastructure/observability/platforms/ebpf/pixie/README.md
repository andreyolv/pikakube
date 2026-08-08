[← eBPF platforms](../README.md)

# Pixie

<https://github.com/pixie-io/pixie>

---

## The problem it solves

eBPF observability with a distinguishing feature the others lack: **PxL**, a scripting
language for querying live telemetry in the cluster.

Instead of a fixed set of dashboards, you write a short script against what the agents are
observing right now — full HTTP request bodies, database queries with their latency, DNS
resolution, CPU flame graphs — and get an answer immediately.

Data is processed and retained **in the cluster** by default, which matters when telemetry
cannot leave.

## When to use it

- ad-hoc deep inspection of live traffic: "show me every failing request to this service, with bodies"
- protocol-level visibility without instrumentation — HTTP, MySQL, PostgreSQL, DNS, Redis, Kafka
- data residency requirements make in-cluster processing a hard constraint

## When not to use it

- you want long retention and historical trends — it is oriented to recent data
- the team will not write scripts; the interactive power is the product, and unused it is heavy
- you want a turnkey service map with interpretation — [Coroot](../coroot/) fits that better

## A caution worth stating

Pixie can capture **full request payloads**. That is exactly why it is powerful for debugging,
and exactly why it needs a decision about scope before deployment — payloads carry
credentials and personal data.

---

[← eBPF platforms](../README.md)
