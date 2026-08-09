[← MongoDB](../README.md)

# mongodb — plain manifests

<https://github.com/mongodb/mongo>
<https://github.com/mongodb/mongo-kafka>

---

## What this shape is

MongoDB as ordinary Kubernetes objects: a [Deployment](deployment.yaml), a
[PVC](pvc.yaml) and a [Service](service.yaml). One member, no replica set, no operator.

It is the development shape, and it is worth being explicit that this is what it is.

## When it fits

- **local development**, where the application needs a Mongo to talk to
- integration tests for a connector or an extraction pipeline
- learning the query model without operating the failure cases

## When it does not

- anything that must survive losing the node — there is **no replication and no failover**
- anything requiring backups beyond copying a volume
- **change streams**, which require a replica set even for a single member

That last row catches people. Change streams are the mechanism CDC depends on, and MongoDB only
provides them when the deployment is a replica set — a one-member replica set counts, but a plain
standalone does not. A pipeline built against this deployment will fail the moment it tries to
open a change stream.

## Why an operator is usually the answer

The operations a Deployment does not perform:

| Procedure | Detail |
|---|---|
| **Replica set initiation** | `rs.initiate()`, then adding members in order |
| **Failover** | primary election reflected in what clients connect to |
| Backups and PITR | oplog-based recovery, not a volume snapshot |
| Rolling upgrades | ordered across members, with a step-down |
| TLS and users | certificates and credentials as resources |

See [`../README.md`](../README.md) for the four options and how to choose between them — the
short version is that Percona's operator is usually the answer for self-hosting.

## Getting data out

This is MongoDB's realistic role in this platform, and the relevant links live here:

| Path | Tool |
|---|---|
| **CDC into Kafka** | [mongo-kafka](https://github.com/mongodb/mongo-kafka) — the official connector, built on change streams |
| Batch extraction | [Airbyte](../../../../../analytics-engineering/integration/airbyte/README.md) |
| Streaming platform | [`data-streaming/`](../../../../../data-streaming/README.md) |

Both paths depend on the replica-set point above, which is the practical reason this deployment
shape is development-only.

## Notes

The original notes for this folder also recorded
[mongo-express](https://github.com/mongo-express/mongo-express) and the
[Community Operator](https://github.com/mongodb/mongodb-kubernetes-operator), which now have
their own pages —
[mongo-express](../../../../tooling/management/mongo-express/README.md) under management tooling,
and [`mongodb-operator/`](../mongodb-operator/README.md) beside this one.

`mongodb.PNG` in this folder is a screenshot kept alongside the manifests.

---

[← MongoDB](../README.md)
