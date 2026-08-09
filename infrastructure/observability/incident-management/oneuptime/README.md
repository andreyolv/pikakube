[← Incident management](../README.md)

# OneUptime

<https://github.com/oneuptime/oneuptime>

---

## The problem it solves

Most teams assemble incident response from several products: uptime monitoring in one place,
on-call in another, status page in a third, incident timeline in a fourth.

OneUptime is one product covering all of it — monitoring, on-call schedules, escalation,
incident management, status pages and post-mortems. Positioned as the open-source alternative
to the commercial suites.

## When to use it

- you want a **status page** and incident tooling together, without integrating three services
- a small team where operating four tools is not realistic
- external users need to be told about incidents without each of them asking

## When not to use it

- Prometheus and Grafana already cover monitoring — you would be adopting a large platform for the on-call slice of it, and duplicating the rest
- you only need schedules and escalation — [GoAlert](../goalert/README.md) or [Grafana OnCall](../oncall/README.md) are much smaller

---

## Notes

> Does not support OCI Helm — the chart repository is awkward to work with.

Worth planning for in a GitOps setup where everything else is an `OCIRepository`: this one
needs a different source type, which makes it the exception in an otherwise uniform pipeline.

---

[← Incident management](../README.md)
