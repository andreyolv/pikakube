[← NewSQL](../README.md)

# Multigres

<https://github.com/multigres/multigres>

<https://multigres.com>

[Vitess](../vitess/README.md) for PostgreSQL — the same architecture, by people who built the
original, aimed at the engine that never had one. Apache-2.0, and **early**.

---

## The problem it solves

[§2](../README.md#2-two-architectures-and-the-difference-matters) of this folder splits these tools
into two columns: databases built distributed from the storage up, and routing layers that shard an
engine you already run. Look at which engines appear in the second column and the gap is obvious:

| Approach | MySQL | PostgreSQL |
|---|---|---|
| **Shard the engine you already run** | [Vitess](../vitess/README.md), [ShardingSphere](../shardingsphere/README.md) | *(nothing comparable)* |
| Replace it with a distributed engine | — | [CockroachDB](../cockroachdb/README.md), [YugabyteDB](../yugabytedb/README.md) |
| Extend it in-engine | — | Citus, as a PostgreSQL extension |

A MySQL estate that outgrows one machine has had a pragmatic answer since 2011: keep MySQL, put
Vitess in front of it, shard incrementally, keep the backups and the expertise. A PostgreSQL estate
in the same position has had three worse options — rewrite onto a wire-compatible distributed
engine, adopt an extension the managed providers may not offer, or shard in the application and own
that forever.

Multigres is the missing entry. It applies Vitess's design to Postgres: a proxy in front of real
PostgreSQL instances, a topology service holding the cluster's shape, a component beside each
instance managing it, and an orchestration layer handling failover and resharding.

| Vitess | Multigres | Role |
|---|---|---|
| VTGate | **multigateway** | the proxy clients connect to; routes queries to shards |
| VTTablet | **multipooler** | sits beside each Postgres, manages it — and pools connections |
| vtorc | **multiorch** | failover and cluster orchestration |
| vtctld / VTAdmin | **multiadmin** | administration and topology control |
| etcd / ZooKeeper | topology store | the cluster's shape |

The lineage is the reason to pay attention rather than to file it with every other new database:
it is led by **Sugu Sougoumarane, a co-creator of Vitess**, developed in the open with Supabase
behind it. The design is not being invented — it is being ported, by the people who learned its
sharp edges at YouTube scale.

## The part that is useful before sharding is

**Connection pooling is not a footnote here, it is arguably the nearer-term point.** PostgreSQL's
process-per-connection model makes connection count an operational constraint long before data
volume is, which is why every serious Postgres deployment ends up running
[PgBouncer, pgcat or Odyssey](../../../tooling/pooler/postgres/README.md) — a separate component,
with its own pooling-mode caveats around prepared statements and session state.

Multigres folds pooling into the same layer that does routing, because Vitess always did. A cluster
that is not sharded at all still has a reason to want that layer, and *"we adopted it as a pooler
and sharded later"* is the adoption path that would make this project stick. It is also the honest
counter-argument: PgBouncer works today, is boring, and is not early-stage software.

## When to use it

Stated carefully, because the honest answer today is *"do not yet, but watch it"*:

- **an existing PostgreSQL estate approaching the limits of one machine**, where leaving Postgres is
  unacceptable — this is the case the project exists for
- when the MySQL-versus-Postgres asymmetry above is the actual reason a team is being pushed toward
  CockroachDB or Yugabyte, and nobody wants that migration
- **evaluation, prototyping and tracking**: the architecture is knowable now because Vitess is
  documented, so a design that assumes a routing layer can be sketched before the software is ready
- as a reason to **make sharding-friendly schema decisions early** — see below

## When not to use it

- **production, today.** The project describes itself as being in the early stages of development,
  and it is not soliciting large contributions. That is a clear statement from the maintainers and
  it should be taken at face value
- **greenfield.** The same rule as Vitess: if there is no existing estate to preserve, a natively
  distributed engine is simpler than Postgres plus a routing layer
- when the requirement is **read scaling** — that is replicas and a pooler, not sharding
- when the requirement is **analytics** — that is a column store
  ([`../../../analytical/`](../../../analytical/README.md)) or the lakehouse, not a sharded OLTP
  database
- when Citus already solves it and is available on your platform. Extension-based sharding is a
  genuinely different trade — inside the engine rather than in front of it — and it is production
  software now

## The constraint that does not go away

Everything [Vitess's page](../vitess/README.md) says about the sharding key applies here unchanged,
because it is a property of the architecture rather than of the implementation:

- **the sharding key is a schema decision, not a configuration one**, and choosing it badly is
  expensive to undo
- **cross-shard transactions are constrained**, and queries that ignore the key fan out to every
  shard
- **the operational surface grows**: Postgres, plus a gateway, plus a per-instance component, plus a
  topology store — each of which can fail on its own

That is the trade in the second column of [§2](../README.md#2-two-architectures-and-the-difference-matters):
not fewer problems than CockroachDB, different ones. What you buy is that the shards are **real
PostgreSQL** — the same `pg_dump`, the same extensions, the same `EXPLAIN`, the same operational
knowledge, and the same tooling in [`tooling/`](../../../tooling/README.md) — and that getting there
is incremental rather than a migration.

## Notes

**The useful thing to take from this today is a design constraint, not a dependency.** If a Postgres
database might one day need horizontal scale, the decision that matters is made early and cheaply:
is there a natural tenant or entity key that most queries already carry? Schemas designed with that
key present are shardable later by Multigres, by Citus, or by hand. Schemas without one are not, and
no routing layer fixes it afterwards.

**Watch the maturity signals, not the announcements.** For a project of this shape the questions
that decide readiness are specific and answerable: is online resharding implemented and tested; what
happens to in-flight transactions during a failover; which PostgreSQL wire-protocol features the
gateway does not yet handle (prepared statements, `LISTEN`/`NOTIFY`, `COPY`, cursors); and is there
a Kubernetes operator, because Vitess's usability on Kubernetes came from one. Those, not the star
count, tell you where it is.

**Where this fits in pikakube.** [PostgreSQL is the default here](../../../sql/postgresql/README.md),
this is a Kind cluster, and nothing in it is close to the scale that makes sharding a question — so
Multigres is catalogued as a **direction**, not a candidate. Its value in this repository is that it
fills a real hole in [§2](../README.md#2-two-architectures-and-the-difference-matters)'s table: the
"shard what you already run" column has been MySQL-only, which quietly biases every scaling
conversation about Postgres toward a full engine replacement. Worth revisiting in a year with the
questions in the previous note in hand.

---

[← NewSQL](../README.md)
