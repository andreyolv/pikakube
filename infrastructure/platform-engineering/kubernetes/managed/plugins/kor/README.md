[← Plugins](../README.md)

# kor

<https://github.com/yonahd/kor>

---

## The problem it solves

Clusters accumulate. A ConfigMap created for an experiment, a Secret for a service that was deleted,
a ServiceAccount nothing uses, a PVC whose pod is long gone, an empty Deployment. None of it breaks
anything, all of it makes the cluster harder to reason about, and some of it costs money.

kor scans for orphaned and unused resources — ConfigMaps, Secrets, Services, ServiceAccounts,
Deployments, StatefulSets, Roles, HPAs, PVCs and more — and reports what appears to have no consumer.
It can output text, JSON or a summary, which makes it usable both interactively and in a report.

## When to use it

- Periodic cleanup of a cluster that has been running for a while
- Auditing an inherited cluster to find out what is actually in use
- Cost reduction, particularly for orphaned PersistentVolumeClaims
- Producing a review list — not a delete script

## When not to use it

- Anywhere its output would be piped straight into `kubectl delete`
- Where resources are consumed in ways it cannot see — see below
- As a substitute for owning what you create; the real fix is upstream of this tool
- On a GitOps cluster, without checking Git first; if it is in Git, deleting it achieves nothing

## Notes

Recorded as a link only.

**"Unused" is a heuristic and it must be treated as one.** kor infers usage from references it can
find — a ConfigMap mounted by a pod, a Secret referenced by a ServiceAccount. Things it cannot see:

- resources referenced by **name in application code** rather than in a manifest
- Secrets read through the API by an operator at runtime
- resources consumed by a CRD whose relationships kor does not model
- anything used by a workload that is **currently scaled to zero** — including everything paused by
  [`sleep/`](../../sleep/README.md), which is a real interaction worth remembering
- resources that exist for a job that runs monthly

Each of those looks exactly like an orphan. Deleting a Secret an operator reads at runtime produces a
failure at the next reconcile, some distance from the deletion, and nobody connects the two.

**On a GitOps cluster the question changes shape.** If the resource is declared in Git, deleting it
from the cluster is pointless — the reconciler restores it. So kor's output on a GitOps cluster is
best read as a list of things to remove **from the repository**, and its real value is finding the
resources that are in the cluster and in no repository at all. Those are the genuine orphans, and
they are also the most interesting ones, because their existence means somebody applied something by
hand.

**The useful workflow**: run it, read the report, check each item against Git, delete from Git, let
the reconciler do the removal. Slower than a pipe into `kubectl delete`, and the only version that is
safe.

---

[← Plugins](../README.md)
