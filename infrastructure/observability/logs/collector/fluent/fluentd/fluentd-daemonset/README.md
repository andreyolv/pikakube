[← Fluentd](../README.md)

# Fluentd DaemonSet

Manifests for running [Fluentd](../README.md) directly as a DaemonSet, without an operator.

---

## When this shape makes sense

- an existing Fluentd deployment being kept as-is
- a plugin only available in the Ruby ecosystem is required on the node itself
- you want the collector configuration visible as plain manifests rather than behind CRDs

## When it does not

Running Fluentd on **every node** means paying the Ruby runtime footprint per node.
[Fluent Bit](../../fluent-bit/README.md) is the DaemonSet in almost every current setup, with Fluentd —
if needed at all — sitting behind it as an aggregator where the cost is paid a few times
instead of once per node.

## Reference

Web UI for Fluentd configuration: <https://github.com/fluent/fluentd-ui>

---

[← Fluentd](../README.md)
