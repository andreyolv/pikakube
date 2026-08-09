[← Autoscaler](../README.md)

# Cluster Turndown

<https://github.com/kubecost/cluster-turndown>

---

## The problem it solves

Non-production clusters run all week and are used during office hours. Nights and weekends are
roughly two thirds of the hours in a week, paid for at full price.

Cluster Turndown, from the Kubecost project, scales a cluster down on a **schedule** rather than in
reaction to load. A `TurndownSchedule` custom resource declares a start, an end and a repeat
interval; at the start time the controller scales workloads down and shrinks node groups to a
minimum, and at the end time it puts everything back.

It is scheduled, not reactive, and that is the point — the Cluster Autoscaler cannot help with idle
time, because from its perspective idle pods with requests are perfectly legitimate.

## When to use it

- Development, staging and CI clusters with predictable working hours
- Cost reduction where the saving is measured in whole nodes, not in requests
- Environments where a few minutes of morning warm-up is acceptable

## When not to use it

- Production, or anything with users outside the assumed window
- Clusters running batch or scheduled jobs overnight — they will simply not run
- Stateful workloads that do not tolerate being stopped and restarted
- When workload-level shutdown is enough; [`sleep/`](../../sleep/README.md) scales Deployments without touching node groups, which is far less invasive

## Notes

**Deployed as plain manifests, not Helm** — `full.yaml`, `namespace.yaml` and
`turndownschedule.yaml`. It is the only tool in this folder without a chart, which reflects what
upstream provides.

The recorded schedule:

```yaml
apiVersion: kubecost.com/v1alpha1
kind: TurndownSchedule
metadata:
  name: pause-cluster
spec:
  start: 2025-03-12T00:00:00Z
  end: 2027-03-12T08:00:00Z
  repeat: daily
```

Read it carefully, because the semantics are not obvious: with `repeat: daily`, the **times of day**
from `start` and `end` are what recur — turn down at 00:00 UTC, bring back at 08:00 UTC. The dates
set when the schedule begins and when it stops repeating; the two-year span is simply "keep doing
this".

The times being **UTC** is the trap. An eight-hour window that looks like overnight in one timezone
is the middle of the working day in another, and daylight saving moves the boundary twice a year
relative to local office hours.

**Recorded upstream issue:** <https://github.com/kubecost/cluster-turndown/issues/65>.

Before adopting this, check the project's activity. Cluster Turndown sits at the edge of the
Kubecost product rather than at its centre, and a controller that scales your node groups to zero is
not a good place for an unmaintained dependency. The safer alternative for most of the benefit is
[`sleep/kube-downscaler`](../../sleep/kube-downscaler/README.md) or
[`sleep/kube-green`](../../sleep/kube-green/README.md), which scale workloads and let the Cluster
Autoscaler remove the nodes that are left empty — the same saving, without a second controller
holding the node groups.

---

[← Autoscaler](../README.md)
