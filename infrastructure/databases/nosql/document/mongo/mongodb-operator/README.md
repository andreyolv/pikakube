[← MongoDB](../README.md)

# MongoDB Community Operator

<https://github.com/mongodb/mongodb-kubernetes-operator>
<https://github.com/mongodb/helm-charts>

Samples: <https://github.com/mongodb/mongodb-kubernetes-operator/tree/master/config/samples>

---

## What it is

MongoDB's own operator for the **Community Edition**. It manages replica sets as a
`MongoDBCommunity` custom resource — members, users, TLS and version upgrades.

| Capability | Detail |
|---|---|
| **Replica set orchestration** | initiation and reconfiguration handled by the controller |
| **Automated failover** | primary election, with the Service following it |
| Users | declared as Kubernetes resources, with credentials from Secrets |
| TLS | certificates wired in, including rotation |
| Rolling upgrades | ordered across members, with a step-down |

Crucially, it produces a **replica set** rather than a standalone — which is what makes change
streams available, and therefore what makes the deployment usable as a CDC source. See
[`../mongodb/`](../mongodb/README.md) for why that matters.

## When to use it

- Community Edition, self-hosted, with a replica set that must survive node loss
- MongoDB's own tooling is preferred over a third party's
- the deployment may later move towards the enterprise line or Atlas

## When not to use it

- **backups and point-in-time recovery are required** — this is the gap; the Community Operator
  does not cover them, and [Percona's](../percona-mongodb-operator/README.md) does
- sharding is needed
- the current official operator is the intended path —
  [`mongodb-kubernetes/`](../mongodb-kubernetes/README.md) supersedes this line

## The naming confusion

Worth untangling, because it is the main source of difficulty in this folder:

| Repository | What it is |
|---|---|
| `mongodb-kubernetes-operator` | **this one** — the older Community Operator |
| `mongodb-kubernetes` | the current official operator, unifying community and enterprise — [here](../mongodb-kubernetes/README.md) |
| `percona-server-mongodb-operator` | Percona's, Apache-2.0 — [here](../percona-mongodb-operator/README.md) |

Documentation, blog posts and Stack Overflow answers refer to all three as "the MongoDB
operator", frequently without saying which. Checking the repository name is the only reliable way
to know what a set of instructions applies to.

## The practical position

The Community Operator does the orchestration and stops short of the day-2 work that actually
decides whether a database survives — backups, PITR, sharding.

That is why [`../README.md`](../README.md) points at **Percona** for self-hosting: Apache-2.0,
and the complete feature set without a commercial tier. This operator is the right choice when
staying within MongoDB's own tooling matters more than those features.

## Notes

The [samples](https://github.com/mongodb/mongodb-kubernetes-operator/tree/master/config/samples)
are the useful starting point — [`example/mongodb.yaml`](example/mongodb.yaml) and
[`example/secret.yaml`](example/secret.yaml) here are the minimal pair: the replica set, and the
credentials it reads.

For this platform MongoDB is a **source system** rather than a system of record, so the operator
question is mostly about whether change streams are available and the deployment is stable enough
to extract from — see [`../README.md`](../README.md#how-this-applies-to-pikakube).

---

[← MongoDB](../README.md)
