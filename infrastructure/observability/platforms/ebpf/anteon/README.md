[← eBPF platforms](../README.md)

# Anteon

<https://github.com/getanteon/anteon>
<https://github.com/getanteon/anteon-helm-charts>

---

## What it is

An eBPF service map combined with **load testing** — an unusual pairing. The idea is that you
generate load and watch the resulting dependency graph and latency in the same tool, rather
than correlating a load generator with a separate observability stack.

## When to use it

- you want load testing and the resulting service behaviour in one place
- validating how a system degrades under load, without instrumenting it first

## When not to use it

- you want a service map for production use — [Coroot](../coroot/) is more complete and better maintained for that
- resources are tight. See below

---

## Notes

> It spins up an enormous number of pods — far more than the value justifies.

Worth knowing before installing it on anything small. On a laptop cluster or a modest node
pool, the footprint alone makes it impractical, regardless of whether the features fit.

## Related

For load testing as its own capability, see
[`software-engineering/tests/load/`](../../../../software-engineering/tests/load/) — k6 and
Locust, without an observability platform attached.

---

[← eBPF platforms](../README.md)
