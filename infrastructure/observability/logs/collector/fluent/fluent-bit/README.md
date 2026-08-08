[← Fluent family](../README.md)

# Fluent Bit

<https://github.com/fluent/fluent-bit>
<https://github.com/fluent/helm-charts>

---

## The problem it solves

Something has to run on **every node**, tail every container log file, attach the Kubernetes
metadata that makes a line attributable, filter what will never be read, and ship the rest.

Fluent Bit does that in a few megabytes of memory. Written in C, CNCF graduated, and the
default choice for Kubernetes log collection — the footprint matters because the cost is
multiplied by node count.

## When to use it

- **the default** for shipping Kubernetes logs to any backend
- resource-constrained nodes, or large clusters where per-node overhead is multiplied
- as the agent half of an [agent-plus-aggregator](../README.md) setup

## When not to use it

- heavy transformation is needed in the collector — [Vector](../../vector/) and its VRL language are a better fit
- you need a plugin that only exists in the Ruby ecosystem — [Fluentd](../fluentd/)

## Configuration reality

Parsers, filters and routing live in a config format that is easy to start with and gets
awkward at scale. If the configuration is going to grow, [Fluent Operator](../fluent-operator/)
turns it into reviewable CRDs — worth deciding early rather than after a 500-line ConfigMap
exists.

---

## Notes

### Kubernetes events

Fluent Bit can collect Kubernetes **events**, not only container logs — which is one way to
solve the [one-hour expiry problem](../../../../events/README.md):

- <https://www.josehisse.dev/blog/exportando-eventos-do-kubernetes-com-o-fluentbit/>
- <https://github.com/fluent/fluent-bit/issues/1140>

Worth weighing against a dedicated exporter: doing it here means one fewer component, but
event-specific filtering and routing are more limited than in
[kubernetes-event-exporter](../../../../events/kubernetes-event-exporter/).

### Related projects

- <https://github.com/fluent/fluentd>
- <https://github.com/fluent/fluent-operator>
- <https://github.com/fluent/fluentd-ui>

---

[← Fluent family](../README.md)
