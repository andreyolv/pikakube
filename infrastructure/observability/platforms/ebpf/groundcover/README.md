[← eBPF platforms](../README.md)

# groundcover

<https://github.com/groundcover-com/helm-charts>

---

> **Commercial.** The repository here is the Helm chart; the platform is a paid product.

## The problem it solves

An eBPF observability platform whose distinguishing claim is **BYOC** — bring your own cloud.
The agents and the data plane run in your infrastructure, and only the control plane and UI
are the vendor's.

That addresses the objection that usually blocks a SaaS platform: telemetry, including logs
with credentials and personal data, never leaves your environment.

The pricing model follows from it — by node rather than by ingest volume, which removes the
usual surprise where log growth outpaces the budget.

## When to use it

- a commercial platform is acceptable but **data residency is not negotiable**
- ingest-based pricing has already burned you, or is projected to
- you want eBPF coverage with vendor support behind it

## When not to use it

- open source is a requirement — [Coroot](../coroot/) is the closest equivalent
- you are prepared to run the stack yourself; you would be paying for operations you can absorb

## What to check before adopting

The BYOC boundary is the whole value proposition, so verify it precisely: **which data
actually reaches the control plane** — metadata, aggregates, or samples of the telemetry
itself. "Data stays in your cloud" is a spectrum, and the details decide whether it satisfies
your constraint.

---

[← eBPF platforms](../README.md)
