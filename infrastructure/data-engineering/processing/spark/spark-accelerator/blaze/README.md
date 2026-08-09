[← Spark accelerators](../README.md)

# Blaze

<https://github.com/kwai/blaze>

---

## What it is

A Spark accelerator from Kuaishou, built on
[DataFusion](../../../../query-engine/datafusion/README.md) — the same approach as
[DataFusion Comet](../datafusion-comet/README.md): intercept Spark's physical plan and execute it in a
native Rust engine.

Used in production at very large scale inside Kuaishou, which is a meaningful signal for a
component this invasive.

## When to use it

- evaluating DataFusion-based acceleration alongside Comet
- the operators your workload uses happen to be better covered here

## When not to use it

- Delta or Iceberg are required — as with Comet, check support before anything else. [Gluten](../gluten/README.md) is the option that covers both today
- you want the largest community; this is more narrowly used outside its origin
- there is no capacity to measure fallback rates on real plans

## How to choose between the three

They are close enough that features do not decide it. What does:

1. **Table format support** — Delta and Iceberg. This eliminates candidates immediately
2. **Fallback rate on your actual plans** — the only number that matters, and it is workload-specific
3. **Maintenance and community** — this is deep in the execution path, and being alone with a bug is expensive

Run the same real job through each, read the physical plan, count the fallbacks. That
comparison takes an afternoon and is worth more than any benchmark.

---

[← Spark accelerators](../README.md)
