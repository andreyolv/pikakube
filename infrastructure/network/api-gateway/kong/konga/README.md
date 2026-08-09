[← Kong](../README.md)

# Konga

<https://github.com/pantsel/konga>

Admin UI for [Kong](../README.md).

---

> **Archived project.** No longer maintained, and limited to **PostgreSQL versions below 11**
> — which rules it out on any current database. Recorded here as historical reference, not as
> a candidate.

## What it was

A web UI for Kong's admin API: managing services, routes, consumers and plugins without
using the admin API directly. It was the common answer to "Kong has no interface" for years.

## What to use instead

| Need | Option |
|---|---|
| Official UI | Kong Manager, bundled with Kong |
| Declarative configuration | `decK`, or the [Kong Ingress Controller](../../../ingress-controller/kong-ingress/README.md) with CRDs |
| GitOps | define `KongPlugin` and `KongConsumer` as manifests — reviewable, versioned, no UI needed |

For a GitOps repository the third row is the honest answer: a UI that mutates state outside
Git is working against the model, whatever its condition.

---

[← Kong](../README.md)
