[← PostgreSQL poolers](../README.md)

# PgBouncer

<https://github.com/pgbouncer/pgbouncer>

Chart references: <https://artifacthub.io/packages/helm/icoretech/pgbouncer> ·
<https://github.com/icoretech/helm/blob/main/charts/pgbouncer/values.yaml>

---

## The problem it solves

The default answer, and the one to choose unless something specific rules it out.

PostgreSQL allocates **a process per connection**. A few hundred is a real ceiling, and a fleet of
application pods reaches it without doing any work — see
[`../../README.md`](../../README.md#1-the-problem-precisely) for the arithmetic. PgBouncer sits in
front, keeps a small number of real backend connections, and multiplexes many clients across them.

It has been the standard for long enough that operators, dashboards and runbooks assume it. That is
most of the argument: [PgCat](../pgcat/README.md) and [Odyssey](../odyssey/README.md) each do
something PgBouncer does not, and neither has the surrounding ecosystem.

| Property | Detail |
|---|---|
| Written in | C — small, old, and extremely well understood |
| **Pool modes** | session, transaction, statement |
| Footprint | tiny; a few megabytes of memory |
| **Operator integration** | CloudNativePG, StackGres and Crunchy all deploy it for you |
| Prepared statements in transaction mode | supported in recent versions, which removed the historic objection |
| Threading | **single-threaded per process** — see below |

## When to use it

- **pooling is the requirement**, and nothing more
- a database **operator** manages the deployment — the integration is worth more than any feature
  difference elsewhere
- the deployment should be boring, and the failure modes already documented by other people

## When not to use it

- read/write splitting across replicas is wanted at the pooler — [PgCat](../pgcat/README.md)
- sharding — [PgCat](../pgcat/README.md), though that is a much larger commitment
- single-threaded throughput is a **measured** constraint and running several instances is
  unattractive — [Odyssey](../odyssey/README.md)
- MySQL — [ProxySQL](../../mysql/proxysql/README.md)

## The single-threaded objection

The standard complaint, and it decides less than it appears to.

One PgBouncer process saturates one core. The conventional answer is running several instances
behind a Service, which on Kubernetes is a replica count rather than a project — and a single
instance handles a large workload before that becomes necessary.

Worth treating as a number to measure rather than a reason to choose differently. If PgBouncer's
CPU is not near a core, the objection is theoretical.

## What to configure

| Setting | Guidance |
|---|---|
| **`pool_mode`** | `transaction` — session mode multiplexes nothing, so the pooler solves nothing. See [`../../README.md`](../../README.md#2-pooling-modes--the-decision-that-matters) |
| `max_client_conn` | generous; this is what the application sees |
| **`default_pool_size`** | **small** — this is the number that protects the database |
| `server_idle_timeout` | so backend connections are released rather than held open forever |
| `SHOW POOLS` / stats export | **waiting clients** is the metric that predicts an incident |

Getting `default_pool_size` wrong by making it large recreates the original problem with an extra
hop in front of it.

The failure to expect once transaction mode is on: anything session-scoped breaks — `SET` outside a
transaction, session advisory locks, `LISTEN`/`NOTIFY`, temporary tables. That list is in
[`../../README.md`](../../README.md#3-what-breaks-in-transaction-mode), and it fails intermittently
under load rather than immediately, which is why it is worth reading before deploying rather than
after.

## Notes

Two chart references were recorded for this folder — the
[icoretech chart on Artifact Hub](https://artifacthub.io/packages/helm/icoretech/pgbouncer) and
[its values file](https://github.com/icoretech/helm/blob/main/charts/pgbouncer/values.yaml).

The values file is the useful one to read, because PgBouncer's configuration is small enough that
the chart's values are effectively the whole surface: pool mode, sizes, timeouts and the auth
mechanism.

**For this platform, the chart is probably not the route.**
[CloudNativePG](../../../../sql/postgresql/operator/cnpg/README.md) is what runs PostgreSQL here,
and it ships a `Pooler` custom resource that deploys PgBouncer against an existing cluster —
credentials, TLS and service wiring included. That makes pooling a small amount of YAML rather than
a separate release to maintain, and it is why
[`../README.md`](../README.md#how-this-applies-to-pikakube) points here almost by default.

The gap this closes is the one named in [`../../README.md`](../../README.md#7-how-this-applies-to-pikakube):
pooling is the piece that decides behaviour under load on this platform, and nothing is deployed
yet.

---

[← PostgreSQL poolers](../README.md)
