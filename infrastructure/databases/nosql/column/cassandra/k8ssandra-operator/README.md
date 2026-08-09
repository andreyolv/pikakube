[← Cassandra](../README.md)

# K8ssandra Operator

<https://github.com/k8ssandra/k8ssandra-operator>

---

## The problem it solves

Cassandra runs fine in a StatefulSet. What a StatefulSet cannot do is the **ongoing operations**,
and for Cassandra those are where the data is lost — see
[`../cassandra/`](../cassandra/README.md).

K8ssandra makes the cluster and its operations Kubernetes resources:

| Capability | Why it is not a chart |
|---|---|
| **`K8ssandraCluster` CRD** | the whole topology — datacentres, racks, nodes — declared and reconciled |
| **Scheduled repair** | via Reaper; the operation that silently corrupts data when skipped |
| **Backups** | via Medusa, to object storage, with restore |
| Node replacement | a dead node replaced with the correct flags and a streaming rebuild |
| Rolling upgrades | one node at a time, health-checked between |
| **Multi-datacentre** | replication across clusters, which is a primary reason to choose Cassandra |
| Monitoring | metrics exposed for Prometheus |
| Stargate | optional REST, GraphQL and document APIs over CQL |

**Reaper is the component that justifies the operator on its own.** Cassandra tolerates replicas
diverging and reconciles them lazily through anti-entropy repair. If repair never runs, deleted
data can reappear once tombstones expire — a failure that is silent, delayed, and extremely
confusing when it surfaces. Scheduling it correctly by hand is possible and it is the thing that
does not survive the first busy quarter.

## When to use it

- **any Cassandra that is not a development instance**
- multi-datacentre replication, which is one of the main reasons to run Cassandra at all
- backups and repair should be declared rather than remembered
- the topology will change — nodes added, replaced, or a second datacentre introduced

## When not to use it

- a single node for local development — the [chart](../cassandra/README.md) or a container is
  simpler
- Cassandra is not actually the right answer, which is worth checking first against
  [`../../README.md`](../../README.md#5-decision-tree)
- [ScyllaDB](../../scylladb/README.md) is the chosen engine — it has its own operator

## What still has to be decided

The operator runs the cluster. It does not decide the two things that determine whether the
cluster is usable, and both are permanent:

| Decision | Why it is not the operator's |
|---|---|
| **The partition key** | it *is* the schema; it cannot be changed later — see [`../../README.md`](../../README.md#2-the-partition-key-is-the-schema) |
| **Consistency levels** | chosen per query; `R + W > RF` or reads are intermittently stale |

An operator makes it easy to run a well-operated cluster containing a data model that cannot
serve the queries. That is worth stating, because the deployment being easy is often mistaken for
the hard part being done.

Also worth setting deliberately: `NetworkTopologyStrategy` for replication even with one
datacentre, so adding a second later does not require re-keying every keyspace.

## Notes

[`example/k8ssandracluster.yaml`](example/k8ssandracluster.yaml) is the custom resource, and it
is the useful thing to read first — it shows the whole topology as one declaration, which is the
difference from a chart's values file.

The operator is Apache-2.0 and built by DataStax, which is the main commercial backer of
Cassandra. That is worth knowing in both directions: sustained development, and a project whose
roadmap follows a vendor's.

For this platform, nothing here is deployed and nothing should be — see
[`../../README.md`](../../README.md#7-how-this-applies-to-pikakube). A masterless multi-node store
on a single Kind cluster demonstrates the API and none of the properties that justify the data
model it demands.

---

[← Cassandra](../README.md)
