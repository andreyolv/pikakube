[← Platforms](../README.md)

# KubeBlocks

<https://github.com/apecloud/kubeblocks>

---

## The problem it solves

A cluster ends up running several stateful systems, and each arrives with its own operator: one for
PostgreSQL, one for MySQL, one for Redis, one for Kafka, one for MongoDB. Each has its own CRDs, its
own backup mechanism, its own idea of what an upgrade or a failover looks like, and its own bugs.

KubeBlocks replaces that with one operator and a uniform model: `Cluster` and `ClusterDefinition`
resources describing an engine, its topology, its backup policy and its resources. Provisioning
PostgreSQL and provisioning Redis become the same operation with a different parameter.

## When to use it

- Several different database engines in one cluster, and the per-engine operator sprawl is the problem
- Building database-as-a-service for internal teams, where a uniform interface is the product
- Consistent backup, restore and failover semantics across engines matter more than per-engine depth
- The engines you need are well supported by it

## When not to use it

- One database engine — its dedicated operator will be more capable and better documented
- Where you need engine-specific features the abstraction does not expose
- Production-critical data without verifying the specific engine's maturity in KubeBlocks
- If [`databases/`](../../../../../databases/README.md) tooling already covers the estate

## Notes

**Chart** `kubeblocks` version `0.9.0-alpha.1` from `https://apecloud.github.io/helm-charts`, with a
namespace manifest and empty values.

**That version string is the headline: `alpha.1`.** An alpha operator managing production databases
is not a defensible position, and it is worth stating plainly rather than letting the version sit
unremarked in a manifest. As a mapped option it is fine; as something to reconcile against a cluster
holding data it is not.

**It does not belong in `platforms/` in the same sense as its neighbours.** APL, KubeSphere and
Devtron are general platform distributions. KubeBlocks is a **domain** platform — it manages one
class of workload, very well or not at all. The natural neighbour is
[`databases/`](../../../../../databases/README.md), which is where per-engine operators such as
CloudNativePG live, and the honest comparison is with those rather than with a distribution.

**The trade, stated properly:** a dedicated operator encodes deep knowledge of one engine —
CloudNativePG's understanding of PostgreSQL failover is the product of years focused on PostgreSQL. A
uniform operator encodes shared knowledge of many. For an organisation running five engines and
needing consistent backup and self-service, uniformity can be worth more than depth. For one
critical PostgreSQL cluster, it is not close.

ApeCloud maintain it, with a commercial offering above the open-source operator.

---

[← Platforms](../README.md)
