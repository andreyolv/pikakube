[← Incident management](../README.md)

# GoAlert

<https://github.com/target/goalert>

---

## The problem it solves

On-call scheduling and escalation, from Target, with a deliberate focus on **actually
reaching the person**: voice calls, SMS, push, and escalation when nobody acknowledges.

That emphasis is the point. Many tools stop at "we sent a notification". GoAlert treats
delivery and acknowledgement as the product, which is the part that matters at 3am.

## When to use it

- phone and SMS escalation is a hard requirement
- you want a self-contained, self-hosted service rather than a suite
- schedules, rotations and overrides need to be managed properly

## When not to use it

- Grafana is the centre of the stack and integration matters more — [Grafana OnCall](../oncall/README.md)
- you also want status pages and monitoring — [OneUptime](../oneuptime/README.md)

## Known issues worth reading before deploying

<https://github.com/target/goalert/issues/2107>
<https://github.com/target/goalert/issues/3093>

Worth reviewing up front: an on-call tool that misbehaves fails exactly when it is needed, and
these are the kind of thing you want to know about before the first page rather than during
it.

---

[← Incident management](../README.md)
