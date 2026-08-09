[← Incident management](../README.md)

# Grafana OnCall

<https://github.com/grafana/oncall>

---

## The problem it solves

Alertmanager routes to a channel. Grafana OnCall routes to a **person** — with schedules,
rotations, escalation chains, acknowledgement, and delivery over push, SMS and phone.

Its advantage over the alternatives is proximity: it integrates directly with Grafana alerts
and with Alertmanager, so the alert, the dashboard and the escalation live in one place
rather than being wired together.

## When to use it

- Grafana is already the centre of the observability stack
- you want schedules and escalation without adopting a separate vendor
- alerts should link back to the dashboard they came from

## When not to use it

- Grafana is not part of the stack — the integration is the main reason to choose it
- you need a status page and broader incident tooling — [OneUptime](../oneuptime/README.md)

## Check the project's current status

Grafana has changed the positioning of OnCall over time. Before adopting it for a real
rotation, confirm the maintenance and licensing situation — an on-call system is a poor place
to discover a project has changed direction.

---

[← Incident management](../README.md)
