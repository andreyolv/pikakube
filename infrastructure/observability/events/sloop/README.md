[← Events](../README.md)

# Sloop

<https://github.com/salesforce/sloop>

---

## The problem it solves

The hardest question in Kubernetes debugging is about something that **no longer exists**:
what happened to that pod before it disappeared? `kubectl describe` cannot answer it — the
object is gone, and the events expired an hour ago.

Sloop records the history of Kubernetes objects and events over time and presents it visually.
You can look at a deleted pod and see its whole lifecycle: created, scheduled, image pulled,
started, killed, recreated.

## When to use it

- reconstructing incidents involving pods that are already gone
- watching how a Deployment behaved across a rollout
- a cluster where things churn constantly and `kubectl` only ever shows the present

## When not to use it

- you only need events routed to a log store — [kubernetes-event-exporter](../kubernetes-event-exporter/) is simpler
- storage is tight; it keeps its own history

## Why it is worth knowing about

Most tools here move events somewhere. Sloop is the only one that reconstructs a **timeline
of an object**, which is a different and often more useful thing during a post-mortem.

---

[← Events](../README.md)
