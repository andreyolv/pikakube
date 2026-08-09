[← Events](../README.md)

# event_exporter

<https://github.com/caicloud/event_exporter>
<https://github.com/caicloud/event_exporter/blob/master/deploy/deploy.yml>

---

## The problem it solves

The other tools in this folder move event **text** somewhere durable. This one turns events
into **Prometheus metrics**, so you can alert on their rate.

That is a different question. "Store the reason so I can read it later" is retention; "tell
me when evictions across the cluster exceed a threshold" needs a number in Prometheus.

## When to use it

- you want to **alert** on event rates — a spike in `OOMKilled` or `FailedScheduling`
- events should appear on the same dashboards as the rest of the metrics

## When not to use it

- you need the event text preserved for investigation — that is [kubernetes-event-exporter](../kubernetes-event-exporter/README.md)
- you want object history — [sloop](../sloop/README.md)

## Usually both

Rates and text answer different halves of the same incident: the metric tells you something
started happening at 02:14, the stored event tells you what it said. Running one of each is
common and not redundant.

---

[← Events](../README.md)
