[← Events](../README.md)

# kubernetes-event-exporter

<https://github.com/resmoio/kubernetes-event-exporter>

---

## The problem it solves

Kubernetes events expire after roughly an hour, taking the explanation for last night's
incident with them.

This exports them to somewhere durable — Elasticsearch, Loki, Opsgenie, webhooks, chat — with
routing and filtering, so `OOMKilled` and `FailedScheduling` are still answerable tomorrow.

It is **the default choice** in this folder: actively maintained, flexible routing, and the
filtering needed to keep volume sane.

## When to use it

- events should land in the same store as logs, and be queryable together
- you want to route specific reasons somewhere specific — `OOMKilled` to a channel, everything else to storage

## When not to use it

- you want event *metrics* to alert on rather than the text — [event-exporter](../event-exporter/README.md)
- you want to browse a pod's history visually — [sloop](../sloop/README.md)

## Filter first

Unfiltered export is a large volume of routine noise. Start from the reasons that end
investigations — `OOMKilled`, `Evicted`, `FailedScheduling`, `FailedMount`,
`ImagePullBackOff` — and widen from there.

Dashboard: <https://grafana.com/grafana/dashboards/17882-kubernetes-event-exporter/>

---

[← Events](../README.md)
