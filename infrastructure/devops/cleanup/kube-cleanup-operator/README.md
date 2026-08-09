[← Cleanup](../README.md)

# kube-cleanup-operator

<https://github.com/lwolf/kube-cleanup-operator>

---

## The problem it solves

A `CronJob` running every five minutes leaves a `Job` behind every five minutes, and each `Job`
leaves a `Pod`. Nothing removes them by default. After a few weeks the namespace holds thousands of
completed objects, `kubectl get pods` is unusable, and etcd is carrying state that describes work
finished long ago.

Failed and evicted Pods are worse: they persist indefinitely by design, on the assumption that
somebody will look at them. Nobody looks at the four-hundredth one.

kube-cleanup-operator watches Jobs and Pods and deletes them once they have been in a terminal
state for longer than a configured duration. The controller takes its policy entirely from
command-line flags:

| Flag | What it removes |
|---|---|
| `--delete-successful-after` | Jobs and Pods that completed successfully |
| `--delete-failed-after` | Jobs and Pods that failed |
| `--delete-pending-pods-after` | Pods stuck in `Pending` — usually unschedulable |
| `--delete-evicted-pods-after` | Pods evicted under node pressure |
| `--delete-orphaned-pods-after` | Pods whose owning Job no longer exists |

A duration of `0` disables a category, which is how you keep failures around for inspection while
still clearing successes.

## When to use it

- **Failed, evicted, pending and orphaned Pods** need cleaning up — this is the real reason to
  deploy it, because Kubernetes has no native answer for any of those four
- Jobs are created by something that does not set `ttlSecondsAfterFinished` — a Helm chart, an
  operator, an external system — and patching every producer is not practical
- a single cluster-wide retention policy is wanted, rather than a field repeated on every Job

## When not to use it

- **If the only problem is completed Jobs.** Kubernetes has `ttlSecondsAfterFinished` in the Job
  spec. It is native, needs no controller, and the TTL travels with the object that created it.
  Prefer it, and reach for a controller for what it does not cover
- if failed Jobs need to stay for post-mortem analysis and nobody has agreed how long — set the
  retention deliberately rather than accepting a default that deletes the evidence
- if a general TTL on arbitrary resources is what is wanted; that is [mayfly](../mayfly/README.md)

## Notes

The only recorded reference is the repository: <https://github.com/lwolf/kube-cleanup-operator>.

**Deployed here**, via a Flux `HelmRelease` against the `lwolf-charts` Helm repository, chart
version `1.0.4`. The configured policy is worth reading as a statement of intent:

| Setting | Value | Meaning |
|---|---|---|
| `--delete-successful-after` | `3m` | successful work is evidence of nothing; clear it almost immediately |
| `--delete-failed-after` | `60m` | failures get an hour to be noticed |
| `--delete-pending-pods-after` | `15m` | fifteen minutes unschedulable means it is not going to schedule |
| `--delete-evicted-pods-after` | `15m` | evicted Pods are noise |
| `--delete-orphaned-pods-after` | `15m` | the owning Job is gone; the Pod has no reason to exist |
| `--legacy-mode` | `false` | use the current controller behaviour rather than the pre-1.0 semantics |
| `rbac.global` | `true` | cluster-wide, not scoped to one namespace |

The one-hour window on failures is the setting to argue about. If nothing alerts on failed Jobs,
one hour means failures are deleted before anyone sees them, and the cluster looks healthy because
the evidence was collected by a cleanup controller. Retention is only safe when something else is
watching.

**Project health.** This is a small, single-purpose controller that has seen very little activity
for a long time. That matters less here than it would elsewhere — it watches two built-in resource
types and deletes them, and that API is stable. Still, treat it as maintenance-only software and be
aware that a Kubernetes version bump breaking it would not be fixed quickly.

---

[← Cleanup](../README.md)
