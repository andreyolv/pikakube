[← PostgreSQL operators](../README.md)

# StackGres

<https://github.com/ongres/stackgres>
<https://stackgres.io/doc/>

---

## What it is

The most **opinionated** of the operators here. StackGres does not just run Postgres — it
bundles the surrounding stack and ships it as one unit:

| Included | Which otherwise is |
|---|---|
| **PgBouncer** | a separate deployment you have to remember — see [`tooling/pooler/`](../../../../tooling/pooler/) |
| Envoy | a proxy in front, for observability and connection handling |
| Prometheus exporter | configured separately |
| Backup to object storage | configured separately |
| Extension management | installing extensions into images by hand |
| A web console | not usually available |

The extension handling is genuinely distinctive: extensions are declared and installed without
rebuilding an image, which is normally an awkward part of running Postgres on Kubernetes.

## When to use it

- you want **pooling included** rather than remembered — the most commonly missing piece
- extensions are used heavily and image-building is friction
- a console matters for people who do not read CRDs
- one opinionated stack is preferable to assembling four things

## When not to use it

- you want minimal moving parts — [CloudNativePG](../cnpg/README.md) runs Postgres and nothing else
- the opinions conflict with existing conventions; this stack brings Envoy and PgBouncer whether or not they fit
- commercial support is the deciding factor — [Crunchy](../crunchydata/README.md)

## The trade

More included, less control. That is the whole decision.

For a team that would otherwise deploy PgBouncer separately, forget the exporter, and build
custom images for extensions, StackGres arrives with all three solved. For a team with
established patterns for those, it arrives with opinions to reconcile.

Worth noting for this repository: **pooling is the piece most likely to be missing** on a CNPG
deployment — see [`sql/README.md`](../../../README.md#5-running-them-on-kubernetes). StackGres
solves that by construction.

---

[← PostgreSQL operators](../README.md)
