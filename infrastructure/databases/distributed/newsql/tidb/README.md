[← NewSQL](../README.md)

# TiDB

<https://github.com/pingcap/tidb>
<https://github.com/pingcap/tidb-operator>

---

## The problem it solves

MySQL-compatible distributed SQL, with a genuine **HTAP** story — the same data queryable as rows
for transactions and as columns for analytics, without an ETL pipeline between them.

That last part is the differentiator, and it is worth understanding rather than accepting:

| Component | Role |
|---|---|
| **TiDB** | the stateless SQL layer — MySQL wire protocol, the query planner |
| **[TiKV](../../key-value/tikv/README.md)** | row storage, Raft-replicated, distributed |
| **TiFlash** | a **columnar replica** of the same data, fed from the same Raft groups |
| **PD** | the placement driver — tracks regions, decides where they live |

TiFlash is the HTAP mechanism. It maintains a columnar copy updated from the same replication
stream, so an analytical query reads columns while transactions keep writing rows. The optimiser
chooses between them per query.

The consequence is that "load the transactional data into a warehouse" — a pipeline, a schedule,
and a staleness window — is removed for a class of workload. When it fits, that is a substantial
architectural simplification.

## When to use it

- **MySQL compatibility** and a measured write or storage ceiling on one machine
- analytics on transactional data, without a separate warehouse and the pipeline feeding it
- an existing MySQL estate whose applications should keep working unchanged
- horizontal scale with real ACID transactions

## When not to use it

- **the ceiling has not been measured** — see
  [`../README.md`](../README.md#4-decision-tree); this is slower than PostgreSQL for a workload
  that fits on one machine
- PostgreSQL compatibility is what matters —
  [YugabyteDB](../yugabytedb/README.md) or [CockroachDB](../cockroachdb/README.md)
- the goal is sharding an existing MySQL estate incrementally —
  [Vitess](../vitess/README.md) keeps the shards as real MySQL
- the operational surface is a concern; this is four component types before anything runs

## What to model differently

The rules in [`../README.md`](../README.md#5-what-to-model-differently) apply, and one is
particularly consequential here:

**Avoid monotonically increasing primary keys.** An `AUTO_INCREMENT` key concentrates every insert
on the last region, so one Raft leader absorbs the entire write load and adding nodes does not
help. Use `AUTO_RANDOM`, which TiDB provides for exactly this, or a UUID.

This is the most common cause of "we scaled out and it got slower", and the reason is visible in
[TiKV's](../../key-value/tikv/README.md) design rather than in TiDB's.

## Notes

Recorded from deploying it:

> **Install the CRDs before the operator.**
>
> ```bash
> kubectl create -f https://raw.githubusercontent.com/pingcap/tidb-operator/v1.6.1/manifests/crd.yaml \
>   --dry-run=client -o yaml | \
> kubectl-slice --template '{{.kind | lower}}/{{.metadata.name | replace ".pingcap.com" ""}}.yaml' \
>   --output-dir .
> ```

That command is worth explaining, because the technique generalises well beyond TiDB.

The upstream CRD manifest is a single large file containing every custom resource definition.
`kubectl-slice` splits it into one file per resource, named by kind and by the CRD's name with the
`.pingcap.com` suffix removed — which is what makes them reviewable in Git and applicable
individually.

The reason it is needed at all is the general Kubernetes problem: **CRDs must exist before the
resources that use them**, and Helm's handling of CRDs is limited. Installing them separately and
explicitly is the reliable approach, and the same pattern applies to several operators in this
repository — see the
[FoundationDB note](../../key-value/foundationdb/README.md#notes) for the same problem in a
different form.

The sliced CRDs are kept in [`customresourcedefinition/`](customresourcedefinition/), and
[`example/tidbcluster.yaml`](example/tidbcluster.yaml) is the cluster definition.

Nothing is deployed here, and on a single Kind cluster nothing should be — four component types
with Raft groups on one machine demonstrates the API and none of the properties. TiDB is
catalogued as the **HTAP** answer, which is the one genuinely distinct proposition in
[`newsql/`](../README.md).

---

[← NewSQL](../README.md)
