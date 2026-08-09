[← Dashboards](../README.md)

# Kubevious

<https://github.com/kubevious/kubevious>
<https://github.com/kubevious/helm>

---

## The problem it solves

Kubevious reorganises the cluster into an **application-centric tree** instead of a flat list of
resource types, and then validates it. Rather than showing you Deployments in one view and
ConfigMaps in another, it shows a workload with everything attached to it — its config, its secrets,
its service, its ingress, its RBAC — in one place.

On top of that structure it runs checks and surfaces misconfigurations: a Service selecting nothing,
a mount referencing a ConfigMap that does not exist, overlapping ingress rules, missing resource
limits. It also keeps a time machine of past states, which is unusual for a dashboard.

## When to use it

- Auditing a cluster you have inherited and do not understand
- Finding config errors that are valid YAML and still wrong
- Explaining how one application's objects fit together
- You want a record of what the cluster looked like before a change

## When not to use it

- As a routine operations console; it is an analysis tool
- Where a policy engine already enforces these rules — Kyverno or Gatekeeper reject at admission,
  which is strictly better than reporting afterwards
- Small clusters, where the structure is already obvious
- If the extra storage and processing it needs are not justified by the questions you have

## Notes

**Chart** `kubevious` version `1.2.2` from `https://helm.kubevious.io`.

**The chart lives in a separate repository** — <https://github.com/kubevious/helm>, distinct from
<https://github.com/kubevious/kubevious>. That is why both links are recorded, and it is worth
knowing generally: when a project splits its chart out, the chart's issues, versioning and release
cadence are separate from the application's. Looking for a values option in the main repository and
not finding it is a common half-hour.

No other notes were recorded.

The distinction that decides whether this is useful: **Kubevious reports, admission control
prevents.** Finding that a Deployment has no resource limits is worth something; refusing to admit it
is worth more. If a policy engine is already in place, Kubevious's validation is largely redundant
and its value narrows to the application-centric view and the time machine — which are still real,
just narrower.

The other thing it does that nothing else in this folder does is keep **history**. Every dashboard
here shows the present; Kubevious can show the cluster as it was, which puts it a little closer to
[`observability/`](../../../../../observability/README.md) than its neighbours.

---

[← Dashboards](../README.md)
