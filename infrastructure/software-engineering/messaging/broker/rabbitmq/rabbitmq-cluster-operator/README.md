[← RabbitMQ](../README.md)

# RabbitMQ Cluster Operator

<https://github.com/rabbitmq/cluster-operator>
<https://github.com/rabbitmq/messaging-topology-operator>

Examples in this folder: [`example/rabbitmqcluster.yaml`](example/rabbitmqcluster.yaml) ·
[`example/queue.yaml`](example/queue.yaml)

---

## The problem it solves

The [Helm chart](../rabbitmq/README.md) gives you a cluster. This gives you **clusters and the
things inside them** as Kubernetes resources.

The Bitnami chart deployed here installs two controllers, and they are separate upstream projects
doing separate jobs:

| Operator | CRD | What it declares |
|---|---|---|
| **Cluster operator** | `RabbitmqCluster` | the cluster — replicas, storage, resources, broker config |
| **Messaging topology operator** | **`Queue`**, **`Exchange`**, **`Binding`**, **`Policy`**, **`User`**, **`Permission`**, `Vhost`, `Federation`, `Shovel`, `SuperStream`, `SchemaReplication` | everything *inside* a running broker |

The cluster operator is convenience — a CRD instead of chart values, plus rolling upgrades that
understand quorum queue membership rather than restarting pods in ordinal order and hoping.

**The topology operator is the reason to be here.** Without it, queues and users are created by
whichever application connected first, by a human in the management UI, or by `rabbitmqadmin` in a
script nobody kept. None of that is in Git, none of it is reviewed, and none of it survives a
cluster being rebuilt.

That matters most because the important queue arguments are **immutable after declaration**:

| Argument | Changing it means |
|---|---|
| queue type (`quorum` vs classic) | delete and recreate the queue |
| durability | delete and recreate |
| `x-dead-letter-exchange` | delete and recreate |
| `delivery-limit`, `max-length` | delete and recreate |

A queue declared accidentally at application startup had those decided by whoever wrote the
connection code. A queue declared as a `Queue` resource had them reviewed in a pull request.

## When to use it

- **topology belongs in Git** — queues, exchanges, bindings, users, permissions and policies
- several clusters, or clusters recreated regularly, where reproducibility is the requirement
- self-service: teams declare their own queues with review, instead of filing a request
- rolling upgrades of a quorum-queue cluster, where member-aware ordering is not optional
- users and permissions as reviewable resources rather than UI state

## When not to use it

- **one static cluster** whose configuration rarely changes — [the chart](../rabbitmq/README.md)
  is less to run and less to learn
- application code declares its own queues and will keep doing so — see the conflict note below
- topology is already managed by another mechanism and nobody wants two sources of truth

## Notes

Recorded links:

- <https://github.com/rabbitmq/cluster-operator> — runs the cluster.
- <https://github.com/rabbitmq/messaging-topology-operator> — turns queues, exchanges, users and
  policies into Kubernetes resources. This is the interesting one.

### As configured here

The `HelmRelease` installs the Bitnami `rabbitmq-cluster-operator` chart, which bundles both
controllers, and enables metrics with a **`ServiceMonitor` for each** —
`clusterOperator.metrics` and `msgTopologyOperator.metrics`. Both, deliberately: a topology
operator that silently fails to reconcile a `Queue` is a change that looks merged and never
happened, and only its own metrics show that.

Scraping is by [Prometheus](../../../../../observability/metrics/storage/prometheus/README.md).

### The examples

[`example/rabbitmqcluster.yaml`](example/rabbitmqcluster.yaml) — a three-replica cluster named
`my-rabbitmq-cluster` with 2Gi persistence, 2Gi memory and 1 CPU requested, `additionalConfig`
setting the default user and `log.console.level=debug`, and a `ClusterIP` service.

The annotation on it is the part worth understanding:

```
rabbitmq.com/topology-allowed-namespaces: "rabbitmq"
```

That is the **authorisation boundary of the topology operator**. It declares which namespaces may
point `Queue`, `User` or `Policy` resources at this cluster. Without it, only the cluster's own
namespace may. Set to a list, it enables self-service — a team declares queues in its own
namespace against a shared broker; set to `"*"`, any namespace in the cluster can create queues
and users on it, which is rarely what anyone means.

[`example/queue.yaml`](example/queue.yaml) — a `Queue` named `pikachu` referencing the cluster
through `rabbitmqClusterReference`. Minimal on purpose: it shows that a queue is now an object
Flux applies and reconciles, like a Deployment.

Note what the example does **not** set — `type: quorum`, a dead-letter exchange, a
`delivery-limit`. Those default to a classic queue with no retry limit and no dead-letter target,
which is exactly the shape [`broker/`](../../README.md#10-anti-patterns) argues against. The
example is a mechanism demonstration, not a template to copy into production.

### The conflict to plan for

The topology operator and application-side declarations will fight, and the last declaration wins.
`queue_declare` with arguments that differ from the existing queue fails with
`PRECONDITION_FAILED` and takes the channel down with it — so a mismatch is not a warning, it is
an application that cannot start.

Adopting this means **removing queue declarations from application code**, not adding CRDs
alongside them. That is an application change, and it is the real cost of the migration.

---

[← RabbitMQ](../README.md)
