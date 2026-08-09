[← Incident management](../README.md)

# Aurora

<https://github.com/Arvo-AI/aurora>

---

## The problem it solves

The first fifteen minutes of an incident are largely mechanical: gather the logs, check what
deployed recently, look at the obvious metrics, form a first hypothesis. Aurora aims to do
that automatically and hand the responder a starting point instead of a blank page.

## When to use it

- experimenting with AI-assisted triage as a **first responder**, ahead of a human
- alert volume is high enough that initial triage is itself the bottleneck

## When not to use it

- **as the paging layer.** This does not replace schedules, escalation or acknowledgement — that is [GoAlert](../goalert/README.md) or [Grafana OnCall](../oncall/README.md)
- where a wrong first hypothesis is expensive. A confident, incorrect starting point can cost more time than no starting point at all

## Related

The same idea appears in [`troubleshooting/`](../../troubleshooting/README.md) —
[HolmesGPT](../../troubleshooting/holmesgpt/README.md) and [k8sgpt](../../troubleshooting/k8sgpt/README.md)
both do AI-assisted diagnosis, from the cluster side rather than the incident side.

If AI-assisted triage is the goal, those two are more established and worth comparing first.

---

[← Incident management](../README.md)
