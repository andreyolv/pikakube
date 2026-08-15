[← MariaDB](../README.md)

# MariaDB operators

Running [MariaDB](../README.md) on Kubernetes as a set of resources rather than as a StatefulSet and
a runbook.

Tools covered: [`mariadb-operator`](mariadb-operator/README.md)

---

## What an operator has to solve here

The list is largely the one written for [MySQL operators](../../mysql/operator/README.md) —
bootstrap in order, failover without two writable primaries, re-cloning a replica that fell too far
behind, binlog-based recovery, rolling upgrades, routing writes to the current primary, users and
grants as objects. It is worth repeating only where MariaDB differs, and it differs in one
structural way:

**MariaDB's high-availability story is Galera first.** Where MySQL's mainstream answers are
asynchronous or semi-synchronous replication with a promotion step, MariaDB ships **synchronous
multi-primary replication** in the distribution itself, and it is what most MariaDB clusters use.
That changes what the operator is for:

| | Asynchronous / semi-sync replication | **Galera** |
|---|---|---|
| Writes go to | one primary | any node — certification resolves conflicts |
| Failover means | promoting a replica, then repointing the others | no promotion; the cluster survives losing a node |
| The hard problem | **election and repointing** | **quorum, state transfer, and split-brain** |
| A new or lagging node | is re-cloned | performs an **SST** — a full state transfer that loads a donor |
| What the operator earns its place doing | orchestrating failover correctly | bootstrapping and **recovering** the cluster, in the right order, from the right node |

The last row is the point. Galera removes the failover problem and replaces it with a recovery
problem: after an unclean shutdown of the whole cluster, somebody has to determine which node holds
the most advanced state and bootstrap from it. Done by hand, at 03:00, that is where data gets lost.
An operator that does it correctly and repeatedly is the entire argument for running MariaDB on
Kubernetes rather than beside it.

## The landscape

Thinner than PostgreSQL's, where [CloudNativePG](../../postgresql/operator/cnpg/README.md) is a
clear default, and thinner even than MySQL's:

| Option | Position |
|---|---|
| **[mariadb-operator](mariadb-operator/README.md)** | the community operator, MIT — Galera, replication, MaxScale, backups and PITR. The default open answer |
| MariaDB Enterprise Operator | MariaDB plc's own, commercially supported, for MariaDB Enterprise Server |
| Percona XtraDB Cluster Operator | **Galera for MySQL/Percona Server, not MariaDB** — the same replication technology, a different database |
| A StatefulSet and a chart | viable for a single instance with a PVC; not viable for Galera |

That third row is the one that causes confusion in evaluations. Galera is a replication layer used
by more than one distribution, so "a Galera operator" is not automatically a MariaDB operator — check
which server it manages before it reaches a shortlist.

---

[← MariaDB](../README.md)
