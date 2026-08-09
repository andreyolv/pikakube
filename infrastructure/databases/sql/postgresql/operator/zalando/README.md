[← PostgreSQL operators](../README.md)

# Zalando Postgres Operator

<https://github.com/zalando/postgres-operator>

---

## What it is

The operator that was **the** standard for years, from Zalando, built on **Patroni** — the HA
framework that most of this category grew out of.

Its architecture reflects that lineage: Patroni handles consensus and failover, using
Kubernetes or etcd as the distributed configuration store.

## Why it matters historically

Patroni is the reference implementation of PostgreSQL HA, and understanding it explains the
category. Every operator solves the same problem — who is primary, and how does that change
safely — and this one does it with the component that defined the approach.

## When to use it

- an **existing Zalando estate** that works. Migrating operators is a real project
- Patroni is already understood and operated elsewhere
- the UI it ships with is useful to the team

## When not to use it

- **new deployments.** [CloudNativePG](../cnpg/README.md) achieves the same without Patroni or an external DCS, which is fewer components and fewer failure modes
- you want CNCF governance
- commercial support is required — [Crunchy](../crunchydata/README.md)

## The architectural difference, concretely

| | Zalando | [CloudNativePG](../cnpg/README.md) |
|---|---|---|
| Consensus | Patroni, plus a DCS | the Kubernetes API |
| Extra components | yes | none |
| Failure modes | includes the DCS | fewer |

That is the whole reason the default moved. Not that Patroni is bad — it is well understood and
battle-tested — but that a Kubernetes-native operator can use the API server as the consensus
layer and skip an entire class of component.

## If you are on it

There is no urgency. It works, it is maintained, and migrating operators means a migration of
the data. The time to reconsider is when the cluster is being rebuilt anyway.

---

[← PostgreSQL operators](../README.md)
