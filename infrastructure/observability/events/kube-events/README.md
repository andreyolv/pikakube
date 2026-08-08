[← Events](../README.md)

# kube-events

<https://github.com/kubesphere/kube-events>

---

## The problem it solves

Between raw export and simple notification there is a middle ground: **rules over events**.
Not "send everything somewhere", but "when an event matches this pattern, do this".

kube-events, from the KubeSphere project, provides that — an event pipeline with rules for
filtering, alerting and archiving, expressed declaratively rather than in the configuration
of an exporter.

## When to use it

- you already run KubeSphere, where this is the native option
- you want event handling expressed as rules rather than exporter configuration
- filtering and alerting should be defined together, not split across two tools

## When not to use it

- there is no KubeSphere in the picture — [kubernetes-event-exporter](../kubernetes-event-exporter/) has a broader community and covers the export case well
- Prometheus and Alertmanager already own alerting, in which case adding a second rule engine for events splits the definition of "what is an alert" across two places

---

[← Events](../README.md)
