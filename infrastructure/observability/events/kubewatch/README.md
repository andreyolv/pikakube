[← Events](../README.md)

# kubewatch

<https://github.com/robusta-dev/kubewatch>

---

## The problem it solves

Sometimes the requirement is only: **tell the team in Slack when something changes in the
cluster** — a deployment updated, a pod created, a secret modified.

kubewatch watches cluster resources and pushes those changes to chat. No storage, no query
layer, no retention.

## When to use it

- a small team that wants visibility of cluster changes in a channel
- development environments, where "who just changed that?" is the common question
- an audit-trail feel without an audit-log pipeline

## When not to use it

- retention matters — this notifies, it does not store. [kubernetes-event-exporter](../kubernetes-event-exporter/README.md)
- you need a real audit trail — that is [audit logs](../../../security/2-cluster/audit/README.md), which are complete and tamper-evident in a way notifications are not
- the cluster is busy enough that the channel becomes unreadable

## Related

Maintained by the same project as [Robusta](../../alerting/robusta/README.md), which covers the richer
enrichment and automation case.

---

[← Events](../README.md)
