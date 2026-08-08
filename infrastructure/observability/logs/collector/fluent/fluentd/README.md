[← Fluent family](../README.md)

# Fluentd

<https://github.com/fluent/fluentd>
<https://github.com/fluent/fluentd-ui>

---

## The problem it solves

The original CNCF log collector, written in Ruby, with the **largest plugin ecosystem** of
anything in this folder — over a thousand plugins covering inputs, outputs and transformations
that nothing else supports.

That ecosystem is now its main reason to exist. For ordinary Kubernetes log shipping,
[Fluent Bit](../fluent-bit/) is smaller and does the job; Fluentd earns its place when you
need a specific integration that only exists here.

## When to use it

- a required plugin exists only in the Ruby ecosystem — an unusual destination, a legacy
  format, a niche enrichment source
- as the **aggregator** behind Fluent Bit agents, where its footprint is paid once rather than per node
- an existing Fluentd deployment that works and has no reason to be replaced

## When not to use it

- greenfield Kubernetes log collection — Fluent Bit covers it at a fraction of the resource cost
- resource-constrained nodes; the Ruby runtime is heavy when multiplied by node count
- transformation is the main requirement — [Vector](../../vector/) is a better tool for that

## The honest positioning

Not deprecated, and not the default any more. The Fluent project's own centre of gravity has
moved to Fluent Bit, and Fluentd is now the specialist option rather than the general one.

Additional references: [`fluentd-daemonset/`](fluentd-daemonset/)

---

[← Fluent family](../README.md)
