[← Alerting](../README.md)

# kwatch

<https://github.com/abahmed/kwatch>

---

## The problem it solves

Sometimes the requirement is simply: **tell me in Slack when a pod starts crash-looping.**

The usual answer to that is Prometheus, plus alert rules, plus Alertmanager, plus receivers —
a monitoring stack to deliver one notification.

kwatch is a single deployment that watches for pod failures and container crashes and posts
them, with the relevant log lines attached. No Prometheus, no rules, no exporters.

## When to use it

- small or early-stage clusters with no metrics stack yet
- development and lab environments where the goal is a heads-up, not an SLO
- you want a notification today and the metrics stack is a later project

## When not to use it

- you already run Prometheus and Alertmanager — this duplicates a subset of them with a second notification path
- you need symptom-based alerting, grouping, inhibition or on-call routing. It does none of that, by design

## The honest framing

Deliberately limited. That is the feature — it fills the gap between "no alerting at all" and
"a full observability stack", and the correct time to remove it is when Prometheus arrives.

---

[← Alerting](../README.md)
