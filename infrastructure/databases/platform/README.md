[← Databases](../README.md)

# Database platform

Running databases as a **self-service capability**, not as individual deployments.

Tools covered: [`openeverest`](openeverest/README.md)

---

## The problem it solves

A platform team ends up operating several databases for several teams. Each request —
"we need a Postgres for this service" — becomes a ticket, a Helm release, a set of decisions
about sizing, backup and monitoring, and a thing to remember to upgrade.

That does not scale, and the failure is predictable: teams start running their own, badly, or
the platform team becomes the bottleneck for every new service.

A database platform makes provisioning **self-service and consistent**:

| Capability | What it replaces |
|---|---|
| Provision on request | a ticket and a hand-written manifest |
| Standard configuration | each database configured differently by whoever created it |
| Backup by default | remembering to set it up per instance |
| Monitoring by default | discovering there was none during an incident |
| Upgrades as a fleet operation | tracking versions in a spreadsheet |

## The tools

| Tool | What it is | Detail |
|---|---|---|
| **Percona Everest** | open-source platform for provisioning and managing PostgreSQL, MySQL and MongoDB clusters on Kubernetes, built on the Percona operators | [→](openeverest/README.md) |

## What it is built on

Worth understanding, because it explains both the value and the limits: this is a **layer over
operators**, not a new database runtime.

The operators — [CloudNativePG](../sql/postgresql/operator/cnpg/README.md), Percona's, the MongoDB
operator — already encode failover, backup and upgrade. What the platform adds is the
**self-service surface** on top: a catalogue, provisioning, and consistent defaults across
engines.

So the question it answers is organisational rather than technical: *how do teams get a
database without asking us?*

## Where this sits

| Concern | Where |
|---|---|
| Running one database well | the operator, in [`sql/`](../sql/README.md) or [`nosql/`](../nosql/README.md) |
| **Teams provisioning their own** | here |
| Self-service infrastructure generally | [`platform-engineering/`](../../platform-engineering/) — Crossplane, Backstage |

The overlap with `platform-engineering/` is real. A Crossplane composition plus a Backstage
template achieves something similar, using components this repository already maps — which is
the honest alternative to adopting a database-specific platform.

## When it makes sense

- **several teams** need databases, and provisioning is currently a ticket
- consistency matters more than per-database tuning
- backup and monitoring should be defaults rather than decisions

## When it does not

- a small number of databases, operated by the team that uses them
- one engine only — the operator alone is simpler
- you already have a self-service story through Crossplane and Backstage; this would be a second one

## How this applies to pikakube

Not deployed. The repository already runs [CloudNativePG](../sql/postgresql/operator/cnpg/README.md)
directly, which is the right shape for one cluster.

It is mapped because the transition it represents is a real one for a platform team: the point
at which "we run the databases" has to become "teams provision databases from a catalogue" —
and the alternative path, through
[Crossplane](../../platform-engineering/iac/) and
[Backstage](../../platform-engineering/idp/), is already mapped in this repository.

---

[← Databases](../README.md)
