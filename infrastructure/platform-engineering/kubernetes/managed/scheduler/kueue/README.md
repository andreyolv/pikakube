[← Scheduler](../README.md)

# Kueue

<https://github.com/kubernetes-sigs/kueue>

---

## The problem it solves

Kueue is the conservative answer to batch scheduling: it manages the **queue**, and leaves placement
to the default scheduler.

A `Job` is not admitted to the cluster until its quota is available. Kueue holds it — suspended,
occupying nothing — until a `ClusterQueue` has room, then unsuspends it and lets the standard
scheduler place its pods. Quota is organised into `ResourceFlavor`s (for example, spot versus
on-demand, or GPU model) and can be **borrowed** between queues in a cohort and reclaimed when the
owner needs it.

The design consequence is significant: **you keep the standard `Job` API and the standard
scheduler.** Nothing about your workloads changes.

## When to use it

- Batch and ML on Kubernetes without replacing the scheduler
- Standard `Job`, plus integrations for Kubeflow, Ray, Spark and similar
- Quota that teams can borrow from each other while capacity is idle
- You want a `kubernetes-sigs` project rather than a third-party scheduler

## When not to use it

- Fine-grained placement control within a job — that needs a real scheduler such as [Volcano](../volcano/README.md)
- Deep queue hierarchies with complex sharing policy — [YuniKorn](../yunikorn/README.md)
- Long-running services; Kueue is about admitting finite work
- Where the workload does not support suspension, which is the mechanism it relies on

## Notes

**Installed from an `OCIRepository`**, with a namespace manifest. Recorded as a link only.

**The mechanism is `Job.spec.suspend`**, and understanding that explains both the elegance and the
limits. Kubernetes `Job` has had a `suspend` field since 1.21: a suspended job creates no pods. Kueue
admits a job by flipping that field. So the entire queueing system is built on a standard API field
rather than on intercepting scheduling — which is why it needs no scheduler of its own and composes
with everything else.

It also means Kueue can only manage things that can be suspended. It queues **jobs**, not pods; a
bare Deployment is outside its model.

**The quota model** in three objects, which is the whole API surface:

- **`ResourceFlavor`** — a kind of capacity, mapped to nodes by labels. Spot versus on-demand, or
  `nvidia-a100` versus `nvidia-t4`.
- **`ClusterQueue`** — quota over flavours, with borrowing rules and a cohort it belongs to.
- **`LocalQueue`** — the namespace-scoped entry point that users submit to, pointing at a
  `ClusterQueue`.

The borrowing behaviour is the interesting part: a team can exceed its guaranteed quota while other
teams are idle, and the capacity is reclaimed when they return. That is what makes static quota
palatable — the usual objection to `ResourceQuota` is that guaranteed capacity sits unused, and this
answers it directly.

**Where it sits among the alternatives:** Kueue is the smallest change that solves queueing and
quota. It does not gang-schedule at the pod level in the way Volcano does — it admits a whole job at
once, which covers most of the same need, and the difference matters when partial placement of an
admitted job is still possible. For most teams the smaller change is the right one, and
`kubernetes-sigs` ownership makes it the safest default in this folder.

---

[← Scheduler](../README.md)
