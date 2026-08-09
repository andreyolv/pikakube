[← Sleep](../README.md)

# kube-green

<https://github.com/kube-green/kube-green>

---

## The problem it solves

The same job as [kube-downscaler](../kube-downscaler/README.md) — scale workloads to zero outside
working hours — expressed as a **custom resource** rather than as annotations.

A `SleepInfo` object in a namespace declares when to sleep, when to wake, which weekdays, and which
resources to exclude. The operator reads it and acts. The schedule is therefore a first-class
Kubernetes object: it lives in Git, is reviewed in a pull request, and is visible with `kubectl get
sleepinfo` rather than by inspecting annotations across every Deployment.

The project frames this as sustainability as much as cost — idle compute is emissions as well as
invoice.

## When to use it

- GitOps-managed clusters, where the schedule should be a declared object like everything else
- One schedule per namespace, rather than per workload
- You want the sleeping policy reviewable and diffable
- Suspending CronJobs during the window, which it handles explicitly

## When not to use it

- Production or anything with users outside the window
- Fixed-size clusters — no nodes removed, no saving
- Where a CRD and an operator are more machinery than the problem justifies
- Workloads that do not survive being stopped

## Notes

**Chart, namespace manifest, and a committed `example/sleepinfo.yaml`** — the example being the
useful artifact, since the `SleepInfo` schema is the whole interface.

**What a `SleepInfo` declares**, and the fields that decide behaviour:

- **`sleepAt` and `wakeUpAt`**, in cron format — and a `SleepInfo` with no `wakeUpAt` sleeps and never
  wakes, which is legitimate for an environment being retired and is not what anyone means by
  accident.
- **`timeZone`** — an explicit field, which is a better design than embedding it in a schedule string.
  Set it. UTC windows drift against local office hours and move twice a year.
- **`excludeRef`** — the workloads that must keep running. This is where the operator's own
  dependencies and anything stateful belong.
- **`suspendCronJobs`** — whether CronJobs are suspended during the window. Explicit, which is
  better than the silent non-execution that catches people out elsewhere.

**Namespace-scoped is the key design decision.** A `SleepInfo` applies to the namespace it is in, so
the unit of sleeping is an environment rather than a workload. That matches how these environments are
actually reasoned about — "the staging namespace sleeps at night" — and it avoids the annotation
sprawl of per-workload schedules.

**The GitOps fit is the argument for it over
[kube-downscaler](../kube-downscaler/README.md).** With a CRD, changing the schedule is a commit,
reviewable and reversible, with history. With annotations, the schedule is spread across every
workload and changing it means touching each one. In a repository like this, where everything else is
declared, consistency is worth something on its own.

The saving still depends on the [cluster autoscaler](../../autoscaler/README.md) removing the nodes
that empty out. Scaling to zero on fixed capacity changes the invoice by nothing.

---

[← Sleep](../README.md)
