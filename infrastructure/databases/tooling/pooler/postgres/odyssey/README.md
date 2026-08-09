[← PostgreSQL poolers](../README.md)

# Odyssey

<https://github.com/yandex/odyssey>

---

## The problem it solves

A multi-threaded connection pooler, from Yandex, built for connection counts where
[PgBouncer](../pgbouncer/README.md)'s single-threaded process becomes the bottleneck.

It is the narrowest entry in this folder, and its argument is correspondingly narrow: same job as
PgBouncer, more cores, proven at a scale most deployments will never reach.

| Property | Detail |
|---|---|
| Written in | C |
| **Threading** | **multi-threaded**, with a configurable worker count |
| Pool modes | session and transaction |
| Origin | Yandex, running it in production at their scale |
| Per-route configuration | pools, limits and auth defined per user/database route |
| TLS | supported on both sides |
| Ecosystem | **small** — the main cost |

## When to use it

- PgBouncer's single-threaded model is a **measured** limit, not a suspected one
- running several PgBouncer instances behind a Service is unattractive for a specific reason
- very high connection counts, where per-connection overhead matters

## When not to use it

- **almost every other case.** [PgBouncer](../pgbouncer/README.md) is the default, and the bar for
  choosing something else is a capability it lacks
- routing is what is wanted — read/write splitting or load balancing across replicas —
  [PgCat](../pgcat/README.md) does that and this does not
- a database operator manages the deployment; the integrations are PgBouncer's
- the ecosystem matters: fewer people have run it, and there is less written about what goes wrong

## The honest framing

Odyssey solves one problem well and nothing else.

The decision tree in [`../README.md`](../README.md#decision-tree) puts it behind a question worth
being strict about: *is single-threaded a **measured** limit?* Usually it is not — a PgBouncer
instance handles a large workload, and horizontal replicas are cheap on Kubernetes, so the
constraint people expect to hit rarely arrives.

Where Odyssey genuinely wins is the case where multiplying PgBouncer instances is itself the
problem: each one holds its own pool of backend connections, so N instances mean N × `pool_size`
connections to the database. Scaling PgBouncer horizontally therefore works against the thing a
pooler exists to do, and past a point one multi-threaded process is the cleaner answer.

That is a real argument and it applies at a scale worth confirming with numbers first.

## Notes

Only the upstream repository was recorded for this folder — <https://github.com/yandex/odyssey> —
with no chart reference, unlike [PgBouncer](../pgbouncer/README.md) and
[PgCat](../pgcat/README.md), which both have one.

That absence is itself informative in a GitOps repository: no published chart means either a
hand-written Deployment or building one, which is friction that the alternatives do not have. Worth
confirming current packaging before planning around it.

The provenance consideration recorded for [YDB](../../../../distributed/newsql/ydb/README.md)
applies here too and should be stated plainly rather than avoided: for some organisations, adopting
infrastructure originating from a Russian company is a procurement decision made outside
engineering. That is a real constraint on adoption regardless of the software's quality, and a
catalogue that omits it is less useful.

**For this platform it is not the recommendation**, and the reason is the same as everywhere in
this folder: [CloudNativePG](../../../../sql/postgresql/operator/cnpg/README.md) integrates
PgBouncer through a `Pooler` resource, which makes it a small amount of YAML rather than a component
to package and operate.

Odyssey is catalogued as the answer to a question this platform is not asking — and as the reason
to *measure* PgBouncer's CPU before assuming its threading model is a problem.

---

[← PostgreSQL poolers](../README.md)
