[← Database platform](../README.md)

# Percona Everest

<https://github.com/percona/everest>
<https://github.com/percona/percona-helm-charts>

---

## The problem it solves

Databases as a **self-service capability** rather than a ticket.

Every folder in [`databases/`](../../README.md) describes how to run one database well. This one
describes how to let other teams provision databases without the platform team being involved in
each request.

| Without it | With it |
|---|---|
| A team needs Postgres, so they open a ticket | they request one through a UI or an API |
| The platform team writes a `Cluster` manifest | a template is applied |
| Backups configured per instance, by hand | policy applied by default |
| Each database configured slightly differently | consistent, from templates |
| The platform team is the bottleneck | **it defines the guardrails instead** |

Everest sits on top of Percona's operators — PostgreSQL, MySQL and MongoDB — and provides the
provisioning layer, the UI and the API above them.

| Capability | Detail |
|---|---|
| **Multi-engine** | PostgreSQL, MySQL, MongoDB, via Percona operators |
| **Self-service provisioning** | UI and API |
| Backups and PITR | configured as part of provisioning rather than afterwards |
| Monitoring | [PMM](../../tooling/monitoring/pmm/README.md) integration |
| Multi-namespace | databases placed where they belong |
| Open source | Apache 2.0 |

## When to use it

- **several teams need databases**, and provisioning is currently a request to the platform team
- a mixed estate — PostgreSQL, MySQL and MongoDB under one provisioning model
- backups and monitoring should be **defaults**, not per-instance decisions
- Percona's operators are already the chosen path

## When not to use it

- **one team, a handful of databases** — operators plus manifests in Git is less to run, and this
  adds a control plane to solve a coordination problem that does not exist
- GitOps purity matters: databases provisioned through a UI are not in Git, which is the tension
  below
- non-Percona operators are in use — [CloudNativePG](../../sql/postgresql/operator/cnpg/README.md)
  in particular is not what this drives
- a broader internal developer platform already exists — see
  [`platform-engineering/idp/`](../../../platform-engineering/idp/README.md)

## The tension with GitOps

Worth naming, because it is the same one that appears with
[StreamPark](../../../data-streaming/processing/streampark/README.md) and several other
self-service tools in this repository.

Everest provisions databases through its own API and stores its own state. A GitOps repository
declares them as manifests. Both are legitimate and they answer to different owners:

| Model | Source of truth | Fits |
|---|---|---|
| **GitOps** | the repository | platform-managed databases, reviewed as code |
| **Self-service** | the control plane | application teams provisioning their own |

The resolution is usually not to choose one globally but to decide **which databases belong to
which model**: platform-critical instances in Git, team-owned instances through the portal, with
the boundary written down.

Getting that boundary wrong in either direction is the failure — either the platform team stays a
bottleneck, or nobody can reconstruct the estate from the repository.

## Notes

Mapped as the **platform** entry in [`databases/`](../../README.md), and it is the only one that
answers a question about organisation rather than about technology.

For this platform it is not applicable today: there is one operator,
[CloudNativePG](../../sql/postgresql/operator/cnpg/README.md), one PostgreSQL cluster, and one
person. Self-service exists to remove a bottleneck between teams, and there are no teams.

It is worth having catalogued for the corporate case, where the question *"how do application
teams get a database?"* has exactly two common answers — a ticket queue, or a platform — and the
first one scales badly.

Note the operator mismatch as a real consideration: Everest drives **Percona's** operators. A
platform standardised on CloudNativePG would be choosing between the self-service layer and its
existing PostgreSQL operator, which is a larger decision than it first appears.

---

[← Database platform](../README.md)
