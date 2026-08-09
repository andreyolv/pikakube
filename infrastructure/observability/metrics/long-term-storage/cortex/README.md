[← Long-term storage](../README.md)

# Cortex

<https://github.com/cortexproject/cortex>
<https://github.com/cortexproject/cortex-helm-chart>

---

## What it is

The original horizontally scalable, multi-tenant Prometheus backend, and the project
[Mimir](../mimir/README.md) was forked from in 2022. CNCF, still maintained, with the same core model:
Prometheus remote write into a distributed cluster with object storage behind it.

## When to use it

- there is an **existing Cortex deployment** that works
- CNCF governance is a requirement, which the fork does not have
- you specifically want the upstream project rather than the vendor-led continuation

## When not to use it

- starting fresh. Grafana's engineering effort went into Mimir after the fork, and for a new
  deployment that is where the momentum is — [Mimir](../mimir/README.md)
- a modest deployment, where [Thanos](../thanos/README.md) is far less to operate

## The context that decides it

The fork happened over licensing and direction. Both projects continue and are technically
close, but the practical situation is that most new deployments choose Mimir, and most Cortex
deployments are ones that predate the fork.

Mapped here because migrating off it is a real task that platform teams still face, and
because "which one and why" is a question worth having an answer to rather than discovering
mid-decision.

---

[← Long-term storage](../README.md)
